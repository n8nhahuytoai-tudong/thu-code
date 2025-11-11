@echo off
chcp 65001 >nul
title YouTube Scene Analyzer - Easy Launcher
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     YOUTUBE SCENE-BY-SCENE ANALYZER - EASY LAUNCHER           ║
echo ║     Phân tích video và tạo prompt cho từng cảnh               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chưa được cài đặt!
    echo.
    echo Vui lòng cài Python 3.8+ từ: https://www.python.org/downloads/
    echo Nhớ tick "Add Python to PATH" khi cài!
    echo.
    pause
    exit /b 1
)

echo [OK] Python đã cài đặt
echo.

REM Check if script exists
if not exist "youtube_scene_by_scene_analyzer.py" (
    echo [ERROR] Không tìm thấy file youtube_scene_by_scene_analyzer.py
    echo.
    echo Vui lòng đảm bảo file .bat và .py ở cùng thư mục!
    echo.
    pause
    exit /b 1
)

echo [OK] Script tìm thấy
echo.

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] Chưa có file .env với OpenAI API key!
    echo.
    set /p API_KEY="Nhập OpenAI API Key (hoặc Enter để bỏ qua): "

    if not "!API_KEY!"=="" (
        echo OPENAI_API_KEY=!API_KEY!>.env
        echo [OK] Đã tạo file .env
        echo.
    ) else (
        echo [INFO] Bạn sẽ cần nhập API key khi chạy script
        echo.
    )
)

REM Check if requirements are installed
echo Đang kiểm tra dependencies...
python -c "import cv2, numpy, openai" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Một số package chưa được cài đặt!
    echo.
    set /p INSTALL="Cài đặt dependencies ngay? (Y/N): "

    if /i "!INSTALL!"=="Y" (
        echo.
        echo Đang cài đặt... (có thể mất vài phút)
        pip install -r requirements.txt
        echo.
        echo [OK] Đã cài đặt xong!
        echo.
    ) else (
        echo.
        echo [INFO] Bỏ qua cài đặt. Script có thể không chạy được!
        echo.
    )
)

echo ════════════════════════════════════════════════════════════════
echo.
echo CÁCH SỬ DỤNG:
echo   1. Nhập YouTube URL (VD: https://youtube.com/watch?v=...)
echo   2. Hoặc kéo thả file video (.mp4) vào cửa sổ này
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Get YouTube URL or video file
set /p VIDEO_INPUT="Nhập YouTube URL hoặc kéo thả file video vào đây: "

REM Remove quotes if dragged
set VIDEO_INPUT=%VIDEO_INPUT:"=%

if "%VIDEO_INPUT%"=="" (
    echo.
    echo [ERROR] Bạn chưa nhập gì!
    echo.
    pause
    exit /b 1
)

echo.
echo ────────────────────────────────────────────────────────────────
echo [START] Đang xử lý: %VIDEO_INPUT%
echo ────────────────────────────────────────────────────────────────
echo.

REM Run the Python script with URL as argument
python youtube_scene_by_scene_analyzer.py "%VIDEO_INPUT%"

echo.
echo ════════════════════════════════════════════════════════════════
echo [DONE] Hoàn tất!
echo ════════════════════════════════════════════════════════════════
echo.
echo Kết quả đã được lưu trong thư mục: output_scenes\
echo.

REM Ask to open output folder
set /p OPEN_FOLDER="Mở thư mục kết quả? (Y/N): "
if /i "%OPEN_FOLDER%"=="Y" (
    start "" "output_scenes"
)

echo.
echo Nhấn phím bất kỳ để đóng cửa sổ...
pause >nul
