@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title YouTube Scene Analyzer - Drag and Drop
color 0B

echo.
echo ================================================================
echo      DRAG VIDEO OR URL HERE TO ANALYZE
echo ================================================================
echo.

REM Check if file/URL was dragged
if "%~1"=="" (
    echo [ERROR] No file or URL provided!
    echo.
    echo HOW TO USE:
    echo   1. Drag video file (.mp4) onto this .bat icon
    echo   2. Or create shortcut with URL as parameter
    echo   3. Or run RUN.bat to enter URL manually
    echo.
    pause
    exit /b 1
)

set "VIDEO_INPUT=%~1"

echo [INFO] Processing: %VIDEO_INPUT%
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    pause
    exit /b 1
)

REM Check .env
if not exist ".env" (
    echo [WARNING] No .env file!
    echo.
    set /p "API_KEY=Enter OpenAI API Key: "
    if not "!API_KEY!"=="" (
        echo OPENAI_API_KEY=!API_KEY!>.env
        echo [OK] Created .env file
        echo.
    )
)

echo ================================================================
echo [START] Starting analysis...
echo ================================================================
echo.

python youtube_scene_by_scene_analyzer.py "%VIDEO_INPUT%"

echo.
echo ================================================================
echo [DONE] Complete!
echo ================================================================
echo.

REM Auto open output folder
if exist "output_scenes" (
    echo Opening output folder...
    start "" "output_scenes"
)

echo.
pause
