@echo off
chcp 65001 >nul
title YouTube Scene Analyzer - Installer
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║           YOUTUBE SCENE ANALYZER - AUTO INSTALLER             ║
echo ║           Cài đặt tự động tất cả dependencies                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Kiểm tra Python...
python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python chưa được cài đặt!
    echo.
    echo Vui lòng tải và cài Python 3.8+ từ:
    echo https://www.python.org/downloads/
    echo.
    echo QUAN TRỌNG: Nhớ tick "Add Python to PATH" khi cài!
    echo.
    pause
    exit /b 1
)
echo [OK] Python đã cài
echo.

echo [2/4] Kiểm tra pip...
pip --version
if errorlevel 1 (
    echo [ERROR] pip không tìm thấy!
    pause
    exit /b 1
)
echo [OK] pip sẵn sàng
echo.

echo [3/4] Cài đặt Python packages...
echo Đang cài đặt: opencv-python, numpy, openai, yt-dlp
echo (Có thể mất 2-5 phút tùy tốc độ mạng)
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Cài đặt thất bại!
    echo.
    echo Thử cài thủ công:
    echo   pip install opencv-python numpy openai yt-dlp
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Packages đã cài xong!
echo.

echo [4/4] Kiểm tra cài đặt...
python test_installation.py

echo.
echo ════════════════════════════════════════════════════════════════
echo [INFO] Cần thiết lập API Key
echo ════════════════════════════════════════════════════════════════
echo.

if exist ".env" (
    echo [OK] File .env đã tồn tại
) else (
    echo File .env chưa có. Bạn có thể:
    echo   1. Tạo file .env với nội dung: OPENAI_API_KEY=sk-your-key
    echo   2. Hoặc nhập API key khi chạy script
    echo.
    echo Lấy API key tại: https://platform.openai.com/api-keys
    echo.

    set /p CREATE_ENV="Tạo file .env ngay bây giờ? (Y/N): "
    if /i "%CREATE_ENV%"=="Y" (
        echo.
        set /p API_KEY="Nhập OpenAI API Key của bạn: "
        if not "!API_KEY!"=="" (
            echo OPENAI_API_KEY=!API_KEY!>.env
            echo.
            echo [OK] Đã tạo file .env
        )
    )
)

echo.
echo ════════════════════════════════════════════════════════════════
echo ✓ CÀI ĐẶT HOÀN TẤT!
echo ════════════════════════════════════════════════════════════════
echo.
echo Bạn có thể chạy analyzer bằng:
echo   - Chạy RUN.bat (giao diện nhập URL)
echo   - Kéo thả URL/video vào DRAG_VIDEO_HERE.bat
echo   - Hoặc: python youtube_scene_by_scene_analyzer.py
echo.
echo.
pause
