@echo off
setlocal

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\install_autostart_windows.ps1"

echo.
echo Si ves "Autostart enabled on Windows.", quedo instalado.
pause

endlocal
