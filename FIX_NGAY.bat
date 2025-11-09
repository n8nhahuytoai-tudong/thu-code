@echo off
chcp 65001 >nul
cls

echo ======================================================================
echo                    FIX NGAY - XÓA CACHE LỖI
echo ======================================================================
echo.
echo Script này sẽ:
echo   1. Xóa cache cũ (chứa dữ liệu lỗi)
echo   2. Sẵn sàng chạy lại phân tích
echo.
echo ======================================================================
echo.

echo Đang xóa cache cũ...

REM Xóa cache
if exist "cache" (
    rmdir /S /Q cache 2>nul
    echo ✓ Đã xóa folder cache
) else (
    echo - Không có folder cache
)

REM Tạo lại folder cache rỗng
mkdir cache 2>nul
echo ✓ Đã tạo cache mới

REM Xóa temp files
if exist "temp_video.mp4" del /Q temp_video.mp4 2>nul
if exist "temp_audio.m4a" del /Q temp_audio.m4a 2>nul
if exist "temp_frames" rmdir /S /Q temp_frames 2>nul
echo ✓ Đã xóa files tạm

echo.
echo ======================================================================
echo                         HOÀN TẤT!
echo ======================================================================
echo.
echo Cache đã được xóa sạch.
echo.
echo BÂY GIỜ CHẠY LẠI:
echo   → Double-click: run_youtube_to_sora.bat
echo   → Hoặc: run_advanced.bat
echo.
echo Lần này sẽ phân tích lại hoàn toàn (không dùng cache cũ).
echo.

pause
