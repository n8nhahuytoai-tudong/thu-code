@echo off
chcp 65001 >nul 2>&1
cls
echo ========================================
echo    SETUP API KEY CHO VIDEO ANALYZER
echo ========================================
echo.

REM Check if .env already exists
if exist .env (
    echo [!] File .env da ton tai!
    echo.
    echo Ban muon:
    echo   [1] Mo file .env hien tai
    echo   [2] Tao lai file .env moi (ghi de file cu)
    echo   [0] Thoat
    echo.
    set /p choice=Nhap lua chon (0-2): 
    
    if "%choice%"=="1" goto OPEN_EXISTING
    if "%choice%"=="2" goto CREATE_NEW
    if "%choice%"=="0" exit
    goto END
)

:CREATE_NEW
echo [1/3] Tao file .env tu template...
copy .env.example .env >nul 2>&1

if errorlevel 1 (
    echo [ERROR] Khong the tao file .env!
    echo.
    echo Vui long thu thu cong:
    echo   copy .env.example .env
    pause
    exit /b 1
)

echo [OK] Da tao file .env
echo.

:OPEN_EXISTING
echo [2/3] Mo file .env de ban dien API key...
echo.
echo Huong dan:
echo   1. Truy cap: https://console.anthropic.com/
echo   2. Dang ky tai khoan (mien phi $5 credit)
echo   3. Settings - API Keys - Create Key
echo   4. Copy key (dang: sk-ant-api03-xxxxx)
echo   5. Dan vao file .env thay cho YOUR_API_KEY_HERE
echo   6. Save file (Ctrl+S) va dong lai
echo.
pause
echo.

REM Try to open with notepad
notepad .env

echo.
echo [3/3] Kiem tra file .env...

REM Check if API key was filled
findstr /C:"YOUR_API_KEY_HERE" .env >nul
if %errorlevel%==0 (
    echo.
    echo [!] CANH BAO: Ban chua dien API key!
    echo.
    echo File .env van con "YOUR_API_KEY_HERE"
    echo Vui long mo lai file va dien API key that.
    echo.
    echo De mo lai: notepad .env
    echo.
) else (
    findstr /C:"sk-ant-" .env >nul
    if %errorlevel%==0 (
        echo [OK] Da dien API key!
        echo.
        echo ========================================
        echo   SETUP HOAN TAT!
        echo ========================================
        echo.
        echo Ban co the chay tool voi AI:
        echo   start.bat - Chon [1] hoac [2]
        echo.
    ) else (
        echo [!] CANH BAO: API key co ve khong dung format!
        echo.
        echo API key phai bat dau bang: sk-ant-
        echo Vui long kiem tra lai.
        echo.
    )
)

:END
pause
