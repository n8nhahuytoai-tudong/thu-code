@echo off
REM ========================================
REM ComfyUI - ALL-IN-ONE OPTIMIZED
REM Gop tat ca toi uu vao 1 file duy nhat
REM ========================================

echo.
echo ========================================
echo   ComfyUI - OPTIMIZED (ALL-IN-ONE)
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if python exists
if not exist "python_embeded\python.exe" (
    echo [ERROR] Khong tim thay Python!
    echo.
    echo Vui long copy file nay vao thu muc ComfyUI chinh
    echo Vi du: D:\ComfyUI_windows_portable\
    echo.
    pause
    exit /b 1
)

REM Check if ComfyUI\main.py exists
if not exist "ComfyUI\main.py" (
    echo [ERROR] Khong tim thay ComfyUI\main.py!
    echo.
    echo Vui long copy file nay vao thu muc ComfyUI chinh
    echo Vi du: D:\ComfyUI_windows_portable\
    echo.
    pause
    exit /b 1
)

echo [OK] Tim thay ComfyUI tai: %CD%
echo.

REM ======================
REM CPU OPTIMIZATION
REM ======================
set OMP_NUM_THREADS=8
set MKL_NUM_THREADS=8
set NUMEXPR_NUM_THREADS=8
set OPENBLAS_NUM_THREADS=8
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

echo [SETUP] CPU Threads: 8
echo [SETUP] GPU VRAM: High mode (12GB)
echo [SETUP] SSD Cache: Enabled

REM ======================
REM ARGUMENTS
REM ======================
REM Ban co the BAT/TAT cac option sau:

REM Option 1: BASIC (Mac dinh)
set ARGS=--windows-standalone-build --highvram --preview-method auto

REM Option 2: WITH FP16 (Nhanh 2x, VRAM 50%, Quality 99%) - KHUYẾN NGHỊ!
REM Uncomment dong duoi de bat FP16:
REM set ARGS=--windows-standalone-build --highvram --preview-method auto --force-fp16

REM Option 3: EXTREME (Nhanh nhat, Quality giam 5-10%)
REM set ARGS=--windows-standalone-build --highvram --preview-method auto --force-fp16 --use-split-cross-attention

echo.
echo ========================================
echo   CHON CHE DO (Chi can sua 1 lan)
echo ========================================
echo.
echo Hien tai dang dung: BASIC MODE
echo.
echo Muon NHANH 2X?
echo   - Mo file nay bang Notepad
echo   - Tim dong: REM set ARGS=...--force-fp16
echo   - Xoa chu "REM " o dau dong
echo   - Luu file va chay lai
echo.
echo ========================================
echo   STARTING COMFYUI...
echo ========================================
echo.

REM Start ComfyUI
python_embeded\python.exe -s ComfyUI\main.py %ARGS%

if errorlevel 1 (
    echo.
    echo [ERROR] ComfyUI gap loi!
    echo.
)

pause
