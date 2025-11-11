@echo off
chcp 65001 >nul 2>&1
:MENU
cls
echo ========================================
echo    VIDEO ANALYZER TOOL
echo ========================================
echo.
echo Chon che do:
echo.
echo [1] Phan tich video local (co AI)
echo [2] Phan tich tu URL YouTube (co AI)
echo [3] Phan tich video local (KHONG AI - nhanh)
echo [4] Phan tich tu URL (KHONG AI - nhanh)
echo [5] Cai dat dependencies
echo [0] Thoat
echo.
set /p choice=Nhap lua chon (0-5):

if "%choice%"=="1" goto LOCAL_AI
if "%choice%"=="2" goto URL_AI
if "%choice%"=="3" goto LOCAL_NO_AI
if "%choice%"=="4" goto URL_NO_AI
if "%choice%"=="5" goto INSTALL
if "%choice%"=="0" exit
goto MENU

:LOCAL_AI
echo.
echo Nhap duong dan file video:
set /p VIDEO_PATH=
set VIDEO_PATH=%VIDEO_PATH:"=%
echo.
echo Dang phan tich voi AI...
python video_analyzer.py --input "%VIDEO_PATH%"
goto DONE

:URL_AI
echo.
echo Nhap URL video (YouTube, Vimeo, etc):
set /p VIDEO_URL=
echo.
echo Dang tai va phan tich voi AI...
python video_analyzer.py --url "%VIDEO_URL%"
goto DONE

:LOCAL_NO_AI
echo.
echo Nhap duong dan file video:
set /p VIDEO_PATH=
set VIDEO_PATH=%VIDEO_PATH:"=%
echo.
echo Dang phan tich nhanh (khong AI)...
python video_analyzer.py --input "%VIDEO_PATH%" --no-ai
goto DONE

:URL_NO_AI
echo.
echo Nhap URL video:
set /p VIDEO_URL=
echo.
echo Dang tai va phan tich nhanh (khong AI)...
python video_analyzer.py --url "%VIDEO_URL%" --no-ai
goto DONE

:INSTALL
echo.
echo Dang cai dat dependencies...
cd ..
pip install -r requirements.txt
cd video_analyzer
echo.
echo Hoan tat cai dat!
echo.
pause
goto MENU

:DONE
echo.
echo ========================================
echo HOAN TAT!
echo ========================================
echo.
echo Bao cao: output\reports\
echo Frames: output\frames\
echo.
pause
goto MENU
