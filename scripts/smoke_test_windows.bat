@echo off
echo ============================================
echo   MemoryQwen v0.1 Smoke Test
echo ============================================
cd /d %~dp0..

echo [1/5] Health Check
python -m src.cli health
echo.

echo [2/5] Memory Stats
python -m src.cli memory stats
echo.

echo [3/5] Guardian Status
python -m src.cli guardian status
echo.

echo [4/5] Task List
python -m src.cli task list
echo.

echo [5/5] Profile Show
python -m src.cli profile show
echo.

echo ============================================
echo   Smoke Test Complete
echo ============================================
pause
