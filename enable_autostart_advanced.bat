@echo off
REM ========================================
REM Auto-start ComfyUI on Windows Boot
REM Method: Task Scheduler (Advanced)
REM ========================================

echo.
echo ========================================
echo   ComfyUI Auto-Start Setup (Advanced)
echo   Su dung Windows Task Scheduler
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
set COMFYUI_SCRIPT=D:\ComfyUI_windows_portable\start_comfyui_cpu_boost.bat
set TASK_NAME=ComfyUI_AutoStart

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

REM Check if task already exists
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Task da ton tai trong Task Scheduler!
    echo.
    choice /C YN /M "Ban co muon xoa task cu va tao lai khong"
    if errorlevel 2 (
        echo [INFO] Huy bo thao tac
        pause
        exit /b 0
    )
    schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1
    echo [OK] Da xoa task cu
    echo.
)

REM Get delay time from user
echo [CONFIG] Cau hinh thoi gian delay...
echo.
echo Ban muon ComfyUI chay sau bao lau khi bat may?
echo   1. Ngay lap tuc (0 giay)
echo   2. Sau 30 giay (khuynen nghi)
echo   3. Sau 60 giay
echo   4. Sau 120 giay (2 phut)
echo.
choice /C 1234 /N /M "Chon (1-4): "

if errorlevel 4 (
    set DELAY=PT2M
    set DELAY_TEXT=2 phut
) else if errorlevel 3 (
    set DELAY=PT1M
    set DELAY_TEXT=1 phut
) else if errorlevel 2 (
    set DELAY=PT30S
    set DELAY_TEXT=30 giay
) else (
    set DELAY=PT0S
    set DELAY_TEXT=ngay lap tuc
)

echo.
echo [INFO] Dang tao Task Scheduler...
echo   - Ten task: %TASK_NAME%
echo   - Script: %COMFYUI_SCRIPT%
echo   - Delay: %DELAY_TEXT%
echo.

REM Create Task Scheduler task
schtasks /Create /TN "%TASK_NAME%" /TR "\"%COMFYUI_SCRIPT%\"" /SC ONLOGON /DELAY %DELAY% /RL HIGHEST /F

if errorlevel 1 (
    echo [ERROR] Khong the tao task!
    echo.
    pause
    exit /b 1
)

echo [OK] Tao task thanh cong!
echo.

echo ========================================
echo   THANH CONG!
echo ========================================
echo.
echo [OK] ComfyUI se TU DONG CHAY khi bat may!
echo.
echo Thong tin:
echo   - Task name: %TASK_NAME%
echo   - Trigger: Khi dang nhap Windows
echo   - Delay: %DELAY_TEXT%
echo   - Priority: Highest
echo   - Script: %COMFYUI_SCRIPT%
echo.
echo Luu y:
echo   - ComfyUI se chay sau %DELAY_TEXT% khi dang nhap
echo   - Task chay voi quyen cao nhat (Administrator)
echo   - Server chay tai: http://127.0.0.1:8188
echo.
echo Muon TAT auto-start:
echo   - Chay file: disable_autostart.bat
echo   - Hoac xoa task trong Task Scheduler
echo.

REM Ask to open Task Scheduler
choice /C YN /M "Ban co muon mo Task Scheduler de xem task khong"
if errorlevel 2 goto :end

taskschd.msc

:end
pause
