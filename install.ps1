# Video Summary Skill 安装脚本 (Windows)
# 用法: .\install.ps1

$ErrorActionPreference = "Stop"

# 安装目录
$INSTALL_DIR = "$env:USERPROFILE\.video-summary"
$SKILL_DIR = "$env:USERPROFILE\.claude\skills\video-summary"
$CONFIG_FILE = "$INSTALL_DIR\config.yaml"

Write-Host "========================================" -ForegroundColor Blue
Write-Host "  Video Summary Skill 安装程序" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# 检查依赖
Write-Host "[1/6] 检查依赖..." -ForegroundColor Yellow

# 检查 Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python 未安装，请先安装 Python 3.9+" -ForegroundColor Red
    Write-Host "   下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 检查 yt-dlp
try {
    $ytdlpVersion = yt-dlp --version 2>&1
    Write-Host "   ✓ yt-dlp $ytdlpVersion" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ yt-dlp 未安装，正在安装..." -ForegroundColor Yellow
    pip install yt-dlp
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ yt-dlp 安装失败" -ForegroundColor Red
        exit 1
    }
    Write-Host "   ✓ yt-dlp 已安装" -ForegroundColor Green
}

# 检查 Claude Code
try {
    $claudeVersion = claude --version 2>&1
    Write-Host "   ✓ Claude Code 已安装" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ Claude Code 未安装" -ForegroundColor Yellow
    Write-Host "   请访问 https://claude.ai/download 安装 Claude Code" -ForegroundColor Yellow
}

# 获取脚本所在目录
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# 创建安装目录
Write-Host "[2/6] 创建安装目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $INSTALL_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $SKILL_DIR | Out-Null

# 复制工具文件
Write-Host "[3/6] 复制工具文件..." -ForegroundColor Yellow
Copy-Item -Path "$SCRIPT_DIR\tools" -Destination $INSTALL_DIR -Recurse -Force
Write-Host "   ✓ 工具已复制到 $INSTALL_DIR\tools\" -ForegroundColor Green

# 安装 Python 依赖
Write-Host "[4/6] 安装 Python 依赖..." -ForegroundColor Yellow
pip install -q -r "$INSTALL_DIR\tools\requirements.txt"
Write-Host "   ✓ Python 依赖已安装" -ForegroundColor Green

# 生成配置文件
Write-Host "[5/6] 配置设置..." -ForegroundColor Yellow

$createConfig = $true
if (Test-Path $CONFIG_FILE) {
    Write-Host "   配置文件已存在: $CONFIG_FILE" -ForegroundColor Yellow
    $response = Read-Host "   是否覆盖? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "   ✓ 保留现有配置" -ForegroundColor Green
        $createConfig = $false
    }
}

if ($createConfig) {
    Write-Host ""
    Write-Host "请配置以下选项：" -ForegroundColor Blue
    Write-Host ""

    # 询问输出目录
    $OUTPUT_DIR = Read-Host "视频总结保存目录 [默认: ~/Documents/video-summaries]"
    if ([string]::IsNullOrWhiteSpace($OUTPUT_DIR)) {
        $OUTPUT_DIR = "~/Documents/video-summaries"
    }

    # 询问 B站 cookies
    Write-Host ""
    Write-Host "B站视频需要登录才能获取字幕。"
    $COOKIES_FILE = Read-Host "B站 cookies 文件路径 (可选，留空跳过)"

    # 生成配置文件
    $configContent = @"
# Video Summary Skill 配置文件

# 输出目录（字幕、总结和临时文件）
output_dir: $OUTPUT_DIR

# B站 cookies 文件路径（可选，用于下载需要登录的视频字幕）
cookies_file: "$COOKIES_FILE"
"@

    Set-Content -Path $CONFIG_FILE -Value $configContent -Encoding UTF8
    Write-Host "   ✓ 配置文件已生成: $CONFIG_FILE" -ForegroundColor Green
}

# 生成 SKILL.md
Write-Host "[6/6] 安装 Claude Code Skill..." -ForegroundColor Yellow

$TOOLS_DIR = "$INSTALL_DIR\tools"
$templateContent = Get-Content -Path "$SCRIPT_DIR\skill\SKILL.md.template" -Raw
$skillContent = $templateContent -replace '\{\{TOOLS_DIR\}\}', $TOOLS_DIR
Set-Content -Path "$SKILL_DIR\SKILL.md" -Value $skillContent -Encoding UTF8
Write-Host "   ✓ Skill 已安装到 $SKILL_DIR\" -ForegroundColor Green

# 完成
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ 安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "接下来请配置 API Key："
Write-Host ""
Write-Host "设置环境变量：" -ForegroundColor Blue
Write-Host '  [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-xxx", "User")'
Write-Host ""
Write-Host "使用代理服务（可选）：" -ForegroundColor Blue
Write-Host '  [Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "https://your-proxy.com", "User")'
Write-Host ""
Write-Host "使用方法：" -ForegroundColor Blue
Write-Host "  在 Claude Code 中输入："
Write-Host "  /video-summary https://youtube.com/watch?v=xxx" -ForegroundColor Green
Write-Host ""
Write-Host "配置文件位置: $CONFIG_FILE"
Write-Host "工具目录: $TOOLS_DIR"
Write-Host ""
