@echo off
REM ========================================
REM ComfyUI Optimized Startup Script
REM For RTX 3060 12GB + High RAM Usage
REM FIXED PATH: D:\ComfyUI_windows_portable
REM ========================================

echo.
echo ========================================
echo   ComfyUI - Optimized Mode
echo   GPU: RTX 3060 12GB
echo   Mode: High VRAM + SSD Swap
echo ========================================
echo.

REM Change to ComfyUI directory - FIXED PATH
cd /d D:\ComfyUI_windows_portable

REM Check if Python exists
if not exist ".\python_embeded\python.exe" (
    echo [ERROR] Khong tim thay Python!
    echo Duong dan: D:\ComfyUI_windows_portable\python_embeded\python.exe
    echo.
    echo Vui long kiem tra:
    echo   1. ComfyUI co o D:\ComfyUI_windows_portable khong?
    echo   2. File python_embeded\python.exe co ton tai khong?
    echo.
    echo Neu ComfyUI o cho khac, sua file nay:
    echo   - Click phai -> Edit
    echo   - Tim dong: cd /d D:\ComfyUI_windows_portable
    echo   - Sua thanh duong dan dung cua ban
    echo.
    pause
    exit /b 1
)

REM Set optimized arguments for RTX 3060 12GB
set PYTHON=.\python_embeded\python.exe
set ARGS=--highvram --preview-method auto --use-split-cross-attention

REM Optional: Uncomment if needed
REM --normalvram        : Use if loading very large models
REM --lowvram           : Use if VRAM not enough
REM --cpu               : Offload some processing to CPU
REM --disable-xformers  : Disable xformers if errors occur

echo [INFO] Starting ComfyUI with optimized settings...
echo [INFO] Path: D:\ComfyUI_windows_portable
echo [INFO] Arguments: %ARGS%
echo.

REM Start ComfyUI
%PYTHON% main.py %ARGS%

REM If error occurs
if errorlevel 1 (
    echo.
    echo [ERROR] ComfyUI gap loi khi khoi dong!
    echo.
)

pause
