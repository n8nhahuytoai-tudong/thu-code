@echo off
chcp 65001 >nul
title ComfyUI VPS - Kết nối
color 0B

:menu
cls
echo ╔════════════════════════════════════════╗
echo ║     COMFYUI VPS - VAST.AI              ║
echo ╚════════════════════════════════════════╝
echo.
echo [1] Kết nối VPS
echo [2] Mở ComfyUI (sau khi kết nối)
echo [3] Kiểm tra kết nối
echo [4] Thoát
echo.
set /p choice="Chọn (1-4): "

if "%choice%"=="1" goto connect
if "%choice%"=="2" goto open_browser
if "%choice%"=="3" goto check
if "%choice%"=="4" exit
goto menu

:connect
cls
echo ====================================
echo   Đang kết nối VPS...
echo ====================================
echo.
echo Sau khi kết nối, chọn [2] để mở ComfyUI
echo Hoặc vào trình duyệt: http://localhost:8188
echo.
echo ====================================
echo.

REM ═══════════════════════════════════════════════════════════
REM  Thông tin SSH đã được cập nhật
REM  Port: 56254
REM  Host: 115.231.176.132
REM ═══════════════════════════════════════════════════════════

ssh -p 56254 root@115.231.176.132 -L 8080:localhost:8080 -L 8188:localhost:8188

REM ═══════════════════════════════════════════════════════════

echo.
echo Kết nối đã ngắt.
pause
goto menu

:open_browser
echo Đang mở ComfyUI trong trình duyệt...
start http://localhost:8188
timeout /t 2 >nul
goto menu

:check
cls
echo ====================================
echo   Kiểm tra kết nối ComfyUI...
echo ====================================
echo.
curl -s http://localhost:8188 >nul 2>&1
if %errorlevel%==0 (
    echo [✓] ComfyUI đang chạy!
    echo     Truy cập: http://localhost:8188
) else (
    echo [✗] Không kết nối được ComfyUI
    echo.
    echo Kiểm tra:
    echo   1. VPS có đang Running không?
    echo   2. Đã SSH kết nối chưa? (Chọn [1])
    echo   3. Port SSH và Host đúng chưa?
    echo.
    echo Hướng dẫn lấy thông tin SSH:
    echo   - Vào: https://cloud.vast.ai/instances/
    echo   - Click vào instance đang chạy
    echo   - Copy lệnh SSH
    echo   - Sửa file .bat này
)
echo.
pause
goto menu
