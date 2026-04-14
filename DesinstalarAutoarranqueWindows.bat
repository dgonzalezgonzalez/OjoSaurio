@echo off
setlocal

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\uninstall_autostart_windows.ps1"

echo.
echo Si ves "Autostart disabled on Windows.", quedo desinstalado.
pause

endlocal
