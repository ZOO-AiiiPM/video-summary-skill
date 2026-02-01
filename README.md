# Video Summary Skill

一个用于 [Claude Code](https://claude.ai/download) 的视频总结 Skill。支持 YouTube 和 B站视频，自动提取字幕并由 Claude Code 直接生成深度解读。

## 功能特点

- 支持 YouTube 和 B站视频
- 自动提取视频字幕（支持多语言）
- Claude Code 直接深度解读，无需额外 API 调用
- 跨平台支持（macOS / Linux / Windows）

## 系统要求

- Python 3.9+
- [Claude Code](https://claude.ai/download)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)（安装脚本会自动安装）

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/ZOO-AiiiPM/video-summary-skill.git
cd video-summary-skill
```

### 2. 运行安装脚本

**macOS / Linux:**

```bash
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**

```powershell
# 如果遇到执行策略限制，先运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后运行安装脚本
.\install.ps1
```

安装脚本会：
- 检查并安装依赖
- 复制工具到 `~/.video-summary/`
- 交互式创建配置文件
- 安装 Claude Code Skill

### 3. 使用

直接告诉 Claude Code 你想总结的视频：

```
总结这个视频 https://youtube.com/watch?v=xxx
```

或使用 skill 命令：

```
/video-summary https://www.bilibili.com/video/BVxxx
```

Claude Code 会自动提取字幕并生成深度解读。

## 配置说明

配置文件位置：
- macOS / Linux: `~/.video-summary/config.yaml`
- Windows: `%USERPROFILE%\.video-summary\config.yaml`

```yaml
# 输出目录（字幕、总结和临时文件）
# 支持中文路径，如: ~/Documents/视频总结
output_dir: ~/Documents/video-summaries

# Obsidian 收件箱目录（可选，设置后总结会保存到这里）
obsidian_dir: ""

# B站 cookies 文件路径（可选）
cookies_file: ~/.video-summary/cookies.txt
```

### 获取 B站 Cookies

B站视频字幕需要登录才能获取。你可以使用浏览器扩展导出 cookies：

1. 安装 [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) 扩展
2. 登录 B站
3. 导出 cookies.txt 到配置文件指定的路径

## 目录结构

```
~/.video-summary/
├── config.yaml          # 配置文件
├── cookies.txt          # B站 cookies（可选）
└── tools/               # Python 工具脚本

~/.claude/skills/video-summary/
└── SKILL.md             # Claude Code Skill 定义

~/Documents/video-summaries/  # 默认输出目录
├── subtitles/           # 提取的字幕
├── summaries/           # 生成的总结
└── temp/                # 临时文件
```

## 卸载

**macOS / Linux:**

```bash
./uninstall.sh
```

**Windows:**

```powershell
.\uninstall.ps1
```

## 常见问题

### Q: 字幕提取失败？

1. 确保 yt-dlp 是最新版本：
   - macOS/Linux: `yt-dlp -U`
   - Windows: `pip install -U yt-dlp`
2. B站视频需要配置 cookies
3. 某些视频可能没有字幕

### Q: Windows 上 PowerShell 无法执行脚本？

运行以下命令允许执行本地脚本：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: 如何更新？

```bash
cd video-summary-skill
git pull
./install.sh  # macOS/Linux
# 或
.\install.ps1  # Windows
```

## License

MIT
