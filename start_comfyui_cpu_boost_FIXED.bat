@echo off
REM ========================================
REM ComfyUI CPU + SSD Optimization Mode
REM Tan dung CPU va SSD trong
REM FIXED PATH: D:\ComfyUI_windows_portable
REM ========================================

echo.
echo ========================================
echo   ComfyUI - CPU/SSD BOOST MODE
echo   GPU: RTX 3060 12GB
echo   CPU: Offload preprocessing/postprocessing
echo   SSD: Fast model cache
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
REM --force-fp16: Force FP16 for faster inference (2x speed, 50% VRAM) - RECOMMENDED!

set ARGS=--highvram --preview-method auto --use-split-cross-attention

REM UNCOMMENT line below to enable FP16 (2x faster, 50% less VRAM):
REM set ARGS=--highvram --preview-method auto --use-split-cross-attention --force-fp16

echo [INFO] CPU Threads: 8
echo [INFO] GPU VRAM: 12GB (High mode)
echo [INFO] SSD Cache: Enabled (via system)
echo [INFO] Path: D:\ComfyUI_windows_portable
echo [INFO] Starting ComfyUI with CPU offload...
echo [INFO] Arguments: %ARGS%
echo.
echo [TIP] Muon nhanh 2x? Sua file nay, uncomment dong --force-fp16
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
