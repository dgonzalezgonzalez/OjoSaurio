$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$startupDir = [Environment]::GetFolderPath("Startup")
$targetPath = Join-Path $repoRoot "OjoSaurio.bat"
$shortcutPath = Join-Path $startupDir "OjoSaurio.lnk"

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.WorkingDirectory = $repoRoot
$shortcut.WindowStyle = 1
$shortcut.Description = "OjoSaurio 20-20-20"
$shortcut.Save()

Write-Host "Autostart enabled on Windows."
