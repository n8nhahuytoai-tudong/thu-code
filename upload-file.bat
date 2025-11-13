@echo off
chcp 65001 >nul
title Upload File Lên VPS
color 0A

:menu
cls
echo ╔════════════════════════════════════════╗
echo ║     UPLOAD FILE LÊN VPS                ║
echo ╚════════════════════════════════════════╝
echo.
echo VPS: 47.74.34.39:56254
echo.
echo [1] Upload 1 file
echo [2] Upload cả thư mục
echo [3] Upload vào thư mục models (ComfyUI)
echo [4] Thoát
echo.
set /p choice="Chọn (1-4): "

if "%choice%"=="1" goto upload_file
if "%choice%"=="2" goto upload_folder
if "%choice%"=="3" goto upload_model
if "%choice%"=="4" exit
goto menu

:upload_file
cls
echo ════════════════════════════════════════
echo   UPLOAD FILE
echo ════════════════════════════════════════
echo.
set /p file_path="Kéo file vào đây (hoặc nhập đường dẫn): "

REM Xóa dấu ngoặc kép nếu có
set file_path=%file_path:"=%

if not exist "%file_path%" (
    echo.
    echo [!] File không tồn tại!
    pause
    goto menu
)

set /p remote_path="Đường dẫn lưu trên VPS (mặc định /workspace/): "
if "%remote_path%"=="" set remote_path=/workspace/

echo.
echo Đang upload...
echo Từ: %file_path%
echo Đến: %remote_path%
echo.

scp -P 56254 "%file_path%" root@47.74.34.39:%remote_path%

echo.
if %errorlevel%==0 (
    echo [✓] Upload thành công!
) else (
    echo [✗] Upload thất bại!
)
echo.
pause
goto menu

:upload_folder
cls
echo ════════════════════════════════════════
echo   UPLOAD THƯ MỤC
echo ════════════════════════════════════════
echo.
set /p folder_path="Kéo thư mục vào đây (hoặc nhập đường dẫn): "

REM Xóa dấu ngoặc kép
set folder_path=%folder_path:"=%

if not exist "%folder_path%" (
    echo.
    echo [!] Thư mục không tồn tại!
    pause
    goto menu
)

set /p remote_path="Đường dẫn lưu trên VPS (mặc định /workspace/): "
if "%remote_path%"=="" set remote_path=/workspace/

echo.
echo Đang upload thư mục...
echo Từ: %folder_path%
echo Đến: %remote_path%
echo.

scp -P 56254 -r "%folder_path%" root@47.74.34.39:%remote_path%

echo.
if %errorlevel%==0 (
    echo [✓] Upload thành công!
) else (
    echo [✗] Upload thất bại!
)
echo.
pause
goto menu

:upload_model
cls
echo ════════════════════════════════════════
echo   UPLOAD MODEL (COMFYUI)
echo ════════════════════════════════════════
echo.
echo Model sẽ được upload vào:
echo   /workspace/ComfyUI/models/checkpoints/
echo.
set /p model_path="Kéo file model vào đây (.safetensors hoặc .ckpt): "

REM Xóa dấu ngoặc kép
set model_path=%model_path:"=%

if not exist "%model_path%" (
    echo.
    echo [!] File không tồn tại!
    pause
    goto menu
)

echo.
echo Đang upload model...
echo File: %model_path%
echo.

scp -P 56254 "%model_path%" root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/

echo.
if %errorlevel%==0 (
    echo [✓] Upload model thành công!
    echo Model đã sẵn sàng để dùng trong ComfyUI
) else (
    echo [✗] Upload thất bại!
    echo Kiểm tra:
    echo   1. VPS có đang chạy không?
    echo   2. Thư mục ComfyUI đã tồn tại chưa?
)
echo.
pause
goto menu
