#!/usr/bin/env python3
"""
视频字幕提取工具（支持 YouTube/B站）
用法: python extract_single.py <视频链接>
"""

import subprocess
import os
import re
import sys
import time
from pathlib import Path

# Windows 环境修复：强制 UTF-8 编码，将 Python Scripts 目录加入 PATH
os.environ["PYTHONUTF8"] = "1"
_scripts_dir = os.path.join(os.path.dirname(sys.executable), "Scripts")
if os.path.isdir(_scripts_dir) and _scripts_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = _scripts_dir + os.pathsep + os.environ["PATH"]

from config_loader import get_cookies_file, get_subtitles_dir, get_temp_dir


def detect_platform(url: str) -> str:
    """根据URL自动检测平台"""
    if "bilibili.com" in url or "b23.tv" in url:
        return "bilibili"
    return "youtube"


def get_video_info(url: str, cookies_file: str = None) -> dict:
    """获取视频标题和发布日期"""
    cmd = ["yt-dlp", "--js-runtimes", "node", "--print", "%(title)s\n%(upload_date)s\n%(uploader)s"]
    if cookies_file:
        cmd.extend(["--cookies", cookies_file])
    cmd.append(url)

    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    lines = result.stdout.strip().split("\n")
    title = lines[0] if len(lines) > 0 else ""
    upload_date = lines[1] if len(lines) > 1 else ""
    uploader = lines[2] if len(lines) > 2 else ""

    # 格式化发布日期（从 YYYYMMDD 转为 YYYY-MM-DD）
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    # 清理文件名中的非法字符
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    return {"title": title, "safe_title": safe_title, "upload_date": upload_date, "uploader": uploader}


def download_subtitle(url: str, output_dir: str, platform: str, cookies_file: str = None) -> str | None:
    """下载字幕文件，返回字幕文件路径"""
    # 根据平台设置语言优先级
    if platform == "bilibili":
        # B站：先尝试中文字幕，再尝试 AI 英文字幕
        lang_options = ["zh-CN,zh-Hans,zh-Hant,zh,ai-zh", "ai-en"]
    else:
        lang_options = ["zh-CN,zh-Hans,zh-Hant,zh,en", "en,en-US"]

    for langs in lang_options:
        cmd = [
            "yt-dlp",
            "--js-runtimes", "node",
            "--write-auto-sub",
            "--write-sub",
            "--sub-lang", langs,
            "--sub-format", "vtt/srt/best",
            "--skip-download",
        ]
        if cookies_file:
            cmd.extend(["--cookies", cookies_file])
        cmd.append(url)

        result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", cwd=output_dir)

        # 查找生成的字幕文件
        priority = ["zh-CN", "zh-Hans", "zh-Hans-zh-CN", "zh-Hant", "zh-Hant-zh-CN", "zh", "ai-zh", "en", "en-zh-CN", "en-US", "ai-en"]
        for lang in priority:
            for ext in ["vtt", "srt"]:
                for f in Path(output_dir).glob(f"*.{lang}.{ext}"):
                    return str(f)
        for ext in ["vtt", "srt"]:
            for f in Path(output_dir).glob(f"*.{ext}"):
                return str(f)

        # 如果是限速错误，等待后重试
        if "429" in result.stderr or "请求过于频繁" in result.stderr:
            print("   遇到限速，等待 5 秒后重试...")
            time.sleep(5)
            continue

    return None


def parse_subtitle(subtitle_path: str) -> str:
    """解析字幕文件（VTT/SRT），提取纯文本"""
    with open(subtitle_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    text_lines = []
    seen = set()

    for line in lines:
        if "-->" in line or line.strip() == "" or line.startswith("WEBVTT"):
            continue
        if line.strip().isdigit():
            continue
        clean_line = re.sub(r"<[^>]+>", "", line).strip()
        clean_line = re.sub(r"\{[^}]+\}", "", clean_line)
        if clean_line and clean_line not in seen:
            seen.add(clean_line)
            text_lines.append(clean_line)

    return " ".join(text_lines)


def check_environment():
    """检查运行环境，提前报告缺失依赖"""
    errors = []
    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            errors.append("yt-dlp 无法正常运行")
    except FileNotFoundError:
        errors.append("yt-dlp 未安装或不在 PATH 中。请运行: pip install yt-dlp")
    if errors:
        for e in errors:
            print(f"❌ {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("用法: python extract_single.py <视频链接>")
        print("支持: YouTube, B站")
        sys.exit(1)

    url = sys.argv[1]
    check_environment()
    platform = detect_platform(url)
    platform_name = "B站" if platform == "bilibili" else "YouTube"

    # 从配置获取 cookies 文件（仅 B 站需要）
    cookies_file = get_cookies_file() if platform == "bilibili" else None

    # 从配置获取目录
    subtitles_dir = get_subtitles_dir()
    temp_dir = get_temp_dir()

    print(f"📺 平台: {platform_name}")

    if platform == "bilibili" and not cookies_file:
        print("⚠️  警告: B站字幕需要登录，请在配置文件中设置 cookies_file 路径")

    print("📥 正在获取视频信息...")
    video_info = get_video_info(url, cookies_file)
    print(f"   标题: {video_info['title']}")
    if video_info['upload_date']:
        print(f"   发布日期: {video_info['upload_date']}")
    if video_info['uploader']:
        print(f"   博主: {video_info['uploader']}")

    print("📝 正在下载字幕...")
    subtitle_path = download_subtitle(url, str(temp_dir), platform, cookies_file)

    if not subtitle_path:
        print("❌ 无法获取字幕，该视频可能没有字幕")
        sys.exit(1)

    print("🔍 正在解析字幕...")
    subtitle_text = parse_subtitle(subtitle_path)

    # 保存为txt文件
    output_file = subtitles_dir / f"{video_info['safe_title'][:80]}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"标题: {video_info['title']}\n")
        f.write(f"链接: {url}\n")
        f.write(f"平台: {platform_name}\n")
        if video_info['upload_date']:
            f.write(f"发布日期: {video_info['upload_date']}\n")
        if video_info['uploader']:
            f.write(f"博主: {video_info['uploader']}\n")
        f.write("-" * 50 + "\n\n")
        f.write(subtitle_text)

    # 清理临时文件
    os.remove(subtitle_path)

    print(f"✅ 字幕已保存到: {output_file}")


if __name__ == "__main__":
    main()
