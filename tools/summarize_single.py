#!/usr/bin/env python3
"""
视频深度解读工具
用法: python summarize_single.py <字幕文件路径>

针对高质量访谈、演讲、教学视频进行深度解读，
让读者不看视频也能获得 80% 以上的核心价值。
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows 环境修复：强制 UTF-8 编码
os.environ["PYTHONUTF8"] = "1"

import anthropic

from config_loader import get_anthropic_api_key, get_anthropic_base_url, get_summaries_dir


def get_client() -> anthropic.Anthropic:
    """获取 API 客户端（优先环境变量，其次配置文件）"""
    api_key = get_anthropic_api_key()
    base_url = get_anthropic_base_url()

    if not api_key:
        print("❌ 请设置 ANTHROPIC_API_KEY 环境变量，或在 ~/.video-summary/config.yaml 中配置 anthropic_api_key")
        sys.exit(1)

    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
        print(f"🔗 使用自定义 API 地址: {base_url}")

    return anthropic.Anthropic(**kwargs)


def read_subtitle(file_path: str) -> tuple[str, str, str, str, str, str]:
    """读取字幕文件，返回(标题, 链接, 平台, 发布日期, 博主, 内容)"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 尝试提取标题
    title_match = re.search(r"标题: (.+)", content)
    title = title_match.group(1) if title_match else Path(file_path).stem

    # 尝试提取链接
    url_match = re.search(r"链接: (.+)", content)
    url = url_match.group(1) if url_match else ""

    # 尝试提取平台
    platform_match = re.search(r"平台: (.+)", content)
    platform = platform_match.group(1) if platform_match else ""

    # 尝试提取发布日期
    upload_date_match = re.search(r"发布日期: (.+)", content)
    upload_date = upload_date_match.group(1) if upload_date_match else ""

    # 尝试提取博主
    uploader_match = re.search(r"博主: (.+)", content)
    uploader = uploader_match.group(1) if uploader_match else ""

    # 获取正文内容（跳过头部信息）
    if "-" * 10 in content:
        text = content.split("-" * 10, 1)[-1].strip()
    else:
        text = content

    return title, url, platform, upload_date, uploader, text


def summarize_with_ai(text: str, title: str) -> dict:
    """使用 Claude 进行深度解读"""

    # 根据内容长度动态调整输入
    max_input_chars = 80000  # 约 20000 tokens
    truncated_text = text[:max_input_chars]
    is_truncated = len(text) > max_input_chars

    prompt = f"""你是一位资深的视频内容深度解读专家，擅长分析高质量的访谈、演讲和教学视频。你的任务是为未观看视频的读者提供全面、深入的内容解读，让他们仅通过阅读你的解读就能完整理解视频的核心价值。

## 视频信息
- 标题：{title}
- 字幕内容{"（已截取前半部分）" if is_truncated else ""}：

{truncated_text}

---

## 解读要求

请按照以下结构进行深度解读，全部使用中文：

### 一、视频概览
1. **视频类型**：判断是访谈/演讲/教学/纪录片/其他
2. **核心主题**：一句话概括视频要传达的核心信息
3. **目标受众**：这个视频适合什么样的观众
4. **内容价值**：这个视频能给观众带来什么收获

### 二、内容脉络（重要）
按视频的逻辑顺序，梳理出清晰的内容结构：
- 如果是访谈：按话题/问题分段梳理
- 如果是演讲：按演讲者的论述逻辑分段
- 如果是教学：按知识点/步骤分段
用 1、2、3... 标注各部分，每部分简述主要内容（2-3句）

### 三、核心观点深度解读
挑选视频中 3-5 个最有价值的观点/论述/知识点，进行深度解读：
- 原始观点是什么
- 为什么这个观点重要
- 背后的逻辑/原理是什么
- 对读者有什么启发

### 四、关键信息提取
- **数据与事实**：视频中提到的重要数据、案例、事实
- **方法与工具**：提到的方法论、工具、框架
- **人物与引用**：提到的重要人物、书籍、资源

### 五、金句摘录
提取 5-10 句最有价值的原话（保留原文，可适当翻译）

### 六、思考与启发
- 这个视频最大的价值是什么
- 观众可以从中学到什么
- 有哪些可以立即行动的建议

### 七、元信息
- **分类**：科技/商业/教育/人文/生活/其他
- **关键词**：8-12 个关键词
- **推荐指数**：★★★★★（1-5星）
- **适合人群**：简述

---

请确保解读足够深入和详尽，让读者不看视频也能获得 80% 以上的核心价值。
"""

    client = get_client()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.content[0].text

    # 提取分类
    category_match = re.search(r"\*\*分类\*\*[：:]\s*(.+?)(?=\n|$)", result_text)
    category = category_match.group(1).strip() if category_match else "其他"

    return {
        "category": category,
        "analysis": result_text
    }


def save_result(title: str, url: str, platform: str, upload_date: str, uploader: str, analysis: dict, subtitle_text: str):
    """保存深度解读结果"""
    summaries_dir = get_summaries_dir()

    date_str = datetime.now().strftime("%y-%m-%d")
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = f"{date_str}-{safe_title[:50]}.md"
    filepath = summaries_dir / filename

    # 构建元信息
    meta_lines = [f"> **解读日期**: {date_str}"]
    if upload_date:
        meta_lines.append(f"> **视频发布日期**: {upload_date}")
    if uploader:
        meta_lines.append(f"> **博主**: {uploader}")
    if url:
        meta_lines.append(f"> **原视频**: [{platform or '链接'}]({url})")
    if platform:
        meta_lines.append(f"> **平台**: {platform}")
    meta_lines.append(f"> **分类**: {analysis['category']}")
    meta_info = "\n".join(meta_lines)

    content = f"""# {title}

{meta_info}

---

{analysis['analysis']}

---

<details>
<summary>📜 原始字幕（点击展开）</summary>

{subtitle_text[:15000]}{"..." if len(subtitle_text) > 15000 else ""}

</details>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def main():
    if len(sys.argv) < 2:
        print("用法: python summarize_single.py <字幕文件路径>")
        print("示例: python summarize_single.py ../subtitles/视频标题.txt")
        print("\n本工具针对高质量访谈、演讲、教学视频进行深度解读")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)

    print("📖 正在读取字幕...")
    title, url, platform, upload_date, uploader, subtitle_text = read_subtitle(file_path)
    print(f"   标题: {title}")
    if upload_date:
        print(f"   发布日期: {upload_date}")
    if uploader:
        print(f"   博主: {uploader}")
    if url:
        print(f"   链接: {url}")
    print(f"   字幕长度: {len(subtitle_text)} 字符")

    print("🤖 正在进行 AI 深度解读（这可能需要一些时间）...")
    analysis = summarize_with_ai(subtitle_text, title)

    print("💾 正在保存结果...")
    result_path = save_result(title, url, platform, upload_date, uploader, analysis, subtitle_text)

    print(f"✅ 深度解读完成！结果已保存到: {result_path}")
    print(f"\n{'='*60}\n")
    print(analysis['analysis'])


if __name__ == "__main__":
    main()
