@echo off
REM ========================================
REM Check Virtual Resources
REM RAM ao va GPU ao - Phan tich
REM ========================================

echo.
echo ========================================
echo   Kiem Tra RAM Ao va GPU Ao
echo ========================================
echo.

REM Run PowerShell script
powershell.exe -ExecutionPolicy Bypass -File "%~dp0check_virtual_resources.ps1"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to run check!
    echo.
    pause
    exit /b 1
)

pause
