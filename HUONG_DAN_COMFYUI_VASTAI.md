# Hướng Dẫn Sử Dụng ComfyUI Trên Vast.ai

## 📋 Mục Lục
1. [Thuê VPS với ComfyUI](#1-thuê-vps-với-comfyui)
2. [Lấy thông tin SSH](#2-lấy-thông-tin-ssh)
3. [Kết nối VPS](#3-kết-nối-vps)
4. [Truy cập ComfyUI](#4-truy-cập-comfyui)
5. [File .bat tự động](#5-file-bat-tự-động)

---

## 1. Thuê VPS với ComfyUI

### Bước 1: Đăng nhập Vast.ai
- Vào: https://cloud.vast.ai/
- Đăng nhập tài khoản
- Nạp tiền vào account (nếu chưa có)

### Bước 2: Tìm instance phù hợp
1. Click vào **"Search"** hoặc **"Templates"**
2. Tìm kiếm: `comfyui` hoặc `vastai/comfy`
3. Hoặc chọn **Template**: `vastai/comfy`

### Bước 3: Lọc theo yêu cầu
**Khuyến nghị:**
- **GPU**: RTX 3090 / 4090 (giá tốt, hiệu năng cao)
- **VRAM**: Tối thiểu 24GB
- **Disk Space**: Tối thiểu 50GB
- **Upload/Download**: Tốc độ cao cho tải model

### Bước 4: Thuê instance
1. Click **"Rent"** ở instance bạn chọn
2. Chọn **Image/Template**:
   - Tìm `vastai/comfy`
   - Hoặc Docker image: `vastai/comfy:latest`
3. Chọn **Disk Space** (khuyến nghị: 100GB+)
4. Click **"Rent"** và đợi instance khởi động

### Bước 5: Đợi instance Running
- Instance sẽ chuyển sang trạng thái **"Running"** (màu xanh)
- Thường mất 1-3 phút

---

## 2. Lấy Thông Tin SSH

### Sau khi instance Running:

1. Vào trang: https://cloud.vast.ai/instances/
2. Tìm instance đang chạy
3. Click vào instance hoặc nút **"Connect"**
4. Bạn sẽ thấy lệnh SSH dạng:

```bash
ssh -p XXXXX root@sshX.vast.ai -L 8188:localhost:8188 -L 6006:localhost:6006
```

**Lưu ý các con số:**
- `XXXXX` = Port SSH (ví dụ: 30195, 41234, ...)
- `sshX.vast.ai` = Host (ví dụ: ssh1.vast.ai, ssh6.vast.ai, ...)
- `8188` = Port ComfyUI UI (mặc định)
- `6006` = Port TensorBoard (optional)

---

## 3. Kết Nối VPS

### Cách 1: Dùng file .bat (Windows)

**Tạo file `comfyui-connect.bat`** với nội dung:

```batch
@echo off
title Ket noi ComfyUI VPS
color 0A
echo ====================================
echo   Dang ket noi ComfyUI VPS...
echo ====================================
echo.
echo Port forward:
echo   - ComfyUI: http://localhost:8188
echo   - TensorBoard: http://localhost:6006
echo.
echo Sau khi ket noi thanh cong:
echo   Mo trinh duyet va vao: http://localhost:8188
echo ====================================
echo.

REM Thay doi PORT va HOST theo thong tin cua ban
ssh -p XXXXX root@sshX.vast.ai -L 8188:localhost:8188 -L 6006:localhost:6006

pause
```

**Thay thế:**
- `XXXXX` bằng port SSH của bạn
- `sshX.vast.ai` bằng host của bạn

**Double-click file** để kết nối!

### Cách 2: Dùng Command Prompt
```batch
ssh -p XXXXX root@sshX.vast.ai -L 8188:localhost:8188
```

### Cách 3: Dùng PuTTY (nếu thích giao diện)
1. Tải PuTTY: https://www.putty.org/
2. Mở PuTTY:
   - **Host**: sshX.vast.ai
   - **Port**: XXXXX
   - **Connection type**: SSH
3. Vào **Connection > SSH > Tunnels**:
   - **Source port**: 8188
   - **Destination**: localhost:8188
   - Click **"Add"**
4. Click **"Open"** để kết nối

---

## 4. Truy Cập ComfyUI

### Sau khi SSH kết nối thành công:

1. **Mở trình duyệt** (Chrome/Edge/Firefox)
2. Vào địa chỉ:
   ```
   http://localhost:8188
   ```
3. **ComfyUI** sẽ hiển thị! 🎨

### Nếu ComfyUI chưa chạy trên VPS:

Trong terminal SSH, gõ:

```bash
# Kiểm tra ComfyUI có đang chạy không
ps aux | grep comfy

# Nếu chưa chạy, khởi động ComfyUI
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

---

## 5. File .bat Tự Động (Mẫu Hoàn Chỉnh)

### Tạo file `comfyui-start.bat`:

```batch
@echo off
chcp 65001 >nul
title ComfyUI VPS - Kết nối
color 0B

:menu
cls
echo ╔════════════════════════════════════════╗
echo ║     COMFYUI VPS - VAST.AI              ║
echo ╚════════════════════════════════════════╝
echo.
echo [1] Kết nối VPS
echo [2] Mở ComfyUI (sau khi kết nối)
echo [3] Kiểm tra trạng thái kết nối
echo [4] Thoát
echo.
set /p choice="Chọn (1-4): "

if "%choice%"=="1" goto connect
if "%choice%"=="2" goto open_browser
if "%choice%"=="3" goto check
if "%choice%"=="4" exit
goto menu

:connect
cls
echo ====================================
echo   Đang kết nối VPS...
echo ====================================
echo.
echo Sau khi kết nối, chọn [2] để mở ComfyUI
echo Hoặc vào: http://localhost:8188
echo.

REM === THAY ĐỔI THÔNG TIN Ở ĐÂY ===
ssh -p XXXXX root@sshX.vast.ai -L 8188:localhost:8188 -L 6006:localhost:6006
REM ==================================

pause
goto menu

:open_browser
start http://localhost:8188
echo Đã mở ComfyUI trong trình duyệt!
timeout /t 2 >nul
goto menu

:check
cls
echo Đang kiểm tra kết nối...
curl -s http://localhost:8188 >nul 2>&1
if %errorlevel%==0 (
    echo [OK] ComfyUI đang chạy tại: http://localhost:8188
) else (
    echo [FAIL] Không kết nối được ComfyUI
    echo Hãy kiểm tra:
    echo   1. VPS có đang chạy không?
    echo   2. Đã SSH kết nối chưa?
    echo   3. Port forwarding đúng chưa?
)
echo.
pause
goto menu
```

**Chỉ cần thay đổi dòng:**
```batch
ssh -p XXXXX root@sshX.vast.ai -L 8188:localhost:8188
```

---

## 6. Xử Lý Lỗi Thường Gặp

### ❌ Lỗi: "Connection refused"
**Nguyên nhân:**
- VPS đã tắt/dừng
- Port hoặc host sai

**Giải pháp:**
1. Kiểm tra VPS có **Running** không tại: https://cloud.vast.ai/instances/
2. Copy lại lệnh SSH mới từ Vast.ai
3. Cập nhật lại file .bat

### ❌ Lỗi: Không mở được localhost:8188
**Nguyên nhân:**
- ComfyUI chưa chạy trên VPS
- Port forwarding sai

**Giải pháp:**
```bash
# SSH vào VPS, sau đó:
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

### ❌ Lỗi: "bind: Address already in use"
**Nguyên nhân:**
- Port 8188 đang được dùng bởi chương trình khác

**Giải pháp:**
```bash
# Tìm process đang dùng port
netstat -ano | findstr :8188

# Kill process (Windows)
taskkill /PID <PID> /F
```

---

## 7. Tải Models Vào VPS

### Cách 1: Download trực tiếp trên VPS
```bash
# SSH vào VPS
cd /workspace/ComfyUI/models/checkpoints

# Tải model (ví dụ: Stable Diffusion)
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors
```

### Cách 2: Upload từ máy local
```bash
# Từ máy Windows (CMD)
scp -P XXXXX C:\path\to\model.safetensors root@sshX.vast.ai:/workspace/ComfyUI/models/checkpoints/
```

---

## 8. Tips & Tricks

### ✅ Giữ ComfyUI chạy khi ngắt SSH
```bash
# Cài tmux
apt install tmux -y

# Chạy ComfyUI trong tmux
tmux new -s comfy
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188

# Detach: Ctrl+B rồi nhấn D
# Attach lại: tmux attach -s comfy
```

### ✅ Tự động khởi động ComfyUI
```bash
# Tạo script startup
cat > /workspace/start-comfy.sh << 'EOF'
#!/bin/bash
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188
EOF

chmod +x /workspace/start-comfy.sh

# Thêm vào crontab
(crontab -l 2>/dev/null; echo "@reboot /workspace/start-comfy.sh") | crontab -
```

### ✅ Kiểm tra GPU
```bash
nvidia-smi
watch -n 1 nvidia-smi  # Refresh mỗi giây
```

---

## 9. Bảng Giá Tham Khảo (Vast.ai)

| GPU | VRAM | Giá/giờ | Phù hợp |
|-----|------|---------|---------|
| RTX 3060 | 12GB | ~$0.10 | Học tập, test |
| RTX 3090 | 24GB | ~$0.20-0.30 | Tốt nhất |
| RTX 4090 | 24GB | ~$0.40-0.60 | Cao cấp |
| A100 | 40GB | ~$1.00+ | Chuyên nghiệp |

---

## 10. Checklist Hoàn Chỉnh

- [ ] Đăng nhập Vast.ai và nạp tiền
- [ ] Thuê instance với template `vastai/comfy`
- [ ] Đợi instance chuyển sang **Running**
- [ ] Copy lệnh SSH từ Vast.ai dashboard
- [ ] Tạo file .bat với thông tin SSH
- [ ] Double-click file .bat để kết nối
- [ ] Mở browser vào http://localhost:8188
- [ ] Tải models vào VPS (nếu cần)
- [ ] Bắt đầu sáng tạo! 🎨

---

**Chúc bạn sử dụng ComfyUI thành công!** 🚀
