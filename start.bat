@echo off
echo ============================================
echo   MemoryQwen v0.1.5 — Developer Preview
echo ============================================
echo.
echo Requirements:
echo   1. Ollama running (or LM Studio with OpenAI API)
echo   2. Python 3.11+ in PATH
echo   3. pip install -r requirements.txt (done?)
echo.
echo Checking environment...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Install Python 3.11+
    pause
    exit /b 1
)

echo.
python -m src.cli health
echo.
echo ============================================
echo   Start chatting: type a message below
echo   Type /exit to quit
echo ============================================
echo.

cd /d "%~dp0"
:loop
set "MSG="
set /p "MSG=You > "
if /i "%MSG%"=="/exit" goto end
if "%MSG%"=="" goto loop
echo.
python -m src.cli chat "%MSG%" --web --session startbat
echo.
goto loop

:end
echo Bye!
pause
