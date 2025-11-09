@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

:MENU
cls
echo ======================================================================
echo     YOUTUBE TO SORA 2 - ADVANCED PROMPT GENERATOR (MENU)
echo ======================================================================
echo.
echo 1. Chạy phân tích video (Interactive Mode)
echo 2. Chạy phân tích nhanh (Không audio, dùng cache)
echo 3. Chạy phân tích đầy đủ (Có audio, không cache)
echo 4. Xem kết quả gần nhất
echo 5. Xóa cache
echo 6. Kiểm tra cài đặt
echo 7. Set API Key
echo 8. Hướng dẫn sử dụng
echo 9. Thoát
echo.
set /p choice="Chọn chức năng (1-9): "

if "%choice%"=="1" goto INTERACTIVE
if "%choice%"=="2" goto QUICK
if "%choice%"=="3" goto FULL
if "%choice%"=="4" goto VIEW_RESULTS
if "%choice%"=="5" goto CLEAR_CACHE
if "%choice%"=="6" goto CHECK_SETUP
if "%choice%"=="7" goto SET_API_KEY
if "%choice%"=="8" goto HELP
if "%choice%"=="9" goto EXIT

echo Lựa chọn không hợp lệ!
timeout /t 2 >nul
goto MENU

:INTERACTIVE
cls
echo ======================================================================
echo                    CHẠY INTERACTIVE MODE
echo ======================================================================
echo.
python youtube_to_sora_advanced.py
echo.
pause
goto MENU

:QUICK
cls
echo ======================================================================
echo              CHẠY PHÂN TÍCH NHANH (Không audio)
echo ======================================================================
echo.
set /p url="Nhập YouTube URL: "
echo.
echo Đang phân tích (không audio, dùng cache)...
python -c "from youtube_to_sora_advanced import AdvancedYouTubeToSoraPrompt; p = AdvancedYouTubeToSoraPrompt(); p.process('%url%', use_cache=True, analyze_audio=False)"
echo.
pause
goto MENU

:FULL
cls
echo ======================================================================
echo           CHẠY PHÂN TÍCH ĐẦY ĐỦ (Có audio, không cache)
echo ======================================================================
echo.
set /p url="Nhập YouTube URL: "
echo.
echo Đang phân tích đầy đủ (có audio, không dùng cache cũ)...
python -c "from youtube_to_sora_advanced import AdvancedYouTubeToSoraPrompt; p = AdvancedYouTubeToSoraPrompt(); p.process('%url%', use_cache=False, analyze_audio=True)"
echo.
pause
goto MENU

:VIEW_RESULTS
cls
echo ======================================================================
echo                    KẾT QUẢ GẦN NHẤT
echo ======================================================================
echo.
if not exist "output_results" (
    echo Chưa có kết quả nào!
    echo.
    pause
    goto MENU
)

echo Các file kết quả:
echo.
dir /B /O-D output_results\*.txt 2>nul
if errorlevel 1 (
    echo Không tìm thấy file kết quả!
) else (
    echo.
    set /p open_file="Mở file txt mới nhất? (y/n): "
    if /i "!open_file!"=="y" (
        for /f "delims=" %%i in ('dir /B /O-D output_results\*.txt') do (
            start notepad "output_results\%%i"
            goto MENU_RETURN
        )
    )
)
:MENU_RETURN
echo.
pause
goto MENU

:CLEAR_CACHE
cls
echo ======================================================================
echo                        XÓA CACHE
echo ======================================================================
echo.
if not exist "cache" (
    echo Không có cache để xóa!
    echo.
    pause
    goto MENU
)

set /p confirm="Bạn có chắc muốn xóa cache? (y/n): "
if /i "%confirm%"=="y" (
    rmdir /S /Q cache 2>nul
    mkdir cache
    echo ✓ Đã xóa cache!
) else (
    echo Đã hủy.
)
echo.
pause
goto MENU

:CHECK_SETUP
cls
echo ======================================================================
echo                    KIỂM TRA CÀI ĐẶT
echo ======================================================================
echo.

echo [Python]
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python chưa cài đặt
) else (
    echo ✓ OK
)
echo.

echo [pip packages]
python -c "import openai; print('✓ openai OK')" 2>nul || echo ❌ openai chưa cài
python -c "import cv2; print('✓ opencv-python OK')" 2>nul || echo ❌ opencv-python chưa cài
python -c "import numpy; print('✓ numpy OK')" 2>nul || echo ❌ numpy chưa cài
python -c "import yt_dlp; print('✓ yt-dlp OK')" 2>nul || echo ❌ yt-dlp chưa cài
python -c "import docx; print('✓ python-docx OK')" 2>nul || echo ❌ python-docx chưa cài
echo.

echo [ffmpeg]
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ❌ ffmpeg chưa cài đặt (cần cho audio analysis)
) else (
    echo ✓ ffmpeg OK
)
echo.

echo [OpenAI API Key]
if "%OPENAI_API_KEY%"=="" (
    if exist ".env" (
        echo ✓ API Key trong file .env
    ) else (
        echo ❌ API Key chưa được set
    )
) else (
    echo ✓ API Key đã set trong biến môi trường
)
echo.

echo [Folders]
if exist "output_results" (echo ✓ output_results OK) else (echo ⚠ output_results chưa tạo)
if exist "cache" (echo ✓ cache OK) else (echo ⚠ cache chưa tạo)
echo.

pause
goto MENU

:SET_API_KEY
cls
echo ======================================================================
echo                      SET API KEY
echo ======================================================================
echo.
echo Lấy API Key tại: https://platform.openai.com/api-keys
echo.
set /p new_key="Nhập OpenAI API Key: "

if "%new_key%"=="" (
    echo Không có API key nào được nhập!
) else (
    echo OPENAI_API_KEY=%new_key% > .env
    set OPENAI_API_KEY=%new_key%
    echo.
    echo ✓ API Key đã được lưu vào file .env
    echo Script sẽ tự động load từ file này
)
echo.
pause
goto MENU

:HELP
cls
echo ======================================================================
echo                      HƯỚNG DẪN SỬ DỤNG
echo ======================================================================
echo.
echo CÁC CHỨC NĂNG:
echo.
echo 1. Interactive Mode: Chạy script và nhập thông tin theo hướng dẫn
echo 2. Phân tích nhanh: Nhanh hơn, không phân tích audio
echo 3. Phân tích đầy đủ: Chậm hơn nhưng chi tiết nhất (có audio)
echo 4. Xem kết quả: Mở file kết quả mới nhất
echo 5. Xóa cache: Xóa kết quả phân tích cũ (để phân tích lại)
echo 6. Kiểm tra: Xem các thành phần đã cài đặt đúng chưa
echo 7. Set API Key: Cấu hình OpenAI API Key
echo.
echo KẾT QUẢ OUTPUT:
echo - File .txt: Report dễ đọc
echo - File .json: Data cho developers
echo - File .docx: Word document
echo.
echo CHI PHÍ DỰ TÍNH (video 5 phút):
echo - Với audio: ~$1.00
echo - Không audio: ~$0.95
echo - Từ cache: $0.00
echo.
echo Xem thêm trong file: HUONG_DAN_CHAY.md
echo.
pause
goto MENU

:EXIT
cls
echo.
echo Cảm ơn bạn đã sử dụng YouTube to Sora 2 Analyzer!
echo.
timeout /t 2 >nul
exit /b 0
