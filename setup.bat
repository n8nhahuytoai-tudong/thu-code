@echo off
chcp 65001 >nul
echo ======================================================================
echo         CÀI ĐẶT YOUTUBE TO SORA 2 - ADVANCED ANALYZER
echo ======================================================================
echo.

echo [Bước 1] Kiểm tra Python...
python --version
if errorlevel 1 (
    echo.
    echo ❌ LỖI: Python chưa được cài đặt!
    echo.
    echo Vui lòng:
    echo 1. Tải Python từ: https://www.python.org/downloads/
    echo 2. Cài đặt và NHỚ CHECK "Add Python to PATH"
    echo 3. Khởi động lại Command Prompt
    echo 4. Chạy lại file setup.bat này
    echo.
    pause
    exit /b 1
)
echo ✓ Python OK
echo.

echo [Bước 2] Cài đặt Python packages...
echo Đang cài đặt: openai, opencv-python, numpy, yt-dlp, python-docx
echo Vui lòng đợi...
echo.

python -m pip install --upgrade pip
python -m pip install openai opencv-python numpy yt-dlp python-docx

if errorlevel 1 (
    echo.
    echo ❌ Có lỗi khi cài đặt!
    echo Thử chạy lệnh này thủ công:
    echo   pip install openai opencv-python numpy yt-dlp python-docx
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ Đã cài đặt Python packages thành công!
echo.

echo [Bước 3] Kiểm tra ffmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠ CẢNH BÁO: ffmpeg chưa được cài đặt
    echo.
    echo ffmpeg cần thiết để phân tích audio/transcript.
    echo.
    echo CÁCH CÀI FFMPEG:
    echo.
    echo Tùy chọn 1 - Chocolatey (khuyến nghị):
    echo   1. Cài Chocolatey từ: https://chocolatey.org/install
    echo   2. Chạy: choco install ffmpeg
    echo.
    echo Tùy chọn 2 - Thủ công:
    echo   1. Tải từ: https://ffmpeg.org/download.html
    echo   2. Giải nén vào C:\ffmpeg
    echo   3. Thêm C:\ffmpeg\bin vào PATH
    echo.
    echo Bạn có thể bỏ qua ffmpeg và chạy script mà không phân tích audio.
    echo.
) else (
    echo ✓ ffmpeg đã được cài đặt
    echo.
)

echo [Bước 4] Cấu hình OpenAI API Key...
echo.
if "%OPENAI_API_KEY%"=="" (
    echo API Key chưa được set.
    echo.
    echo Lấy API Key tại: https://platform.openai.com/api-keys
    echo.
    set /p api_key="Nhập OpenAI API Key (hoặc Enter để bỏ qua): "

    if not "!api_key!"=="" (
        echo.
        echo Lưu API key vào file .env...
        echo OPENAI_API_KEY=!api_key! > .env
        echo ✓ API Key đã được lưu vào file .env
        echo Script sẽ tự động load từ file này
    ) else (
        echo.
        echo ⚠ Bạn cần set API key trước khi chạy:
        echo   Option 1: Tạo file .env với nội dung: OPENAI_API_KEY=sk-your-key
        echo   Option 2: Set biến môi trường: set OPENAI_API_KEY=sk-your-key
        echo   Option 3: Nhập khi chạy script
    )
) else (
    echo ✓ API Key đã được set trong biến môi trường
)

echo.
echo ======================================================================
echo                      CÀI ĐẶT HOÀN TẤT!
echo ======================================================================
echo.
echo Bạn có thể chạy script bằng cách:
echo   1. Double-click vào file: run_youtube_to_sora.bat
echo   2. Hoặc chạy: python youtube_to_sora_advanced.py
echo.

pause
