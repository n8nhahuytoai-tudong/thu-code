@echo off
chcp 65001 >nul
title Download File Từ VPS
color 0B

:menu
cls
echo ╔════════════════════════════════════════╗
echo ║     DOWNLOAD FILE TỪ VPS               ║
echo ╚════════════════════════════════════════╝
echo.
echo VPS: 47.74.34.39:56254
echo.
echo [1] Download 1 file
echo [2] Download cả thư mục
echo [3] Download từ output ComfyUI
echo [4] Liệt kê file trên VPS
echo [5] Thoát
echo.
set /p choice="Chọn (1-5): "

if "%choice%"=="1" goto download_file
if "%choice%"=="2" goto download_folder
if "%choice%"=="3" goto download_output
if "%choice%"=="4" goto list_files
if "%choice%"=="5" exit
goto menu

:download_file
cls
echo ════════════════════════════════════════
echo   DOWNLOAD FILE
echo ════════════════════════════════════════
echo.
echo Ví dụ đường dẫn:
echo   /workspace/output.mp4
echo   /workspace/ComfyUI/output/image.png
echo.
set /p remote_path="Đường dẫn file trên VPS: "

set /p local_path="Lưu vào đâu trên máy (mặc định Desktop): "
if "%local_path%"=="" set local_path=%USERPROFILE%\Desktop\

echo.
echo Đang download...
echo Từ: %remote_path%
echo Đến: %local_path%
echo.

scp -P 56254 root@47.74.34.39:%remote_path% "%local_path%"

echo.
if %errorlevel%==0 (
    echo [✓] Download thành công!
    echo File đã lưu tại: %local_path%
) else (
    echo [✗] Download thất bại!
    echo Kiểm tra:
    echo   1. Đường dẫn file đúng chưa?
    echo   2. VPS có đang chạy không?
)
echo.
pause
goto menu

:download_folder
cls
echo ════════════════════════════════════════
echo   DOWNLOAD THƯ MỤC
echo ════════════════════════════════════════
echo.
echo Ví dụ:
echo   /workspace/ComfyUI/output
echo   /workspace/my_folder
echo.
set /p remote_path="Đường dẫn thư mục trên VPS: "

set /p local_path="Lưu vào đâu trên máy (mặc định Desktop): "
if "%local_path%"=="" set local_path=%USERPROFILE%\Desktop\

echo.
echo Đang download thư mục...
echo Từ: %remote_path%
echo Đến: %local_path%
echo.

scp -P 56254 -r root@47.74.34.39:%remote_path% "%local_path%"

echo.
if %errorlevel%==0 (
    echo [✓] Download thành công!
    echo Thư mục đã lưu tại: %local_path%
) else (
    echo [✗] Download thất bại!
)
echo.
pause
goto menu

:download_output
cls
echo ════════════════════════════════════════
echo   DOWNLOAD OUTPUT COMFYUI
echo ════════════════════════════════════════
echo.
echo Liệt kê file trong /workspace/ComfyUI/output/:
echo.

ssh -p 56254 root@47.74.34.39 "ls -lh /workspace/ComfyUI/output/ 2>/dev/null || echo 'Thư mục không tồn tại'"

echo.
echo ════════════════════════════════════════
echo.
set /p filename="Nhập tên file cần download (hoặc * để tải tất cả): "

if "%filename%"=="*" (
    set remote_path=/workspace/ComfyUI/output/
    set is_folder=1
) else (
    set remote_path=/workspace/ComfyUI/output/%filename%
    set is_folder=0
)

set /p local_path="Lưu vào đâu (mặc định Desktop): "
if "%local_path%"=="" set local_path=%USERPROFILE%\Desktop\

echo.
echo Đang download...

if "%is_folder%"=="1" (
    scp -P 56254 -r root@47.74.34.39:%remote_path% "%local_path%"
) else (
    scp -P 56254 root@47.74.34.39:%remote_path% "%local_path%"
)

echo.
if %errorlevel%==0 (
    echo [✓] Download thành công!
    echo File đã lưu tại: %local_path%
) else (
    echo [✗] Download thất bại!
)
echo.
pause
goto menu

:list_files
cls
echo ════════════════════════════════════════
echo   LIỆT KÊ FILE TRÊN VPS
echo ════════════════════════════════════════
echo.
echo [1] Liệt kê /workspace/
echo [2] Liệt kê /workspace/ComfyUI/output/
echo [3] Liệt kê /workspace/ComfyUI/models/
echo [4] Nhập đường dẫn khác
echo [5] Quay lại
echo.
set /p list_choice="Chọn (1-5): "

if "%list_choice%"=="1" set list_path=/workspace/
if "%list_choice%"=="2" set list_path=/workspace/ComfyUI/output/
if "%list_choice%"=="3" set list_path=/workspace/ComfyUI/models/
if "%list_choice%"=="4" (
    set /p list_path="Nhập đường dẫn: "
)
if "%list_choice%"=="5" goto menu

echo.
echo Danh sách file trong %list_path%:
echo ════════════════════════════════════════
ssh -p 56254 root@47.74.34.39 "ls -lh %list_path% 2>/dev/null || echo 'Thư mục không tồn tại'"
echo ════════════════════════════════════════
echo.
pause
goto menu
