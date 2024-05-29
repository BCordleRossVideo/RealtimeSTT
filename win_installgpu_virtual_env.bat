@echo off
cd /d %~dp0

REM Check if the venv directory exists
if not exist realtimestt.venv\Scripts\python.exe (
    echo Creating VENV
    python -m venv realtimestt.venv
) else (
    echo VENV already exists
)

echo Activating VENV
start cmd /k "call realtimestt.venv\Scripts\activate.bat && install_with_gpu_support.bat"
