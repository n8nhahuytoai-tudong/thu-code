@echo off
echo ========================================
echo    VIDEO ANALYZER - Installation
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

REM Install dependencies
echo Installing dependencies...
cd ..
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

cd video_analyzer
echo.
echo ========================================
echo [SUCCESS] Installation completed!
echo ========================================
echo.

REM Setup .env
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo [NOTE] Please edit .env and add your ANTHROPIC_API_KEY
    echo        Get your key at: https://console.anthropic.com/
) else (
    echo .env file already exists
)

echo.
echo Quick start:
echo   start.bat               (menu mode)
echo   run.bat video.mp4       (quick run)
echo.
pause
