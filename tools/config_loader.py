#!/usr/bin/env python3
"""
配置加载模块 - 从 ~/.video-summary/config.yaml 读取用户配置
"""

from pathlib import Path

import yaml


DEFAULT_CONFIG = {
    "output_dir": "~/Documents/video-summaries",
    "cookies_file": "",
    "anthropic_api_key": "",
    "anthropic_base_url": "",
}

CONFIG_DIR = Path.home() / ".video-summary"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


def load_config() -> dict:
    """
    加载用户配置，合并默认值

    Returns:
        dict: 配置字典，包含以下键：
            - output_dir: 输出目录（字幕、总结和临时文件）
            - cookies_file: B站 cookies 文件路径（可选）
    """
    config = DEFAULT_CONFIG.copy()

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}
            config.update({k: v for k, v in user_config.items() if v})
        except Exception as e:
            print(f"⚠️  配置文件读取失败: {e}，使用默认配置")

    return config


def get_anthropic_api_key() -> str | None:
    """获取 API key，优先使用环境变量，其次使用配置文件"""
    import os
    key = os.getenv("ANTHROPIC_API_KEY")
    if key:
        return key
    config = load_config()
    return config.get("anthropic_api_key") or None


def get_anthropic_base_url() -> str | None:
    """获取 API base URL，优先使用环境变量，其次使用配置文件"""
    import os
    url = os.getenv("ANTHROPIC_BASE_URL")
    if url:
        return url
    config = load_config()
    return config.get("anthropic_base_url") or None


def get_output_dir() -> Path:
    """获取输出目录，自动展开 ~ 符号"""
    config = load_config()
    output_dir = Path(config["output_dir"]).expanduser()
    return output_dir


def get_cookies_file() -> str | None:
    """
    获取 cookies 文件路径
    优先级：配置文件 > 安装目录
    """
    config = load_config()

    # 优先使用配置文件中的路径
    cookies_path = config.get("cookies_file", "")
    if cookies_path:
        path = Path(cookies_path).expanduser()
        if path.exists():
            return str(path)

    # 回退到安装目录下的 cookies.txt
    tools_dir = Path(__file__).parent
    default_cookies = tools_dir.parent / "cookies.txt"
    if default_cookies.exists():
        return str(default_cookies)

    return None


def get_summaries_dir() -> Path:
    """获取总结文件保存目录"""
    summaries_dir = get_output_dir() / "summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)
    return summaries_dir


def get_subtitles_dir() -> Path:
    """获取字幕文件保存目录"""
    subtitles_dir = get_output_dir() / "subtitles"
    subtitles_dir.mkdir(parents=True, exist_ok=True)
    return subtitles_dir


def get_temp_dir() -> Path:
    """获取临时文件目录"""
    temp_dir = get_output_dir() / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def ensure_config_exists():
    """确保配置目录和默认配置文件存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        default_content = """# Video Summary Skill 配置文件

# 输出目录（字幕、总结和临时文件）
output_dir: ~/Documents/video-summaries

# B站 cookies 文件路径（可选，用于下载需要登录的视频字幕）
# 示例: ~/.video-summary/cookies.txt
cookies_file: ""

# Anthropic API Key（可选，也可通过环境变量 ANTHROPIC_API_KEY 设置）
anthropic_api_key: ""

# Anthropic API Base URL（可选，用于代理服务）
anthropic_base_url: ""
"""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(default_content)


if __name__ == "__main__":
    # 测试配置加载
    print("配置文件路径:", CONFIG_FILE)
    print("配置内容:", load_config())
    print("输出目录:", get_output_dir())
    print("Cookies 文件:", get_cookies_file())
