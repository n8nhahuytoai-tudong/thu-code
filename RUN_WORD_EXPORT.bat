@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title YouTube to Word Prompts Exporter
color 0C

echo.
echo ================================================================
echo      YOUTUBE TO WORD - SORA PROMPTS EXPORTER
echo      Moi canh = 1 dong prompt sieu chi tiet
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    pause
    exit /b 1
)

echo [OK] Python installed
echo.

REM Check python-docx
echo Checking python-docx package...
python -c "import docx" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] python-docx not installed!
    echo.
    echo Word export requires python-docx package.
    echo.
    set /p "INSTALL=Install python-docx now? (Y/N): "
    if /i "!INSTALL!"=="Y" (
        echo Installing python-docx...
        pip install python-docx
        echo.
    ) else (
        echo.
        echo Cannot continue without python-docx.
        echo Install manually: pip install python-docx
        pause
        exit /b 1
    )
)

echo [OK] python-docx ready
echo.

REM Check .env
if not exist ".env" (
    echo [WARNING] No .env file!
    echo.
    set /p "API_KEY=Enter OpenAI API Key: "
    if not "!API_KEY!"=="" (
        echo OPENAI_API_KEY=!API_KEY!>.env
        echo [OK] Created .env
        echo.
    )
)

echo ================================================================
echo.
echo Enter YouTube URL to analyze:
echo (Each scene will be one detailed prompt line in Word)
echo.
echo ================================================================
echo.

set /p "VIDEO_INPUT=YouTube URL: "

set "VIDEO_INPUT=%VIDEO_INPUT:"=%"

if "%VIDEO_INPUT%"=="" (
    echo [ERROR] No URL provided!
    pause
    exit /b 1
)

echo.
echo ================================================================
echo [START] Processing: %VIDEO_INPUT%
echo ================================================================
echo.

python youtube_to_word_prompts.py "%VIDEO_INPUT%"

echo.
echo ================================================================
echo [DONE] Complete!
echo ================================================================
echo.

REM Try to open output folder
if exist "output_scenes" (
    echo Opening output folder...
    start "" "output_scenes"
)

echo.
pause
