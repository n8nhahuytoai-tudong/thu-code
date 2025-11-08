@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   VIDEO TO JSON CONVERTER
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chưa được cài đặt!
    echo Vui lòng tải Python tại: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Kiểm tra và cài đặt opencv-python nếu cần
echo [1/4] Kiểm tra thư viện Python...
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo [!] OpenCV chưa được cài đặt. Đang cài đặt...
    python -m pip install --upgrade pip
    python -m pip install opencv-python
    if errorlevel 1 (
        echo [ERROR] Không thể cài đặt opencv-python!
        pause
        exit /b 1
    )
    echo [OK] Đã cài đặt opencv-python thành công!
) else (
    echo [OK] OpenCV đã sẵn sàng!
)

echo.
echo [2/4] Chọn file video...
echo.

REM Tạo script VBS để mở hộp thoại chọn file
echo Set objDialog = CreateObject("WScript.Shell").Exec("mshta.exe ""about:<input type=file id=FILE><script>FILE.click();new ActiveXObject('Scripting.FileSystemObject').GetStandardStream(1).WriteLine(FILE.value);close();resizeTo(0,0);</script>""") > "%temp%\selectfile.vbs"
echo WScript.Echo objDialog.StdOut.ReadLine() >> "%temp%\selectfile.vbs"

REM Chạy VBS và lấy đường dẫn file
for /f "delims=" %%i in ('cscript //nologo "%temp%\selectfile.vbs"') do set "VIDEO_PATH=%%i"

REM Xóa file VBS tạm
del "%temp%\selectfile.vbs" >nul 2>&1

REM Kiểm tra xem người dùng có chọn file không
if "%VIDEO_PATH%"=="" (
    echo [!] Không có file nào được chọn!
    pause
    exit /b 1
)

if not exist "%VIDEO_PATH%" (
    echo [ERROR] File không tồn tại: %VIDEO_PATH%
    pause
    exit /b 1
)

echo [OK] File đã chọn: %VIDEO_PATH%
echo.

REM Lấy thư mục chứa file video
for %%F in ("%VIDEO_PATH%") do set "VIDEO_DIR=%%~dpF"
for %%F in ("%VIDEO_PATH%") do set "VIDEO_NAME=%%~nF"

REM Tạo tên file output
set "OUTPUT_FILE=%VIDEO_DIR%%VIDEO_NAME%_info.json"

echo [3/4] Tùy chọn xử lý
echo.
echo Bạn có muốn extract frames từ video không?
echo   1 - Có (extract frames, file JSON sẽ lớn hơn)
echo   2 - Không (chỉ lấy metadata, file JSON nhỏ)
echo.
set /p "EXTRACT_CHOICE=Chọn (1 hoặc 2): "

if "%EXTRACT_CHOICE%"=="2" (
    set "EXTRACT_PARAM=--no-frames"
    echo [OK] Chỉ extract metadata
) else (
    set "EXTRACT_PARAM="
    echo [OK] Sẽ extract frames
    echo.
    set /p "FRAME_INTERVAL=Khoảng cách giữa các frames (mặc định 30): "
    if "!FRAME_INTERVAL!"=="" set "FRAME_INTERVAL=30"
    set /p "MAX_FRAMES=Số frame tối đa (mặc định 10): "
    if "!MAX_FRAMES!"=="" set "MAX_FRAMES=10"
    set "EXTRACT_PARAM=--interval !FRAME_INTERVAL! --max-frames !MAX_FRAMES!"
)

echo.
echo [4/4] Đang xử lý video...
echo ========================================

REM Chạy script Python
python "%~dp0video_to_json.py" "%VIDEO_PATH%" %EXTRACT_PARAM% --output "%OUTPUT_FILE%"

if errorlevel 1 (
    echo.
    echo [ERROR] Có lỗi xảy ra khi xử lý video!
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Hoàn thành!
echo.
echo File JSON đã được lưu tại:
echo %OUTPUT_FILE%
echo.

REM Hỏi có muốn mở file JSON không
set /p "OPEN_CHOICE=Bạn có muốn mở file JSON không? (y/n): "
if /i "%OPEN_CHOICE%"=="y" (
    start "" "%OUTPUT_FILE%"
)

REM Hỏi có muốn mở thư mục chứa file không
set /p "FOLDER_CHOICE=Bạn có muốn mở thư mục chứa file không? (y/n): "
if /i "%FOLDER_CHOICE%"=="y" (
    explorer "%VIDEO_DIR%"
)

echo.
echo Nhấn phím bất kỳ để thoát...
pause >nul
