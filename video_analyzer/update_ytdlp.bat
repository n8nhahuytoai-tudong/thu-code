@echo off
echo ========================================
echo    UPDATE YT-DLP
echo ========================================
echo.

echo This will update yt-dlp to the latest version
echo to fix YouTube download errors (nsig extraction, etc.)
echo.
pause

echo.
echo Uninstalling old version...
pip uninstall yt-dlp -y

if errorlevel 1 (
    echo [WARNING] Could not uninstall old version
    echo Continuing anyway...
)

echo.
echo Installing latest yt-dlp...
pip install yt-dlp

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install yt-dlp
    echo.
    echo Please try manually:
    echo   pip install --upgrade yt-dlp
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] yt-dlp updated!
echo ========================================
echo.

echo Checking version...
yt-dlp --version

echo.
echo You can now try downloading YouTube videos again
echo.
pause
