@echo off
REM ========================================
REM ComfyUI Optimized Startup Script
REM For RTX 3060 12GB + High RAM Usage
REM ========================================

echo.
echo ========================================
echo   ComfyUI - Optimized Mode
echo   GPU: RTX 3060 12GB
echo   Mode: High VRAM + SSD Swap
echo ========================================
echo.

REM Change to ComfyUI directory
cd /d D:\ComfyUI_windows_portable\ComfyUI

REM Check if Python exists
if not exist ".\python_embeded\python.exe" (
    echo [ERROR] Khong tim thay Python!
    echo Duong dan: D:\ComfyUI_windows_portable\ComfyUI\python_embeded\python.exe
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
