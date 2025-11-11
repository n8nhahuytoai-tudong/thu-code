@echo off
chcp 65001 >nul
title YouTube Scene Analyzer - Installer
color 0E

echo.
echo ================================================================
echo      YOUTUBE SCENE ANALYZER - AUTO INSTALLER
echo      Installing all dependencies automatically
echo ================================================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python not installed!
    echo.
    echo Please download and install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
echo [OK] Python installed
echo.

echo [2/4] Checking pip...
pip --version
if errorlevel 1 (
    echo [ERROR] pip not found!
    pause
    exit /b 1
)
echo [OK] pip ready
echo.

echo [3/4] Installing Python packages...
echo Installing: opencv-python, numpy, openai, yt-dlp
echo (This may take 2-5 minutes depending on internet speed)
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed!
    echo.
    echo Try manual installation:
    echo   pip install opencv-python numpy openai yt-dlp
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Packages installed successfully!
echo.

echo [4/4] Checking installation...
python test_installation.py

echo.
echo ================================================================
echo [INFO] API Key Setup Required
echo ================================================================
echo.

if exist ".env" (
    echo [OK] .env file already exists
) else (
    echo .env file not found. You can:
    echo   1. Create .env file with: OPENAI_API_KEY=sk-your-key
    echo   2. Or enter API key when running the script
    echo.
    echo Get API key from: https://platform.openai.com/api-keys
    echo.

    set /p CREATE_ENV="Create .env file now? (Y/N): "
    if /i "%CREATE_ENV%"=="Y" (
        echo.
        set /p API_KEY="Enter your OpenAI API Key: "
        if not "!API_KEY!"=="" (
            echo OPENAI_API_KEY=!API_KEY!>.env
            echo.
            echo [OK] Created .env file
        )
    )
)

echo.
echo ================================================================
echo INSTALLATION COMPLETE!
echo ================================================================
echo.
echo You can now run the analyzer by:
echo   - Run RUN.bat (interactive mode)
echo   - Drag video/URL to DRAG_VIDEO_HERE.bat
echo   - Or: python youtube_scene_by_scene_analyzer.py
echo.
echo.
pause
