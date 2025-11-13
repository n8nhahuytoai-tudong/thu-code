# 📚 HƯỚNG DẪN SỬ DỤNG VPS - TÀI LIỆU TỔNG HỢP

## 🎯 Thông Tin VPS Hiện Tại

```
Host: 47.74.34.39
Port: 56254
User: root
Port Forward: 8080, 8188
```

---

## 📦 CÁC FILE TOOLS (Tải về và dùng)

### 1. **ket-noi-vps.bat**
**Mục đích:** Kết nối VPS đơn giản
- Double-click là kết nối ngay
- Port forward: 8080

### 2. **comfyui-connect.bat**
**Mục đích:** Kết nối VPS với menu
- Có menu lựa chọn
- Port forward: 8080, 8188
- Tích hợp mở browser

### 3. **setup-ssh-key.bat**
**Mục đích:** Tạo và quản lý SSH key
- Tạo SSH key tự động
- Hiển thị public key để copy
- Test kết nối VPS
- Sửa lỗi "Permission denied"

### 4. **upload-file.bat**
**Mục đích:** Upload file/folder lên VPS
- Upload 1 file
- Upload cả thư mục
- Upload model vào ComfyUI
- Kéo thả file vào

### 5. **download-file.bat**
**Mục đích:** Download file/folder từ VPS
- Download 1 file
- Download cả thư mục
- Download output ComfyUI
- Xem danh sách file trên VPS

---

## 📖 CÁC TÀI LIỆU HƯỚNG DẪN

### 1. **HUONG_DAN_DON_GIAN.md**
**Nội dung:** Hướng dẫn setup SSH key từ A-Z
- Các bước cực kỳ chi tiết
- Dành cho người mới bắt đầu
- Sửa lỗi "Permission denied"

### 2. **HUONG_DAN_SSH_KEY.md**
**Nội dung:** Hướng dẫn SSH key chi tiết
- Tạo SSH key
- Thêm key vào Vast.ai
- Xử lý lỗi thường gặp
- Tips nâng cao

### 3. **CHAY_COMFYUI.md**
**Nội dung:** Hướng dẫn chạy ComfyUI
- Cài đặt ComfyUI
- Chạy ComfyUI
- Chạy nền với tmux
- Tải models
- Xử lý lỗi

### 4. **TAI_FILE.md**
**Nội dung:** Hướng dẫn upload/download file
- Dùng SCP
- Dùng WinSCP/FileZilla
- Dùng HTTP
- Upload/download file lớn
- Các tips hữu ích

### 5. **HUONG_DAN_COMFYUI_VASTAI.md**
**Nội dung:** Hướng dẫn thuê VPS Vast.ai với ComfyUI
- Thuê VPS
- Cấu hình ComfyUI
- Lấy thông tin SSH
- Troubleshooting

### 6. **HUONG_DAN_TAI_FILE.md**
**Nội dung:** Hướng dẫn tải file tổng quát
- Phương pháp SCP
- Phương pháp rsync
- Script tự động

### 7. **KET_NOI_VPS_DON_GIAN.md**
**Nội dung:** Các cách kết nối VPS đơn giản
- SSH Config
- SSH Key
- Alias
- VS Code Remote
- Script

---

## 🚀 HƯỚNG DẪN NHANH - 3 BƯỚC

### ✅ LẦN ĐẦU TIÊN (Setup 1 lần duy nhất):

#### Bước 1: Tạo SSH Key
```
1. Tải file: setup-ssh-key.bat
2. Double-click file
3. Chọn [1] - Tạo SSH Key
4. Nhấn Enter 3 lần
```

#### Bước 2: Thêm Key vào Vast.ai
```
1. Trong setup-ssh-key.bat, chọn [2]
2. Copy dòng text (ssh-ed25519...)
3. Vào: https://cloud.vast.ai/account/
4. Paste vào ô "SSH Key"
5. Click "Set SSH Key"
```

#### Bước 3: Restart VPS
```
1. Vào: https://cloud.vast.ai/instances/
2. Stop VPS
3. Đợi 1 phút
4. Start lại
```

### ✅ TỪ LẦN SAU (Cực kỳ đơn giản):

#### Kết nối VPS:
```
Double-click: ket-noi-vps.bat
```

#### Upload file:
```
Double-click: upload-file.bat
```

#### Download file:
```
Double-click: download-file.bat
```

---

## 🎨 SỬ DỤNG COMFYUI

### Bước 1: Kết nối VPS
```
Double-click: ket-noi-vps.bat
```

### Bước 2: Chạy ComfyUI (trong SSH)
```bash
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8080
```

### Bước 3: Mở trình duyệt
```
http://localhost:8080
```

### Upload model:
```
Double-click: upload-file.bat
→ Chọn [3] - Upload model
→ Chọn file .safetensors
```

### Download kết quả:
```
Double-click: download-file.bat
→ Chọn [3] - Download từ output ComfyUI
```

---

## 🛠️ XỬ LÝ LỖI THƯỜNG GẶP

### ❌ Lỗi: "Permission denied (publickey)"
**Giải pháp:**
```
1. Chạy: setup-ssh-key.bat
2. Làm theo 3 bước ở trên
```

**Xem chi tiết:** `HUONG_DAN_DON_GIAN.md`

---

### ❌ Lỗi: "Connection refused"
**Nguyên nhân:**
- VPS đã tắt
- Port/IP sai

**Giải pháp:**
```
1. Vào: https://cloud.vast.ai/instances/
2. Kiểm tra VPS có "Running" không
3. Nếu đã tắt → Start lại
4. Copy lại thông tin SSH mới
```

---

### ❌ Không mở được localhost:8080
**Giải pháp:**
```
1. Kiểm tra ComfyUI có đang chạy không (trong SSH)
2. Kiểm tra port forwarding (-L 8080:localhost:8080)
3. Chạy lại file ket-noi-vps.bat
```

**Xem chi tiết:** `CHAY_COMFYUI.md`

---

## 💡 TIPS HỮU ÍCH

### 1. Chạy ComfyUI nền (không sợ mất kết nối):
```bash
# Cài tmux
apt install tmux -y

# Tạo session
tmux new -s comfy

# Chạy ComfyUI
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8080

# Thoát tmux: Ctrl+B rồi D
# Vào lại: tmux attach -s comfy
```

### 2. Xem GPU:
```bash
nvidia-smi
watch -n 1 nvidia-smi  # Refresh mỗi giây
```

### 3. Xem file trên VPS:
```bash
ls -lh /workspace/
ls -lh /workspace/ComfyUI/output/
```

### 4. Backup toàn bộ output:
```
Double-click: download-file.bat
→ Chọn [2] - Download thư mục
→ Nhập: /workspace/ComfyUI/output
```

---

## 📊 CÁC ĐƯỜNG DẪN QUAN TRỌNG

### Trên VPS:
```
/workspace/                             # Thư mục làm việc
/workspace/ComfyUI/                     # ComfyUI
/workspace/ComfyUI/models/checkpoints/  # Models
/workspace/ComfyUI/models/loras/        # LoRA
/workspace/ComfyUI/output/              # Kết quả
/workspace/ComfyUI/input/               # Input
```

### Trên máy Windows:
```
%USERPROFILE%\.ssh\                     # SSH keys
C:\Users\Admin\Desktop\                 # Desktop
C:\Users\Admin\Downloads\               # Downloads
```

---

## 🔗 LINKS QUAN TRỌNG

```
Vast.ai Dashboard:   https://cloud.vast.ai/instances/
Vast.ai Account:     https://cloud.vast.ai/account/
ComfyUI GitHub:      https://github.com/comfyanonymous/ComfyUI
```

---

## 📞 HỖ TRỢ

### Nếu gặp vấn đề:

1. **Đọc tài liệu liên quan:**
   - Setup SSH: `HUONG_DAN_DON_GIAN.md`
   - ComfyUI: `CHAY_COMFYUI.md`
   - Upload/Download: `TAI_FILE.md`

2. **Kiểm tra:**
   - VPS có đang chạy không?
   - SSH key đã setup chưa?
   - Port và IP đúng chưa?

3. **Test kết nối:**
   ```
   Chạy: setup-ssh-key.bat
   Chọn [3] - Test kết nối
   ```

---

## 🎯 CHECKLIST HOÀN CHỈNH

### Setup ban đầu:
- [ ] Tải tất cả file .bat về máy
- [ ] Chạy setup-ssh-key.bat
- [ ] Tạo SSH key
- [ ] Copy public key
- [ ] Thêm key vào Vast.ai
- [ ] Restart VPS
- [ ] Test kết nối thành công

### Sử dụng hàng ngày:
- [ ] Double-click ket-noi-vps.bat
- [ ] Chạy ComfyUI
- [ ] Upload models (nếu cần)
- [ ] Làm việc với ComfyUI
- [ ] Download kết quả
- [ ] Thoát

---

**🎉 CHÚC BẠN SỬ DỤNG VPS THÀNH CÔNG!**

_Tài liệu được tạo tự động. Nếu có câu hỏi, tham khảo các file hướng dẫn chi tiết._
