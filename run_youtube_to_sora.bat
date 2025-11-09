@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ======================================================================
echo     YOUTUBE TO SORA 2 - ADVANCED PROMPT GENERATOR
echo ======================================================================
echo.

REM Check Python installation
echo [1/5] Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python chưa được cài đặt!
    echo Tải Python tại: https://www.python.org/downloads/
    echo Nhớ check "Add Python to PATH" khi cài đặt!
    pause
    exit /b 1
)
echo ✓ Python đã cài đặt
echo.

REM Check pip
echo [2/5] Kiểm tra pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip chưa được cài đặt!
    pause
    exit /b 1
)
echo ✓ pip đã cài đặt
echo.

REM Check and install dependencies
echo [3/5] Kiểm tra các thư viện cần thiết...
echo Đang cài đặt/cập nhật packages...
python -m pip install --quiet --upgrade openai opencv-python numpy yt-dlp python-docx 2>nul
if errorlevel 1 (
    echo ⚠ Có lỗi khi cài đặt packages. Thử cài thủ công:
    echo   pip install openai opencv-python numpy yt-dlp python-docx
    echo.
) else (
    echo ✓ Các thư viện đã sẵn sàng
)
echo.

REM Check ffmpeg
echo [4/5] Kiểm tra ffmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠ ffmpeg chưa được cài đặt (cần cho phân tích audio)
    echo Tải tại: https://ffmpeg.org/download.html
    echo Hoặc bỏ qua audio analysis khi chạy script
    echo.
) else (
    echo ✓ ffmpeg đã cài đặt
    echo.
)

REM Check API Key
echo [5/5] Kiểm tra OpenAI API Key...
if "%OPENAI_API_KEY%"=="" (
    echo ⚠ OPENAI_API_KEY chưa được set
    echo.
    set /p api_key="Nhập OpenAI API Key (hoặc Enter để nhập sau): "
    if not "!api_key!"=="" (
        set OPENAI_API_KEY=!api_key!
        echo ✓ API Key đã được set cho session này
    ) else (
        echo → Bạn sẽ cần nhập API key khi chạy script
    )
) else (
    echo ✓ API Key đã được set
)
echo.

echo ======================================================================
echo                    BẮT ĐẦU PHÂN TÍCH VIDEO
echo ======================================================================
echo.

REM Run the Python script
python youtube_to_sora_advanced.py

echo.
echo ======================================================================
echo                         HOÀN TẤT!
echo ======================================================================
echo.
echo Kết quả đã được lưu trong folder: output_results\
echo.

pause
