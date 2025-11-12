@echo off
REM ========================================
REM Auto-start ComfyUI on Windows Boot
REM Method: Startup Folder (Simple)
REM ========================================

echo.
echo ========================================
echo   ComfyUI Auto-Start Setup (Simple)
echo   Them shortcut vao Startup folder
echo ========================================
echo.

REM Set paths
set COMFYUI_SCRIPT=D:\ComfyUI_windows_portable\start_comfyui_cpu_boost.bat
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT_NAME=ComfyUI_AutoStart.lnk

echo [INFO] Kiem tra file ComfyUI...
if not exist "%COMFYUI_SCRIPT%" (
    echo [ERROR] Khong tim thay file: %COMFYUI_SCRIPT%
    echo.
    echo Vui long kiem tra duong dan:
    echo 1. File co ton tai khong?
    echo 2. Duong dan co dung khong?
    echo.
    echo Hien tai dang tim: %COMFYUI_SCRIPT%
    echo.
    pause
    exit /b 1
)

echo [OK] Tim thay file ComfyUI
echo.

REM Check if shortcut already exists
if exist "%STARTUP_FOLDER%\%SHORTCUT_NAME%" (
    echo [WARNING] Shortcut da ton tai trong Startup folder!
    echo.
    choice /C YN /M "Ban co muon ghi de shortcut cu khong"
    if errorlevel 2 (
        echo [INFO] Huy bo thao tac
        pause
        exit /b 0
    )
    del "%STARTUP_FOLDER%\%SHORTCUT_NAME%" >nul 2>&1
)

REM Create shortcut using PowerShell
echo [INFO] Dang tao shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_FOLDER%\%SHORTCUT_NAME%'); $Shortcut.TargetPath = '%COMFYUI_SCRIPT%'; $Shortcut.WorkingDirectory = 'D:\ComfyUI_windows_portable'; $Shortcut.Description = 'ComfyUI Auto-Start with CPU Boost'; $Shortcut.Save()"

if errorlevel 1 (
    echo [ERROR] Khong the tao shortcut!
    echo.
    pause
    exit /b 1
)

echo [OK] Tao shortcut thanh cong!
echo.

echo ========================================
echo   THANH CONG!
echo ========================================
echo.
echo [OK] ComfyUI se TU DONG CHAY khi bat may!
echo.
echo Thong tin:
echo   - Shortcut: %SHORTCUT_NAME%
echo   - Vi tri: %STARTUP_FOLDER%
echo   - Script: %COMFYUI_SCRIPT%
echo.
echo Luu y:
echo   - ComfyUI se chay NGAY khi dang nhap Windows
echo   - Cua so Command Prompt se mo ra
echo   - Server chay tai: http://127.0.0.1:8188
echo.
echo Muon TAT auto-start:
echo   - Chay file: disable_autostart.bat
echo   - Hoac xoa shortcut trong Startup folder
echo.

REM Ask to open Startup folder
choice /C YN /M "Ban co muon mo Startup folder de xem shortcut khong"
if errorlevel 2 goto :end

explorer "%STARTUP_FOLDER%"

:end
pause
