# Video Summary Skill

一个用于 [Claude Code](https://claude.ai/download) 的视频总结 Skill。支持 YouTube 和 B站视频，自动提取字幕并生成 AI 深度解读。

## 功能特点

- 支持 YouTube 和 B站视频
- 自动提取视频字幕（支持多语言）
- AI 深度解读，生成结构化的总结
- 跨平台支持（macOS / Linux / Windows）

## 系统要求

- Python 3.9+
- [Claude Code](https://claude.ai/download)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)（安装脚本会自动安装）

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/zoo/video-summary-skill.git
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

### 3. 配置 API Key

**macOS / Linux:**

```bash
echo 'export ANTHROPIC_API_KEY=sk-xxx' >> ~/.zshrc
source ~/.zshrc

# 如果使用代理服务（可选）
echo 'export ANTHROPIC_BASE_URL=https://your-proxy.com' >> ~/.zshrc
```

**Windows (PowerShell):**

```powershell
# 设置用户环境变量（永久生效）
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-xxx", "User")

# 如果使用代理服务（可选）
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "https://your-proxy.com", "User")

# 重启终端使环境变量生效
```

### 4. 使用

在 Claude Code 中输入：

```
/video-summary https://youtube.com/watch?v=xxx
```

或

```
/video-summary https://www.bilibili.com/video/BVxxx
```

## 配置说明

配置文件位置：
- macOS / Linux: `~/.video-summary/config.yaml`
- Windows: `%USERPROFILE%\.video-summary\config.yaml`

```yaml
# 输出目录（字幕、总结和临时文件）
output_dir: ~/Documents/video-summaries

# B站 cookies 文件路径（可选）
cookies_file: ~/.video-summary/cookies.txt
```

### 获取 B站 Cookies

B站视频字幕需要登录才能获取。你可以使用浏览器扩展导出 cookies：

1. 安装 [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) 扩展
2. 登录 B站
3. 导出 cookies.txt 到配置文件指定的路径

## 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `ANTHROPIC_API_KEY` | ✅ | Anthropic API 密钥 |
| `ANTHROPIC_BASE_URL` | ❌ | 自定义 API 地址（用于代理服务） |

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

### Q: AI 总结失败？

1. 检查 API Key 是否正确配置
2. 检查网络连接
3. 如果使用代理，确保 `ANTHROPIC_BASE_URL` 配置正确

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
