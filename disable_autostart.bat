@echo off
REM ========================================
REM Disable ComfyUI Auto-Start
REM Remove from Startup and Task Scheduler
REM ========================================

echo.
echo ========================================
echo   ComfyUI Auto-Start Removal
echo   Tat chuc nang tu dong chay
echo ========================================
echo.

set REMOVED_COUNT=0

REM Check Startup folder shortcut
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT_NAME=ComfyUI_AutoStart.lnk

echo [1/2] Kiem tra Startup folder...
if exist "%STARTUP_FOLDER%\%SHORTCUT_NAME%" (
    echo [FOUND] Tim thay shortcut trong Startup folder
    del "%STARTUP_FOLDER%\%SHORTCUT_NAME%" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Khong the xoa shortcut!
    ) else (
        echo [OK] Da xoa shortcut
        set /a REMOVED_COUNT+=1
    )
) else (
    echo [INFO] Khong tim thay shortcut trong Startup folder
)
echo.

REM Check Task Scheduler
set TASK_NAME=ComfyUI_AutoStart

echo [2/2] Kiem tra Task Scheduler...
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo [FOUND] Tim thay task trong Task Scheduler

    REM Try to delete (may need admin)
    schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Khong the xoa task!
        echo [INFO] Can quyen Administrator de xoa task
        echo.
        echo Click phai vao file bat -^> Run as Administrator
        echo.
    ) else (
        echo [OK] Da xoa task
        set /a REMOVED_COUNT+=1
    )
) else (
    echo [INFO] Khong tim thay task trong Task Scheduler
)
echo.

REM Summary
echo ========================================
echo   KET QUA
echo ========================================
echo.

if %REMOVED_COUNT% gtr 0 (
    echo [OK] Da tat auto-start thanh cong!
    echo [OK] Da xoa %REMOVED_COUNT% cau hinh
    echo.
    echo ComfyUI se KHONG TU DONG CHAY khi bat may nua.
) else (
    echo [INFO] Khong tim thay cau hinh auto-start nao.
    echo [INFO] ComfyUI khong duoc cau hinh tu dong chay.
)
echo.

REM Check other possible startup locations
echo [INFO] Kiem tra cac vi tri khac...
echo.

REM Check common startup locations
set OTHER_STARTUP=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup

if exist "%OTHER_STARTUP%\%SHORTCUT_NAME%" (
    echo [WARNING] Tim thay shortcut trong System Startup folder!
    echo [INFO] Vi tri: %OTHER_STARTUP%
    echo [INFO] Can quyen Administrator de xoa
    echo.

    net session >nul 2>&1
    if %errorLevel% equ 0 (
        choice /C YN /M "Ban co muon xoa shortcut nay khong"
        if not errorlevel 2 (
            del "%OTHER_STARTUP%\%SHORTCUT_NAME%" >nul 2>&1
            if errorlevel 1 (
                echo [ERROR] Khong the xoa!
            ) else (
                echo [OK] Da xoa shortcut
            )
        )
    )
    echo.
)

REM Check registry run keys
echo [INFO] Kiem tra Registry startup keys...
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v ComfyUI >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Tim thay Registry key: HKCU\...\Run\ComfyUI
    choice /C YN /M "Ban co muon xoa registry key nay khong"
    if not errorlevel 2 (
        reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v ComfyUI /f >nul 2>&1
        if errorlevel 1 (
            echo [ERROR] Khong the xoa!
        ) else (
            echo [OK] Da xoa registry key
        )
    )
    echo.
)

reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v ComfyUI >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Tim thay Registry key: HKLM\...\Run\ComfyUI (System-wide)
    echo [INFO] Can quyen Administrator de xoa
    echo.

    net session >nul 2>&1
    if %errorLevel% equ 0 (
        choice /C YN /M "Ban co muon xoa registry key nay khong"
        if not errorlevel 2 (
            reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v ComfyUI /f >nul 2>&1
            if errorlevel 1 (
                echo [ERROR] Khong the xoa!
            ) else (
                echo [OK] Da xoa registry key
            )
        )
    )
    echo.
)

echo ========================================
echo.
echo Muon BAT lai auto-start:
echo   - Chay file: enable_autostart_simple.bat (don gian)
echo   - Hoac: enable_autostart_advanced.bat (nang cao)
echo.

pause
