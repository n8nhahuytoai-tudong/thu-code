# 🎨 HƯỚNG DẪN UPLOAD MODEL LÊN VPS - CỰC KỲ ĐƠN GIẢN

## ⚡ CÁCH 1: DÙNG FILE BAT (DỄ NHẤT!)

### Bước 1: Tải file upload-file.bat về máy
- File này đã có trong repo
- Tải về Desktop để dễ tìm

### Bước 2: Double-click file upload-file.bat

### Bước 3: Chọn [3] - Upload vào thư mục models

### Bước 4: Kéo file model vào cửa sổ CMD
- Hoặc nhập đường dẫn: `C:\Users\Admin\Desktop\model.safetensors`
- Nhấn Enter

### Bước 5: Đợi upload xong
- Sẽ thấy thanh tiến trình
- Khi xong, model đã sẵn sàng để dùng!

**✅ XONG! Model đã trong VPS!**

---

## 💻 CÁCH 2: DÙNG LỆNH TRỰC TIẾP

### Bước 1: Mở Command Prompt (CMD)
- Nhấn Windows + R
- Gõ: `cmd`
- Enter

### Bước 2: Gõ lệnh này (thay đường dẫn file của bạn):

```cmd
scp -P 56254 "C:\Users\Admin\Desktop\model.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/
```

**Lưu ý:**
- Thay `C:\Users\Admin\Desktop\model.safetensors` bằng đường dẫn thật của model
- Dùng dấu ngoặc kép `"..."` nếu đường dẫn có khoảng trắng

### Bước 3: Nhấn Enter và đợi

**✅ XONG!**

---

## 📂 CÁC LOẠI MODEL VÀ NƠI LƯU

### 1. Stable Diffusion Models (Checkpoints):
```
Upload vào: /workspace/ComfyUI/models/checkpoints/
```
**File:** `.safetensors`, `.ckpt`, `.pt`

**Ví dụ:**
```cmd
scp -P 56254 "C:\Models\sd_v1.5.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/
```

### 2. LoRA Models:
```
Upload vào: /workspace/ComfyUI/models/loras/
```
**File:** `.safetensors`, `.pt`

**Ví dụ:**
```cmd
scp -P 56254 "C:\Models\lora_style.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/loras/
```

### 3. VAE Models:
```
Upload vào: /workspace/ComfyUI/models/vae/
```
**File:** `.safetensors`, `.pt`

**Ví dụ:**
```cmd
scp -P 56254 "C:\Models\vae.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/vae/
```

### 4. ControlNet Models:
```
Upload vào: /workspace/ComfyUI/models/controlnet/
```

### 5. Upscale Models (ESRGAN):
```
Upload vào: /workspace/ComfyUI/models/upscale_models/
```

---

## 🎯 VÍ DỤ CỤ THỂ

### Ví dụ 1: Upload model từ Desktop

```cmd
cd Desktop
scp -P 56254 "realistic_v5.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/
```

### Ví dụ 2: Upload LoRA từ Downloads

```cmd
scp -P 56254 "C:\Users\Admin\Downloads\anime_lora.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/loras/
```

### Ví dụ 3: Upload nhiều file cùng lúc

```cmd
scp -P 56254 model1.safetensors model2.safetensors model3.safetensors root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/
```

### Ví dụ 4: Upload cả thư mục models

```cmd
scp -P 56254 -r "C:\MyModels\" root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/
```

---

## 📊 UPLOAD FILE LỚN (Có thanh tiến trình)

Nếu model rất lớn (vài GB), dùng lệnh này để thấy tiến trình:

```cmd
scp -P 56254 -v "C:\large_model.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/
```

Thêm `-v` để thấy chi tiết upload

---

## ✅ KIỂM TRA MODEL ĐÃ UPLOAD CHƯA

### Cách 1: Dùng download-file.bat
```
1. Double-click download-file.bat
2. Chọn [4] - Liệt kê file trên VPS
3. Chọn [3] - Liệt kê models
```

### Cách 2: Dùng SSH
```
1. Double-click ket-noi-vps.bat
2. Kết nối vào VPS
3. Gõ: ls -lh /workspace/ComfyUI/models/checkpoints/
```

Bạn sẽ thấy danh sách model!

---

## 🚀 SAU KHI UPLOAD XONG

### Bước 1: Kết nối VPS
```
Double-click: ket-noi-vps.bat
```

### Bước 2: Chạy ComfyUI
```bash
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8080
```

### Bước 3: Mở ComfyUI
```
Browser: http://localhost:8080
```

### Bước 4: Chọn model
- Trong ComfyUI, tìm node **"Load Checkpoint"**
- Click dropdown
- Chọn model bạn vừa upload
- **XONG!** Bắt đầu tạo ảnh! 🎨

---

## ⏱️ THỜI GIAN UPLOAD DỰ KIẾN

| Kích thước model | Tốc độ 10MB/s | Tốc độ 50MB/s | Tốc độ 100MB/s |
|------------------|---------------|---------------|----------------|
| 2GB              | ~3.5 phút     | ~40 giây      | ~20 giây       |
| 4GB              | ~7 phút       | ~1.5 phút     | ~40 giây       |
| 7GB              | ~12 phút      | ~2.5 phút     | ~1 phút        |
| 15GB             | ~25 phút      | ~5 phút       | ~2.5 phút      |

*Thời gian tùy thuộc vào tốc độ mạng của bạn*

---

## 🔍 XỬ LÝ LỖI

### ❌ Lỗi: "No such file or directory"
**Nguyên nhân:** Thư mục đích chưa tồn tại

**Giải pháp:**
```bash
# SSH vào VPS
ssh -p 56254 root@47.74.34.39

# Tạo thư mục
mkdir -p /workspace/ComfyUI/models/checkpoints
mkdir -p /workspace/ComfyUI/models/loras
mkdir -p /workspace/ComfyUI/models/vae

# Upload lại
```

### ❌ Lỗi: "Permission denied"
**Giải pháp:** Xem file `HUONG_DAN_DON_GIAN.md` để setup SSH key

### ❌ Upload bị ngắt giữa chừng
**Giải pháp:** Dùng rsync để tiếp tục upload:
```cmd
rsync -avz --progress --partial -e "ssh -p 56254" "C:\model.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/
```

---

## 💡 TIPS HỮU ÍCH

### 1. Nén model trước khi upload (nhanh hơn):
```cmd
REM Trên Windows, nén thành .zip
REM Upload file .zip
scp -P 56254 models.zip root@47.74.34.39:/workspace/

REM Trên VPS, giải nén
ssh -p 56254 root@47.74.34.39
cd /workspace
unzip models.zip -d ComfyUI/models/checkpoints/
```

### 2. Upload từ Google Drive/Mega:
```bash
# SSH vào VPS
ssh -p 56254 root@47.74.34.39

# Tải trực tiếp từ link
cd /workspace/ComfyUI/models/checkpoints
wget "https://link-to-model.com/model.safetensors"
```

### 3. Upload từ Hugging Face:
```bash
# SSH vào VPS
cd /workspace/ComfyUI/models/checkpoints

# Tải từ Hugging Face
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors
```

### 4. Upload từ Civitai:
```bash
# SSH vào VPS
cd /workspace/ComfyUI/models/checkpoints

# Copy link download từ Civitai, dán vào wget
wget "https://civitai.com/api/download/models/XXXXX" -O model-name.safetensors
```

---

## 🎯 CHECKLIST UPLOAD MODEL

- [ ] Chuẩn bị file model trên máy Windows
- [ ] Xác định loại model (Checkpoint/LoRA/VAE)
- [ ] Biết đường dẫn lưu trên VPS
- [ ] Chạy upload-file.bat hoặc dùng lệnh SCP
- [ ] Đợi upload hoàn tất
- [ ] Kiểm tra model đã có trên VPS
- [ ] Chạy ComfyUI
- [ ] Test model trong ComfyUI
- [ ] Bắt đầu sáng tạo! 🎨

---

## 📞 CẦN GIÚP ĐỠ?

### Nếu upload không được:

1. **Kiểm tra kết nối:**
   ```cmd
   ping 47.74.34.39
   ```

2. **Kiểm tra VPS có chạy không:**
   - Vào: https://cloud.vast.ai/instances/
   - Xem status có "Running" không

3. **Test SSH:**
   ```cmd
   ssh -p 56254 root@47.74.34.39
   ```

4. **Xem log chi tiết:**
   ```cmd
   scp -v -P 56254 file.txt root@47.74.34.39:/workspace/
   ```

---

**🎉 CHÚC BẠN UPLOAD MODEL THÀNH CÔNG!**

_Sau khi upload xong, đừng quên chạy ComfyUI để test model nhé!_
