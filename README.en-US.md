# Video Summary Skill

A video summary Skill for [Claude Code](https://claude.ai/download). Supports YouTube and Bilibili videos, automatically extracts subtitles and generates deep analysis directly through Claude Code.

## Features

- Supports YouTube and Bilibili videos
- Automatically extracts video subtitles (multi-language support)
- Deep analysis directly through Claude Code with no additional API calls
- Cross-platform support (macOS / Linux / Windows)

## System Requirements

- Python 3.9+
- [Claude Code](https://claude.ai/download)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (automatically installed by the setup script)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/ZOO-AiiiPM/video-summary-skill.git
cd video-summary-skill
```

### 2. Run the installation script

**macOS / Linux:**

```bash
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**

```powershell
# If you encounter execution policy restrictions, run first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run the installation script
.\install.ps1
```

The installation script will:
- Check and install dependencies
- Copy tools to `~/.video-summary/`
- Interactively create the configuration file
- Install Claude Code Skill

### 3. Use

Simply tell Claude Code the video you want to summarize:

```
Summarize this video https://youtube.com/watch?v=xxx
```

Or use the skill command:

```
/video-summary https://www.bilibili.com/video/BVxxx
```

Claude Code will automatically extract subtitles and generate a deep analysis.

## Configuration Instructions

Configuration file location:
- macOS / Linux: `~/.video-summary/config.yaml`
- Windows: `%USERPROFILE%\.video-summary\config.yaml`

```yaml
# Output directory (subtitles, summaries, and temporary files)
# Supports Chinese paths, e.g.: ~/Documents/视频总结
output_dir: ~/Documents/video-summaries

# Obsidian inbox directory (optional, summaries will be saved here if set)
obsidian_dir: ""

# Bilibili cookies file path (optional)
cookies_file: ~/.video-summary/cookies.txt
```

### Getting Bilibili Cookies

Bilibili video subtitles require login to obtain. You can use a browser extension to export cookies:

1. Install [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) extension
2. Log in to Bilibili
3. Export cookies.txt to the path specified in the configuration file

## Directory Structure

```
~/.video-summary/
├── config.yaml          # Configuration file
├── cookies.txt          # Bilibili cookies (optional)
└── tools/               # Python tool scripts

~/.claude/skills/video-summary/
└── SKILL.md             # Claude Code Skill definition

~/Documents/video-summaries/  # Default output directory
├── subtitles/           # Extracted subtitles
├── summaries/           # Generated summaries
└── temp/                # Temporary files
```

## Uninstallation

**macOS / Linux:**

```bash
./uninstall.sh
```

**Windows:**

```powershell
.\uninstall.ps1
```

## Frequently Asked Questions

### Q: Subtitle extraction fails?

1. Ensure yt-dlp is up to date:
   - macOS/Linux: `yt-dlp -U`
   - Windows: `pip install -U yt-dlp`
2. Configure cookies for Bilibili videos
3. Some videos may not have subtitles

### Q: Cannot execute scripts in PowerShell on Windows?

Run the following command to allow local script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: How to update?

```bash
cd video-summary-skill
git pull
./install.sh  # macOS/Linux
# Or
.\install.ps1  # Windows
```

## License

MIT
