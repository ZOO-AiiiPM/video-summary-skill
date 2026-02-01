#!/bin/bash
# Video Summary Skill 卸载脚本
# 用法: ./uninstall.sh

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 安装目录
INSTALL_DIR="$HOME/.video-summary"
SKILL_DIR="$HOME/.claude/skills/video-summary"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Video Summary Skill 卸载程序${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}将删除以下内容：${NC}"
echo -e "  - 工具目录: $INSTALL_DIR"
echo -e "  - Skill 目录: $SKILL_DIR"
echo ""

read -p "是否继续卸载? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消卸载${NC}"
    exit 0
fi

echo ""

# 删除 Skill 目录
if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    echo -e "✓ 已删除 Skill 目录"
else
    echo -e "  Skill 目录不存在，跳过"
fi

# 询问是否保留配置
if [ -d "$INSTALL_DIR" ]; then
    read -p "是否保留配置文件和生成的总结? (Y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        rm -rf "$INSTALL_DIR"
        echo -e "✓ 已删除安装目录（包括配置和数据）"
    else
        # 只删除工具，保留配置
        rm -rf "$INSTALL_DIR/tools"
        echo -e "✓ 已删除工具文件"
        echo -e "  配置文件已保留: $INSTALL_DIR/config.yaml"
    fi
else
    echo -e "  安装目录不存在，跳过"
fi

echo ""
echo -e "${GREEN}✅ 卸载完成${NC}"
echo ""
echo -e "如需重新安装，请运行:"
echo -e "  ./install.sh"
echo ""
