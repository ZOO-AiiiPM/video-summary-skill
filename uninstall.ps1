# Video Summary Skill 卸载脚本 (Windows)
# 用法: .\uninstall.ps1

# 安装目录
$INSTALL_DIR = "$env:USERPROFILE\.video-summary"
$SKILL_DIR = "$env:USERPROFILE\.claude\skills\video-summary"

Write-Host "========================================" -ForegroundColor Blue
Write-Host "  Video Summary Skill 卸载程序" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

Write-Host "将删除以下内容：" -ForegroundColor Yellow
Write-Host "  - 工具目录: $INSTALL_DIR"
Write-Host "  - Skill 目录: $SKILL_DIR"
Write-Host ""

$response = Read-Host "是否继续卸载? (y/N)"
if ($response -ne "y" -and $response -ne "Y") {
    Write-Host "已取消卸载" -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# 删除 Skill 目录
if (Test-Path $SKILL_DIR) {
    Remove-Item -Path $SKILL_DIR -Recurse -Force
    Write-Host "✓ 已删除 Skill 目录" -ForegroundColor Green
} else {
    Write-Host "  Skill 目录不存在，跳过" -ForegroundColor Gray
}

# 询问是否保留配置
if (Test-Path $INSTALL_DIR) {
    $response = Read-Host "是否保留配置文件和生成的总结? (Y/n)"
    if ($response -eq "n" -or $response -eq "N") {
        Remove-Item -Path $INSTALL_DIR -Recurse -Force
        Write-Host "✓ 已删除安装目录（包括配置和数据）" -ForegroundColor Green
    } else {
        # 只删除工具，保留配置
        if (Test-Path "$INSTALL_DIR\tools") {
            Remove-Item -Path "$INSTALL_DIR\tools" -Recurse -Force
        }
        Write-Host "✓ 已删除工具文件" -ForegroundColor Green
        Write-Host "  配置文件已保留: $INSTALL_DIR\config.yaml" -ForegroundColor Gray
    }
} else {
    Write-Host "  安装目录不存在，跳过" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ 卸载完成" -ForegroundColor Green
Write-Host ""
Write-Host "如需重新安装，请运行:"
Write-Host "  .\install.ps1"
Write-Host ""
