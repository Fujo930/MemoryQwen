@echo off
chcp 65001 >nul
title MemoryQwen

echo ========================================
echo    MemoryQwen v0.1.0 — 启动中...
echo ========================================
echo.

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请安装 Python 3.11+
    pause
    exit /b 1
)

:: 检查 Python 版本
python -c "import sys; v=sys.version_info; assert v.major==3 and v.minor>=10, '需要 Python 3.10+'"
if %errorlevel% neq 0 (
    echo [错误] 需要 Python 3.10+
    pause
    exit /b 1
)

:: 虚拟环境
if not exist ".venv\" (
    echo [信息] 创建虚拟环境...
    python -m venv .venv
)

echo [信息] 激活虚拟环境...
call .venv\Scripts\activate.bat

:: 安装依赖
echo [信息] 检查依赖...
pip install -q -r requirements.txt 2>nul

:: 启动
echo.
echo ========================================
echo    启动服务: http://localhost:7860
echo ========================================
echo.

python -m src

if %errorlevel% neq 0 (
    echo.
    echo [错误] 服务异常退出，错误码: %errorlevel%
    pause
)

call .venv\Scripts\deactivate.bat
