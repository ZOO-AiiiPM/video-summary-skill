#!/bin/bash
# Video Summary Skill 安装脚本
# 用法: ./install.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 安装目录
INSTALL_DIR="$HOME/.video-summary"
SKILL_DIR="$HOME/.claude/skills/video-summary"
CONFIG_FILE="$INSTALL_DIR/config.yaml"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Video Summary Skill 安装程序${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查依赖
echo -e "${YELLOW}[1/6]${NC} 检查依赖..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装，请先安装 Python 3.9+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "   ✓ Python $PYTHON_VERSION"

# 检查 yt-dlp
if ! command -v yt-dlp &> /dev/null; then
    echo -e "${YELLOW}   ⚠ yt-dlp 未安装，正在安装...${NC}"
    if command -v brew &> /dev/null; then
        brew install yt-dlp
    elif command -v pip3 &> /dev/null; then
        pip3 install yt-dlp
    else
        echo -e "${RED}❌ 无法自动安装 yt-dlp，请手动安装${NC}"
        exit 1
    fi
fi
echo -e "   ✓ yt-dlp $(yt-dlp --version 2>/dev/null | head -1)"

# 检查 Claude Code
if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}   ⚠ Claude Code 未安装${NC}"
    echo -e "   请访问 https://claude.ai/download 安装 Claude Code"
fi

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 创建安装目录
echo -e "${YELLOW}[2/6]${NC} 创建安装目录..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$SKILL_DIR"

# 复制工具文件
echo -e "${YELLOW}[3/6]${NC} 复制工具文件..."
cp -r "$SCRIPT_DIR/tools" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/tools/extract_single.py"
chmod +x "$INSTALL_DIR/tools/summarize_single.py"
echo -e "   ✓ 工具已复制到 $INSTALL_DIR/tools/"

# 安装 Python 依赖
echo -e "${YELLOW}[4/6]${NC} 安装 Python 依赖..."
pip3 install -q -r "$INSTALL_DIR/tools/requirements.txt"
echo -e "   ✓ Python 依赖已安装"

# 生成配置文件
echo -e "${YELLOW}[5/6]${NC} 配置设置..."

if [ -f "$CONFIG_FILE" ]; then
    echo -e "   配置文件已存在: $CONFIG_FILE"
    read -p "   是否覆盖? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "   ✓ 保留现有配置"
    else
        rm "$CONFIG_FILE"
    fi
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo -e "${BLUE}请配置以下选项：${NC}"
    echo ""

    # 询问输出目录
    read -p "视频总结保存目录 [默认: ~/Documents/video-summaries]: " OUTPUT_DIR
    OUTPUT_DIR=${OUTPUT_DIR:-"~/Documents/video-summaries"}

    # 询问 B站 cookies
    echo ""
    echo "B站视频需要登录才能获取字幕。"
    read -p "B站 cookies 文件路径 (可选，留空跳过): " COOKIES_FILE

    # 生成配置文件
    cat > "$CONFIG_FILE" << EOF
# Video Summary Skill 配置文件

# 输出目录（字幕、总结和临时文件）
output_dir: $OUTPUT_DIR

# B站 cookies 文件路径（可选，用于下载需要登录的视频字幕）
cookies_file: "$COOKIES_FILE"
EOF

    echo -e "   ✓ 配置文件已生成: $CONFIG_FILE"
fi

# 生成 SKILL.md
echo -e "${YELLOW}[6/6]${NC} 安装 Claude Code Skill..."

TOOLS_DIR="$INSTALL_DIR/tools"
sed "s|{{TOOLS_DIR}}|$TOOLS_DIR|g" "$SCRIPT_DIR/skill/SKILL.md.template" > "$SKILL_DIR/SKILL.md"
echo -e "   ✓ Skill 已安装到 $SKILL_DIR/"

# 完成
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ 安装完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "接下来请配置 API Key："
echo ""
echo -e "${BLUE}添加到 shell 配置文件：${NC}"
echo -e "  echo 'export ANTHROPIC_API_KEY=sk-xxx' >> ~/.zshrc"
echo -e "  source ~/.zshrc"
echo ""
echo -e "${BLUE}使用代理服务（可选）：${NC}"
echo -e "  echo 'export ANTHROPIC_BASE_URL=https://your-proxy.com' >> ~/.zshrc"
echo ""
echo -e "${BLUE}使用方法：${NC}"
echo -e "  在 Claude Code 中输入："
echo -e "  ${GREEN}/video-summary https://youtube.com/watch?v=xxx${NC}"
echo ""
echo -e "配置文件位置: $CONFIG_FILE"
echo -e "工具目录: $TOOLS_DIR"
echo ""
