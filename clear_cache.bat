@echo off
chcp 65001 >nul

echo ======================================================================
echo                      XÓA CACHE
echo ======================================================================
echo.

if not exist "cache" (
    echo Không có cache để xóa!
    echo.
    pause
    exit /b 0
)

echo Bạn có chắc muốn xóa tất cả cache?
echo Cache giúp tiết kiệm tiền khi phân tích lại cùng video.
echo.
set /p confirm="Xác nhận xóa? (y/n): "

if /i not "%confirm%"=="y" (
    echo Đã hủy.
    pause
    exit /b 0
)

echo.
echo Đang xóa cache...
rmdir /S /Q cache 2>nul
mkdir cache

echo.
echo ✓ Đã xóa cache thành công!
echo.
pause
