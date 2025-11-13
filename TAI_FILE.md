# Hướng Dẫn Upload/Download File VPS

## 📤 UPLOAD FILE LÊN VPS

### CÁCH 1: Dùng SCP (Đơn giản nhất)

#### Upload 1 file:
**Trên máy Windows**, mở **Command Prompt** (CMD) và gõ:

```cmd
scp -P 56254 C:\đường\dẫn\file.txt root@47.74.34.39:/workspace/
```

**Ví dụ cụ thể:**
```cmd
REM Upload model từ Desktop lên VPS
scp -P 56254 C:\Users\Admin\Desktop\model.safetensors root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/

REM Upload hình ảnh
scp -P 56254 C:\Users\Admin\Pictures\anh.png root@47.74.34.39:/workspace/
```

#### Upload cả thư mục:
```cmd
scp -P 56254 -r C:\Users\Admin\Desktop\MyFolder root@47.74.34.39:/workspace/
```

**Lưu ý:** `-P` phải viết **HOA**, không phải `-p`

---

### CÁCH 2: Dùng WinSCP (Giao diện kéo thả)

#### Bước 1: Tải WinSCP
- Vào: https://winscp.net/eng/download.php
- Tải bản **Installation package**
- Cài đặt

#### Bước 2: Kết nối VPS
1. Mở WinSCP
2. Điền thông tin:
   - **File protocol:** SFTP
   - **Host name:** `47.74.34.39`
   - **Port number:** `56254`
   - **User name:** `root`
   - **Password:** (để trống, dùng SSH key)
3. Click **Advanced...**
4. Vào **SSH > Authentication**
5. Chọn **Private key file:** `C:\Users\Admin\.ssh\id_ed25519`
6. Click **OK** → **Login**

#### Bước 3: Kéo thả file
- **Bên trái:** Máy Windows
- **Bên phải:** VPS
- **Kéo file** từ trái sang phải để upload!

---

### CÁCH 3: Dùng FileZilla (Tương tự WinSCP)

#### Bước 1: Tải FileZilla
- Vào: https://filezilla-project.org/
- Tải **FileZilla Client**
- Cài đặt

#### Bước 2: Kết nối
1. Mở FileZilla
2. Vào **File > Site Manager**
3. Click **New Site**
4. Điền:
   - **Protocol:** SFTP
   - **Host:** `47.74.34.39`
   - **Port:** `56254`
   - **Logon Type:** Key file
   - **User:** `root`
   - **Key file:** `C:\Users\Admin\.ssh\id_ed25519`
5. Click **Connect**

#### Bước 3: Kéo thả
Kéo file từ local (bên trái) sang VPS (bên phải)

---

### CÁCH 4: Upload qua HTTP (Nếu có Python trên VPS)

#### Trên VPS (trong SSH):
```bash
cd /workspace
python3 -m http.server 8080 --bind 0.0.0.0
```

Rồi dùng tool upload file qua web, hoặc:

#### Trên máy Windows:
```cmd
curl -F "file=@C:\path\to\file.txt" http://localhost:8080/upload
```

---

## 📥 DOWNLOAD FILE VỀ MÁY

### CÁCH 1: Dùng SCP

#### Download 1 file:
**Trên máy Windows (CMD):**
```cmd
scp -P 56254 root@47.74.34.39:/workspace/output.mp4 C:\Users\Admin\Downloads\
```

**Ví dụ:**
```cmd
REM Download kết quả video từ VPS về Desktop
scp -P 56254 root@47.74.34.39:/workspace/ComfyUI/output/video.mp4 C:\Users\Admin\Desktop\

REM Download toàn bộ thư mục output
scp -P 56254 -r root@47.74.34.39:/workspace/ComfyUI/output/ C:\Users\Admin\Desktop\
```

---

### CÁCH 2: Dùng WinSCP/FileZilla

Kéo file từ **phải** (VPS) sang **trái** (Windows)

---

### CÁCH 3: Download qua HTTP

#### Trên VPS (trong SSH):
```bash
cd /workspace/ComfyUI/output
python3 -m http.server 8080
```

#### Trên máy Windows:
1. **Mở trình duyệt**
2. Vào: `http://localhost:8080`
3. Click vào file cần tải
4. Trình duyệt sẽ tải file về!

---

## 🚀 TẠO FILE BAT TỰ ĐỘNG

### Upload file tự động:

Tạo file `upload.bat`:
```batch
@echo off
echo Đang upload file lên VPS...
scp -P 56254 "%~1" root@47.74.34.39:/workspace/
echo Hoàn tất!
pause
```

**Cách dùng:**
- Kéo file vào `upload.bat`
- File sẽ tự động upload lên `/workspace/`

---

### Download file tự động:

Tạo file `download.bat`:
```batch
@echo off
set /p remote_path="Nhập đường dẫn file trên VPS: "
set /p local_path="Nhập nơi lưu (ví dụ: C:\Downloads\): "
echo Đang download...
scp -P 56254 root@47.74.34.39:%remote_path% %local_path%
echo Hoàn tất!
pause
```

**Cách dùng:**
- Double-click `download.bat`
- Nhập đường dẫn file trên VPS
- Nhập nơi lưu trên máy
- Enter!

---

## 📊 UPLOAD/DOWNLOAD FILE LỚN

### Dùng rsync (tốt hơn cho file lớn):

#### Upload với progress bar:
```cmd
rsync -avz --progress -e "ssh -p 56254" C:\path\to\file root@47.74.34.39:/workspace/
```

#### Download với progress bar:
```cmd
rsync -avz --progress -e "ssh -p 56254" root@47.74.34.39:/workspace/file C:\path\to\save\
```

#### Tiếp tục upload file bị gián đoạn:
```cmd
rsync -avz --progress --partial -e "ssh -p 56254" C:\path\to\file root@47.74.34.39:/workspace/
```

---

## 🔧 XỬ LÝ LỖI

### Lỗi: "Permission denied"
**Giải pháp:**
- Kiểm tra SSH key đã setup chưa (xem file HUONG_DAN_SSH_KEY.md)

### Lỗi: "No such file or directory"
**Giải pháp:**
- Kiểm tra đường dẫn có đúng không
- Dùng dấu `\` trên Windows, `/` trên Linux

### Lỗi: "Connection refused"
**Giải pháp:**
- VPS có đang chạy không?
- Port và IP đúng chưa?

---

## 💡 TIPS HỮU ÍCH

### 1. Nén file trước khi upload (nhanh hơn):
```cmd
REM Trên Windows, nén thành .zip trước
REM Rồi upload
scp -P 56254 archive.zip root@47.74.34.39:/workspace/

REM Trên VPS, giải nén
unzip archive.zip
```

### 2. Upload nhiều file cùng lúc:
```cmd
scp -P 56254 C:\file1.txt C:\file2.txt C:\file3.txt root@47.74.34.39:/workspace/
```

### 3. Xem tiến trình upload:
Thêm `-v` để xem chi tiết:
```cmd
scp -v -P 56254 C:\file.txt root@47.74.34.39:/workspace/
```

### 4. Giới hạn băng thông (để không nghẽn mạng):
```cmd
REM Giới hạn 5MB/s
scp -l 40000 -P 56254 C:\file.txt root@47.74.34.39:/workspace/
```

---

## 📋 CHECKLIST NHANH

### Upload file:
```cmd
scp -P 56254 C:\path\to\file root@47.74.34.39:/workspace/
```

### Upload thư mục:
```cmd
scp -P 56254 -r C:\path\to\folder root@47.74.34.39:/workspace/
```

### Download file:
```cmd
scp -P 56254 root@47.74.34.39:/workspace/file C:\path\to\save\
```

### Download thư mục:
```cmd
scp -P 56254 -r root@47.74.34.39:/workspace/folder C:\path\to\save\
```

---

## 🎯 CÁC ĐƯỜNG DẪN QUAN TRỌNG TRÊN VPS

```
/workspace/                          # Thư mục làm việc chính
/workspace/ComfyUI/                  # ComfyUI
/workspace/ComfyUI/models/           # Models
/workspace/ComfyUI/models/checkpoints/  # Stable Diffusion models
/workspace/ComfyUI/models/loras/     # LoRA models
/workspace/ComfyUI/models/vae/       # VAE models
/workspace/ComfyUI/output/           # Kết quả đầu ra
/workspace/ComfyUI/input/            # Hình ảnh input
```

---

**Chúc bạn upload/download thành công!** 🚀
