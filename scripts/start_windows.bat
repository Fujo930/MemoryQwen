@echo off
setlocal enabledelayedexpansion
echo ============================================
echo   MemoryQwen v0.1 - Developer Preview
echo ============================================
echo.

cd /d %~dp0..

echo Checking environment...
echo.
python -m src.cli health

echo.
echo ============================================
echo Type a message and press Enter to chat.
echo Type /exit to quit.
echo ============================================
echo.

:loop
set "MSG="
set /p "MSG=You > "
if not defined MSG goto loop
if /i "!MSG!"=="/exit" goto end

echo.
python -m src.cli chat "!MSG!" --session cli-chat
echo.
goto loop

:end
echo.
echo Bye!
pause
