$ErrorActionPreference = "Stop"

$startupDir = [Environment]::GetFolderPath("Startup")
$shortcutPath = Join-Path $startupDir "OjoSaurio.lnk"

if (Test-Path $shortcutPath) {
  Remove-Item $shortcutPath -Force
}

Write-Host "Autostart disabled on Windows."
