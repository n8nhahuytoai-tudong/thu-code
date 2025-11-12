@echo off
REM ========================================
REM Create ZIP Package - Simple Version
REM Tao file ZIP chua tat ca scripts
REM ========================================

echo.
echo ========================================
echo   Creating ComfyUI Optimization Package
echo   Tao goi ZIP cac file toi uu hoa
echo ========================================
echo.

REM Run PowerShell script
echo [INFO] Running PowerShell script...
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0create_package.ps1"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to create package!
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Package created successfully!
echo.
pause
