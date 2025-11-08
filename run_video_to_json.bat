@echo off
chcp 65001 >nul
echo ========================================
echo   VIDEO TO JSON CONVERTER
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chưa được cài đặt!
    pause
    exit /b 1
)

REM Kiểm tra opencv-python
echo Đang kiểm tra thư viện...
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo Đang cài đặt opencv-python...
    pip install opencv-python
)

echo.
echo ========================================
echo CÁCH SỬ DỤNG:
echo.
echo 1. KÉO THẢ file video vào cửa sổ này
echo 2. Nhấn ENTER
echo.
echo Hoặc nhập đường dẫn đầy đủ đến file video
echo ========================================
echo.

set /p "VIDEO_PATH=Đường dẫn video: "

REM Xóa dấu ngoặc kép nếu có
set VIDEO_PATH=%VIDEO_PATH:"=%

if not exist "%VIDEO_PATH%" (
    echo [ERROR] File không tồn tại!
    pause
    exit /b 1
)

echo.
echo Đang xử lý...
python "%~dp0video_to_json.py" "%VIDEO_PATH%"

echo.
pause
