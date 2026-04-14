@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul
  if %ERRORLEVEL% EQU 0 (
    py -3 -m venv .venv
  ) else (
    python -m venv .venv
  )
)

".venv\Scripts\python.exe" -m pip install -e . >nul
set TWENTY20_FOCUS_SECONDS=30
set TWENTY20_BREAK_SECONDS=20
".venv\Scripts\twenty20-beeper.exe"

endlocal
