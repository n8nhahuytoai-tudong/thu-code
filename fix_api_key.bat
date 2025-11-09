@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ======================================================================
echo          QUICK FIX - CẤU HÌNH OPENAI API KEY
echo ======================================================================
echo.
echo File này sẽ giúp bạn cấu hình OpenAI API Key đúng cách.
echo.
echo Lấy API Key tại: https://platform.openai.com/api-keys
echo.

:INPUT_KEY
set /p user_api_key="Nhập OpenAI API Key của bạn: "

if "!user_api_key!"=="" (
    echo.
    echo ❌ API Key không được để trống!
    echo.
    goto INPUT_KEY
)

REM Kiểm tra format API key (phải bắt đầu bằng sk-)
echo !user_api_key! | findstr /b "sk-" >nul
if errorlevel 1 (
    echo.
    echo ⚠ Cảnh báo: API Key thường bắt đầu bằng "sk-"
    echo Bạn có chắc đây là API key đúng không?
    set /p confirm="Tiếp tục? (y/n): "
    if /i not "!confirm!"=="y" goto INPUT_KEY
)

REM Lưu vào file .env
echo OPENAI_API_KEY=!user_api_key! > .env

echo.
echo ✓ API Key đã được lưu vào file .env
echo.

REM Set cho session hiện tại
set OPENAI_API_KEY=!user_api_key!

echo ✓ API Key đã được set cho session này
echo.

REM Test API key
echo Đang kiểm tra API key...
python -c "from openai import OpenAI; client = OpenAI(); print('✓ API Key hợp lệ!')" 2>nul
if errorlevel 1 (
    echo.
    echo ⚠ Không thể verify API key
    echo Lý do có thể là:
    echo   - API key chưa đúng
    echo   - Không có internet
    echo   - Package openai chưa cài
    echo.
    echo Hãy thử chạy script và xem có lỗi gì không.
) else (
    echo ✓ API Key đã được verify thành công!
)

echo.
echo ======================================================================
echo                          HOÀN TẤT!
echo ======================================================================
echo.
echo API Key đã được cấu hình. Bạn có thể:
echo   1. Chạy run_youtube_to_sora.bat
echo   2. Hoặc chạy: python youtube_to_sora_advanced.py
echo.

pause
