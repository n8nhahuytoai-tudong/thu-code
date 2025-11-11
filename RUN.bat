@echo off
chcp 65001 >nul
title YouTube Scene Analyzer
color 0A

echo.
echo ================================================================
echo      YOUTUBE SCENE ANALYZER - EASY LAUNCHER
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python installed
echo.

REM Check script
if not exist "youtube_scene_by_scene_analyzer.py" (
    echo [ERROR] Script file not found!
    echo.
    pause
    exit /b 1
)

echo [OK] Script found
echo.

REM Check .env
if not exist ".env" (
    echo [WARNING] No .env file found!
    echo.
    set /p API_KEY="Enter OpenAI API Key (or press Enter to skip): "
    if not "!API_KEY!"=="" (
        echo OPENAI_API_KEY=!API_KEY!>.env
        echo [OK] Created .env file
        echo.
    )
)

REM Check dependencies
echo Checking dependencies...
python -c "import cv2, numpy, openai" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Some packages not installed!
    echo.
    set /p INSTALL="Install dependencies now? (Y/N): "
    if /i "!INSTALL!"=="Y" (
        echo Installing...
        pip install -r requirements.txt
        echo.
        echo [OK] Installation complete!
        echo.
    )
)

echo ================================================================
echo.
echo HOW TO USE:
echo   1. Enter YouTube URL (e.g. https://youtube.com/watch?v=...)
echo   2. Or drag and drop video file into this window
echo.
echo ================================================================
echo.

set /p VIDEO_INPUT="Enter YouTube URL or drag video file here: "

REM Remove quotes
set VIDEO_INPUT=%VIDEO_INPUT:"=%

if "%VIDEO_INPUT%"=="" (
    echo.
    echo [ERROR] No input provided!
    echo.
    pause
    exit /b 1
)

echo.
echo ----------------------------------------------------------------
echo [START] Processing: %VIDEO_INPUT%
echo ----------------------------------------------------------------
echo.

python youtube_scene_by_scene_analyzer.py "%VIDEO_INPUT%"

echo.
echo ================================================================
echo [DONE] Complete!
echo ================================================================
echo.
echo Results saved in: output_scenes\
echo.

set /p OPEN_FOLDER="Open output folder? (Y/N): "
if /i "%OPEN_FOLDER%"=="Y" (
    start "" "output_scenes"
)

echo.
pause
