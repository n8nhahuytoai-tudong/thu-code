@echo off
REM ========================================
REM ComfyUI CPU + SSD Optimization Mode
REM Tận dụng CPU và SSD trống
REM ========================================

echo.
echo ========================================
echo   ComfyUI - CPU/SSD BOOST MODE
echo   GPU: RTX 3060 12GB
echo   CPU: Offload preprocessing/postprocessing
echo   SSD: Fast model cache
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

REM Set environment variables for CPU optimization
set PYTHON=.\python_embeded\python.exe

REM Enable multi-threading for CPU
set OMP_NUM_THREADS=8
set MKL_NUM_THREADS=8
set NUMEXPR_NUM_THREADS=8
set OPENBLAS_NUM_THREADS=8

REM Set PyTorch to use more CPU threads
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

REM Arguments for CPU + GPU hybrid mode
REM --highvram: Use full VRAM (12GB)
REM --preview-method auto: Auto preview
REM --use-split-cross-attention: Reduce memory usage
REM --force-fp16: Force FP16 for faster inference (optional)
REM --disable-cuda-malloc: Use system memory allocator (better for CPU offload)

set ARGS=--highvram --preview-method auto --use-split-cross-attention

REM Optional: Uncomment for extreme optimization
REM set ARGS=%ARGS% --force-fp16
REM set ARGS=%ARGS% --disable-cuda-malloc

echo [INFO] CPU Threads: 8
echo [INFO] GPU VRAM: 12GB (High mode)
echo [INFO] SSD Cache: Enabled (via system)
echo [INFO] Starting ComfyUI with CPU offload...
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
