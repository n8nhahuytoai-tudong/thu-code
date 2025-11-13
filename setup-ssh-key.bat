@echo off
chcp 65001 >nul
title Setup SSH Key cho Vast.ai
color 0E

:menu
cls
echo ╔════════════════════════════════════════╗
echo ║     SETUP SSH KEY CHO VAST.AI          ║
echo ╚════════════════════════════════════════╝
echo.
echo [1] Tạo SSH Key mới (nếu chưa có)
echo [2] Xem SSH Public Key (để copy vào Vast.ai)
echo [3] Test kết nối VPS
echo [4] Hướng dẫn chi tiết
echo [5] Thoát
echo.
set /p choice="Chọn (1-5): "

if "%choice%"=="1" goto create_key
if "%choice%"=="2" goto show_key
if "%choice%"=="3" goto test_connection
if "%choice%"=="4" goto guide
if "%choice%"=="5" exit
goto menu

:create_key
cls
echo ====================================
echo   TẠO SSH KEY MỚI
echo ====================================
echo.
echo SSH Key sẽ được tạo tại: %USERPROFILE%\.ssh\
echo.
echo Nhấn Enter 3 lần khi được hỏi (không cần đặt password)
echo.
pause

REM Tạo thư mục .ssh nếu chưa có
if not exist "%USERPROFILE%\.ssh" mkdir "%USERPROFILE%\.ssh"

REM Tạo SSH key
ssh-keygen -t ed25519 -C "vastai-key" -f "%USERPROFILE%\.ssh\id_ed25519"

echo.
echo ====================================
echo   SSH Key đã được tạo!
echo ====================================
echo.
echo Bây giờ chọn [2] để xem Public Key
echo và copy vào Vast.ai
echo.
pause
goto menu

:show_key
cls
echo ====================================
echo   SSH PUBLIC KEY CỦA BẠN
echo ====================================
echo.

if not exist "%USERPROFILE%\.ssh\id_ed25519.pub" (
    echo [!] Chưa có SSH key!
    echo     Chọn [1] để tạo SSH key mới
    echo.
    pause
    goto menu
)

echo Copy toàn bộ dòng text dưới đây:
echo.
echo ────────────────────────────────────────
type "%USERPROFILE%\.ssh\id_ed25519.pub"
echo.
echo ────────────────────────────────────────
echo.
echo.
echo HƯỚNG DẪN THÊM VÀO VAST.AI:
echo.
echo 1. Vào: https://cloud.vast.ai/account/
echo 2. Tìm phần "SSH Keys" hoặc "Change SSH Key"
echo 3. Dán (Paste) dòng text trên vào ô
echo 4. Click "Set SSH Key" hoặc "Update"
echo 5. Xong! Bây giờ có thể kết nối VPS
echo.
echo Sau khi thêm key vào Vast.ai, chọn [3] để test!
echo.
pause
goto menu

:test_connection
cls
echo ====================================
echo   TEST KẾT NỐI VPS
echo ====================================
echo.
echo Đang kết nối...
echo.

ssh -p 56254 root@47.74.34.39 -L 8080:localhost:8080 -o ConnectTimeout=10

echo.
if %errorlevel%==0 (
    echo [✓] Kết nối thành công!
) else (
    echo [✗] Kết nối thất bại!
    echo.
    echo Kiểm tra:
    echo   1. Đã thêm SSH key vào Vast.ai chưa?
    echo   2. VPS có đang Running không?
    echo   3. Thông tin SSH còn đúng không?
)
echo.
pause
goto menu

:guide
cls
echo ╔════════════════════════════════════════╗
echo ║     HƯỚNG DẪN CHI TIẾT                 ║
echo ╚════════════════════════════════════════╝
echo.
echo LỖI: Permission denied (publickey)
echo.
echo NGUYÊN NHÂN:
echo   VPS yêu cầu SSH Key để đăng nhập
echo   Không thể dùng password
echo.
echo GIẢI PHÁP:
echo.
echo BƯỚC 1: Tạo SSH Key
echo   - Chọn [1] trong menu
echo   - Nhấn Enter 3 lần
echo.
echo BƯỚC 2: Lấy Public Key
echo   - Chọn [2] trong menu
echo   - Copy toàn bộ dòng text
echo.
echo BƯỚC 3: Thêm vào Vast.ai
echo   - Vào: https://cloud.vast.ai/account/
echo   - Tìm "SSH Keys" hoặc "Change SSH Key"
echo   - Paste key vào
echo   - Click "Set SSH Key"
echo.
echo BƯỚC 4: Restart VPS (QUAN TRỌNG!)
echo   - Vào: https://cloud.vast.ai/instances/
echo   - Click nút "Stop" instance
echo   - Đợi dừng hẳn
echo   - Click "Start" lại
echo   - Đợi chuyển sang "Running"
echo.
echo BƯỚC 5: Kết nối
echo   - Chọn [3] để test
echo   - Hoặc chạy file ket-noi-vps.bat
echo.
echo LƯU Ý:
echo   - SSH key chỉ cần tạo 1 lần
echo   - Có thể dùng cho nhiều VPS
echo   - Nếu đổi máy, cần thêm key mới
echo.
pause
goto menu
