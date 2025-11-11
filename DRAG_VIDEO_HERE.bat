@echo off
chcp 65001 >nul
title YouTube Scene Analyzer - Drag & Drop Mode
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     KÉO THẢ VIDEO/URL VÀO ĐÂY ĐỂ PHÂN TÍCH                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if file/URL was dragged
if "%~1"=="" (
    echo [ERROR] Bạn chưa kéo thả file hoặc URL vào đây!
    echo.
    echo HƯỚNG DẪN:
    echo   1. Kéo file video (.mp4) vào icon file .bat này
    echo   2. Hoặc tạo shortcut với URL làm argument
    echo   3. Hoặc chạy RUN.bat để nhập URL thủ công
    echo.
    pause
    exit /b 1
)

set VIDEO_INPUT=%~1

echo [INFO] Đang xử lý: %VIDEO_INPUT%
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chưa cài đặt!
    pause
    exit /b 1
)

REM Check .env
if not exist ".env" (
    echo [WARNING] Chưa có file .env!
    echo.
    set /p API_KEY="Nhập OpenAI API Key: "
    if not "!API_KEY!"=="" (
        echo OPENAI_API_KEY=!API_KEY!>.env
        echo [OK] Đã tạo .env
        echo.
    )
)

echo ════════════════════════════════════════════════════════════════
echo [START] Bắt đầu phân tích...
echo ════════════════════════════════════════════════════════════════
echo.

python youtube_scene_by_scene_analyzer.py "%VIDEO_INPUT%"

echo.
echo ════════════════════════════════════════════════════════════════
echo [DONE] Hoàn tất!
echo ════════════════════════════════════════════════════════════════
echo.

REM Auto open output folder
if exist "output_scenes" (
    echo Đang mở thư mục kết quả...
    start "" "output_scenes"
)

echo.
pause
