@echo off
echo ========================================
echo    VIDEO ANALYZER - Quick Run
echo ========================================
echo.

REM Check if input provided
if "%~1"=="" (
    echo Usage: run.bat [video_path_or_url] [options]
    echo.
    echo Examples:
    echo   run.bat video.mp4
    echo   run.bat https://youtube.com/watch?v=xxx
    echo   run.bat video.mp4 --no-ai
    echo   run.bat video.mp4 --threshold 30
    echo.
    pause
    exit /b 1
)

REM Detect if input is URL or file
echo %1 | findstr /i "http https youtube youtu.be vimeo" >nul
if %errorlevel%==0 (
    echo Detected URL, downloading...
    python video_analyzer.py --url %*
) else (
    echo Detected local file
    python video_analyzer.py --input %*
)

echo.
echo ========================================
pause
