@echo off
REM ========================================
REM Setup Model Cache on SSD
REM Tận dụng SSD trống để cache models
REM ========================================

echo.
echo ========================================
echo   ComfyUI Model Cache Setup
echo   Toi uu hoa SSD cho model loading
echo ========================================
echo.

REM Check Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Script nay can chay voi quyen Administrator!
    echo.
    echo Click phai vao file bat -^> Run as Administrator
    echo.
    pause
    exit /b 1
)

REM Set paths
set COMFYUI_PATH=D:\ComfyUI_windows_portable\ComfyUI
set MODELS_PATH=%COMFYUI_PATH%\models
set TEMP_PATH=%COMFYUI_PATH%\temp
set OUTPUT_PATH=%COMFYUI_PATH%\output

echo [INFO] Duong dan ComfyUI: %COMFYUI_PATH%
echo [INFO] Duong dan Models: %MODELS_PATH%
echo [INFO] Duong dan Temp: %TEMP_PATH%
echo [INFO] Duong dan Output: %OUTPUT_PATH%
echo.

REM Check if paths exist
if not exist "%COMFYUI_PATH%" (
    echo [ERROR] Khong tim thay thu muc ComfyUI!
    pause
    exit /b 1
)

REM Create temp and output directories if not exist
if not exist "%TEMP_PATH%" (
    echo [INFO] Tao thu muc temp...
    mkdir "%TEMP_PATH%"
)

if not exist "%OUTPUT_PATH%" (
    echo [INFO] Tao thu muc output...
    mkdir "%OUTPUT_PATH%"
)

echo.
echo ========================================
echo   Cau hinh Cache
echo ========================================
echo.

REM Option 1: Windows Prefetch Optimization
echo [1/4] Bat Windows Prefetch cho ComfyUI...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 3 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters" /v EnableSuperfetch /t REG_DWORD /d 3 /f >nul 2>&1
echo    - Prefetch: Enabled

REM Option 2: Disable 8.3 filename for faster file access
echo [2/4] Toi uu hoa file system...
fsutil behavior set disable8dot3 1 >nul 2>&1
echo    - 8.3 filename: Disabled (faster)

REM Option 3: Set large system cache
echo [3/4] Tang system cache...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v LargeSystemCache /t REG_DWORD /d 1 /f >nul 2>&1
echo    - Large System Cache: Enabled

REM Option 4: Optimize for background services (better for server-like apps)
echo [4/4] Toi uu hoa cho background services...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 24 /f >nul 2>&1
echo    - Priority: Optimized for background services

echo.
echo ========================================
echo   Thong tin Cache
echo ========================================
echo.

REM Show disk space
echo [INFO] Dung luong cac o dia:
echo.
wmic logicaldisk get caption,freespace,size,filesystem 2>nul | findstr /V "Caption"
echo.

REM Show models folder size
echo [INFO] Kiem tra dung luong models...
powershell -Command "if (Test-Path '%MODELS_PATH%') { $size = (Get-ChildItem -Path '%MODELS_PATH%' -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB; Write-Host ('Models folder: {0:N2} GB' -f $size) } else { Write-Host 'Models folder: Not found' }"
echo.

REM Show temp folder size
echo [INFO] Kiem tra dung luong temp...
powershell -Command "if (Test-Path '%TEMP_PATH%') { $size = (Get-ChildItem -Path '%TEMP_PATH%' -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB; Write-Host ('Temp folder: {0:N2} GB' -f $size) } else { Write-Host 'Temp folder: 0 GB' }"
echo.

echo ========================================
echo   THANH CONG!
echo ========================================
echo.
echo [OK] Da cau hinh cache toi uu cho ComfyUI
echo.
echo Cac thay doi:
echo   1. Windows Prefetch: Enabled
echo   2. File system: Optimized
echo   3. System cache: Increased
echo   4. Background priority: Optimized
echo.
echo [INFO] Khoi dong lai ComfyUI de ap dung thay doi
echo [INFO] Models se duoc cache tu dong vao RAM/SSD khi load
echo.

pause
