@echo off
chcp 65001 >nul
:MENU
cls
echo ========================================
echo    VIDEO ANALYZER TOOL
echo    Phân tích video tự động với AI
echo ========================================
echo.
echo Chọn chế độ:
echo.
echo [1] Phân tích video local (có AI)
echo [2] Phân tích từ URL YouTube (có AI)
echo [3] Phân tích video local (KHÔNG AI - nhanh)
echo [4] Phân tích từ URL (KHÔNG AI - nhanh)
echo [5] Cài đặt dependencies
echo [0] Thoát
echo.
set /p choice=Nhập lựa chọn (0-5):

if "%choice%"=="1" goto LOCAL_AI
if "%choice%"=="2" goto URL_AI
if "%choice%"=="3" goto LOCAL_NO_AI
if "%choice%"=="4" goto URL_NO_AI
if "%choice%"=="5" goto INSTALL
if "%choice%"=="0" exit
goto MENU

:LOCAL_AI
echo.
echo 📁 Nhập đường dẫn file video:
set /p VIDEO_PATH=^>
set VIDEO_PATH=%VIDEO_PATH:"=%
echo.
echo 🎬 Đang phân tích với AI...
python video_analyzer.py --input "%VIDEO_PATH%"
goto DONE

:URL_AI
echo.
echo 🌐 Nhập URL video (YouTube, Vimeo, etc):
set /p VIDEO_URL=^>
echo.
echo 🎬 Đang tải và phân tích với AI...
python video_analyzer.py --url "%VIDEO_URL%"
goto DONE

:LOCAL_NO_AI
echo.
echo 📁 Nhập đường dẫn file video:
set /p VIDEO_PATH=^>
set VIDEO_PATH=%VIDEO_PATH:"=%
echo.
echo ⚡ Đang phân tích nhanh (không AI)...
python video_analyzer.py --input "%VIDEO_PATH%" --no-ai
goto DONE

:URL_NO_AI
echo.
echo 🌐 Nhập URL video:
set /p VIDEO_URL=^>
echo.
echo ⚡ Đang tải và phân tích nhanh (không AI)...
python video_analyzer.py --url "%VIDEO_URL%" --no-ai
goto DONE

:INSTALL
echo.
echo 📦 Đang cài đặt dependencies...
cd ..
pip install -r requirements.txt
cd video_analyzer
echo.
echo ✅ Hoàn tất cài đặt!
echo.
pause
goto MENU

:DONE
echo.
echo ========================================
echo ✅ HOÀN TẤT!
echo ========================================
echo.
echo 📊 Báo cáo: output\reports\
echo 🖼️  Frames: output\frames\
echo.
pause
goto MENU
