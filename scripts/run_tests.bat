@echo off
cd /d %~dp0..
python -m pytest tests/ -q
pause
