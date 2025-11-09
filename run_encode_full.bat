@echo off
echo ============================================================
echo VIDEO TO JSON - ENCODE TOAN BO VIDEO
echo ============================================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay Python! Vui long cai dat Python truoc.
    pause
    exit /b 1
)

REM Cai dat opencv-python neu chua co
echo [1/3] Kiem tra thu vien...
pip show opencv-python >nul 2>&1
if errorlevel 1 (
    echo Installing opencv-python...
    pip install opencv-python
)

echo.
echo [2/3] Chay script encode video...
echo.

REM Chay script
python video_to_json_full.py

echo.
echo [3/3] HOAN THANH!
echo.
echo File JSON da duoc tao: 123_full.json
echo Ban co the upload file nay len de toi xem het video!
echo.

pause
