@echo off
setlocal enabledelayedexpansion
REM ========================================
REM Find ComfyUI Installation
REM Tu dong tim duong dan ComfyUI
REM ========================================

echo.
echo ========================================
echo   Tim duong dan ComfyUI
echo ========================================
echo.

echo [INFO] Dang tim kiem ComfyUI trong cac thu muc pho bien...
echo.

set FOUND=0

REM Check common paths
if exist "D:\ComfyUI_windows_portable\ComfyUI\python_embeded\python.exe" (
    set COMFYUI_PATH=D:\ComfyUI_windows_portable\ComfyUI
    set FOUND=1
    goto :found
)

if exist "D:\ComfyUI_windows_portable\python_embeded\python.exe" (
    set COMFYUI_PATH=D:\ComfyUI_windows_portable
    set FOUND=1
    goto :found
)

if exist "D:\ComfyUI\python_embeded\python.exe" (
    set COMFYUI_PATH=D:\ComfyUI
    set FOUND=1
    goto :found
)

if exist "C:\ComfyUI_windows_portable\ComfyUI\python_embeded\python.exe" (
    set COMFYUI_PATH=C:\ComfyUI_windows_portable\ComfyUI
    set FOUND=1
    goto :found
)

if exist "C:\ComfyUI_windows_portable\python_embeded\python.exe" (
    set COMFYUI_PATH=C:\ComfyUI_windows_portable
    set FOUND=1
    goto :found
)

if exist "C:\ComfyUI\python_embeded\python.exe" (
    set COMFYUI_PATH=C:\ComfyUI
    set FOUND=1
    goto :found
)

if exist "%USERPROFILE%\ComfyUI_windows_portable\ComfyUI\python_embeded\python.exe" (
    set COMFYUI_PATH=%USERPROFILE%\ComfyUI_windows_portable\ComfyUI
    set FOUND=1
    goto :found
)

if exist "%USERPROFILE%\ComfyUI_windows_portable\python_embeded\python.exe" (
    set COMFYUI_PATH=%USERPROFILE%\ComfyUI_windows_portable
    set FOUND=1
    goto :found
)

if exist "%USERPROFILE%\ComfyUI\python_embeded\python.exe" (
    set COMFYUI_PATH=%USERPROFILE%\ComfyUI
    set FOUND=1
    goto :found
)

REM Not found in common paths
:not_found
echo [NOT FOUND] Khong tim thay ComfyUI trong cac thu muc pho bien!
echo.
echo Cac thu muc da kiem tra:
echo   - D:\ComfyUI_windows_portable\ComfyUI
echo   - D:\ComfyUI_windows_portable
echo   - D:\ComfyUI
echo   - C:\ComfyUI_windows_portable\ComfyUI
echo   - C:\ComfyUI_windows_portable
echo   - C:\ComfyUI
echo   - %USERPROFILE%\ComfyUI_windows_portable\ComfyUI
echo   - %USERPROFILE%\ComfyUI_windows_portable
echo   - %USERPROFILE%\ComfyUI
echo.
echo Vui long nhap duong dan thu cong:
echo Chu y: KHONG can phan "\ComfyUI" cuoi cung neu da co
echo.
echo Vi du:
echo   - D:\ComfyUI_windows_portable\ComfyUI
echo   - D:\ComfyUI_windows_portable
echo   - E:\AI\ComfyUI
echo.
set /p "COMFYUI_PATH=Nhap duong dan ComfyUI: "

REM Remove trailing backslash
if "%COMFYUI_PATH:~-1%"=="\" set COMFYUI_PATH=%COMFYUI_PATH:~0,-1%

REM Validate manual path
if not exist "%COMFYUI_PATH%\python_embeded\python.exe" (
    echo.
    echo [ERROR] Duong dan khong hop le!
    echo Khong tim thay: %COMFYUI_PATH%\python_embeded\python.exe
    echo.
    echo Vui long kiem tra lai:
    echo   1. Duong dan co dung khong?
    echo   2. ComfyUI co duoc cai dat khong?
    echo   3. File python_embeded\python.exe co ton tai khong?
    echo.
    pause
    exit /b 1
)

:found
echo ========================================
echo   TIM THAY COMFYUI!
echo ========================================
echo.
echo ComfyUI path: %COMFYUI_PATH%
echo Python: %COMFYUI_PATH%\python_embeded\python.exe
echo.

REM Check if main.py exists
if exist "%COMFYUI_PATH%\main.py" (
    echo [OK] main.py: Tim thay
) else (
    echo [WARNING] main.py: Khong tim thay!
    echo Duong dan co the chua dung?
)
echo.

REM Save to config file
echo %COMFYUI_PATH%> "%~dp0comfyui_path.txt"
echo [SAVED] Da luu duong dan vao: comfyui_path.txt
echo.

REM Ask to update all .bat files
echo Ban co muon tu dong cap nhat tat ca .bat files?
echo (Sua duong dan trong start_comfyui*.bat, enable_autostart*.bat)
echo.
choice /C YN /M "Cap nhat (Y/N)"
if errorlevel 2 goto :skip_update

echo.
echo [INFO] Dang cap nhat tat ca .bat files...
echo.

REM Update .bat files
set COUNT=0

if exist "start_comfyui_optimized.bat" (
    powershell -Command "(Get-Content 'start_comfyui_optimized.bat') -replace 'cd /d .*ComfyUI', 'cd /d %COMFYUI_PATH%' | Set-Content 'start_comfyui_optimized.bat'"
    echo [OK] start_comfyui_optimized.bat
    set /a COUNT+=1
)

if exist "start_comfyui_cpu_boost.bat" (
    powershell -Command "(Get-Content 'start_comfyui_cpu_boost.bat') -replace 'cd /d .*ComfyUI', 'cd /d %COMFYUI_PATH%' | Set-Content 'start_comfyui_cpu_boost.bat'"
    echo [OK] start_comfyui_cpu_boost.bat
    set /a COUNT+=1
)

if exist "enable_autostart_simple.bat" (
    powershell -Command "(Get-Content 'enable_autostart_simple.bat') -replace 'set COMFYUI_SCRIPT=.*', 'set COMFYUI_SCRIPT=%COMFYUI_PATH%\start_comfyui_cpu_boost.bat' | Set-Content 'enable_autostart_simple.bat'"
    echo [OK] enable_autostart_simple.bat
    set /a COUNT+=1
)

if exist "enable_autostart_advanced.bat" (
    powershell -Command "(Get-Content 'enable_autostart_advanced.bat') -replace 'set COMFYUI_SCRIPT=.*', 'set COMFYUI_SCRIPT=%COMFYUI_PATH%\start_comfyui_cpu_boost.bat' | Set-Content 'enable_autostart_advanced.bat'"
    echo [OK] enable_autostart_advanced.bat
    set /a COUNT+=1
)

echo.
echo [OK] Da cap nhat %COUNT% files!
echo.

:skip_update
echo.
echo ========================================
echo   HUONG DAN TIEP THEO
echo ========================================
echo.
echo Buoc 1: Copy cac file vao thu muc ComfyUI
echo   copy start_comfyui_cpu_boost.bat "%COMFYUI_PATH%\"
echo   copy start_comfyui_optimized.bat "%COMFYUI_PATH%\"
echo.
echo Buoc 2: Chay ComfyUI
echo   cd /d "%COMFYUI_PATH%"
echo   start_comfyui_cpu_boost.bat
echo.
echo Hoac double-click file trong thu muc:
echo   %COMFYUI_PATH%\start_comfyui_cpu_boost.bat
echo.

choice /C YN /M "Ban co muon mo thu muc ComfyUI khong"
if errorlevel 2 goto :end

explorer "%COMFYUI_PATH%"

:end
pause
