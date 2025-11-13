# Hướng Dẫn Chạy ComfyUI Trên VPS

## 🚀 CÁCH 1: CHẠY COMFYUI ĐƠN GIẢN

### Bước 1: Kết nối VPS
- Double-click file **ket-noi-vps.bat**
- Đợi kết nối thành công (thấy dòng `root@...:/workspace$`)

### Bước 2: Kiểm tra ComfyUI có sẵn chưa
Gõ lệnh:
```bash
ls -la /workspace/
```

Nếu thấy thư mục **ComfyUI** → Đã có sẵn, qua Bước 3

Nếu không thấy → Cần cài đặt, xem **CÁCH 2** ở dưới

### Bước 3: Vào thư mục ComfyUI
```bash
cd /workspace/ComfyUI
```

### Bước 4: Chạy ComfyUI
```bash
python main.py --listen 0.0.0.0 --port 8080
```

### Bước 5: Mở ComfyUI trên trình duyệt
1. **Mở trình duyệt** (Chrome/Edge/Firefox) trên máy Windows
2. Vào địa chỉ:
```
http://localhost:8080
```

### ✅ Xong! ComfyUI đã chạy!

---

## 🔧 CÁCH 2: CÀI ĐẶT COMFYUI (NẾU CHƯA CÓ)

### Bước 1: Clone ComfyUI từ GitHub
```bash
cd /workspace
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ComfyUI
```bash
python main.py --listen 0.0.0.0 --port 8080
```

### Bước 4: Mở trình duyệt
Vào:
```
http://localhost:8080
```

---

## 🎨 CHẠY COMFYUI NỀN (KHÔNG SỢ MẤT KẾT NỐI)

### Cách 1: Dùng tmux (Khuyến nghị)

#### Cài tmux:
```bash
apt update && apt install tmux -y
```

#### Tạo session mới:
```bash
tmux new -s comfy
```

#### Chạy ComfyUI trong tmux:
```bash
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8080
```

#### Thoát tmux (ComfyUI vẫn chạy):
Nhấn phím: **Ctrl + B**, rồi nhấn **D**

#### Quay lại tmux:
```bash
tmux attach -s comfy
```

#### Dừng tmux:
```bash
tmux kill-session -t comfy
```

### Cách 2: Dùng nohup

```bash
cd /workspace/ComfyUI
nohup python main.py --listen 0.0.0.0 --port 8080 > comfy.log 2>&1 &
```

Xem log:
```bash
tail -f comfy.log
```

Dừng:
```bash
pkill -f "python main.py"
```

---

## 📦 TẢI MODELS CHO COMFYUI

### 1. Tải model từ Hugging Face:
```bash
cd /workspace/ComfyUI/models/checkpoints

# Ví dụ: Tải Stable Diffusion 1.5
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors
```

### 2. Tải model từ Civitai:
```bash
cd /workspace/ComfyUI/models/checkpoints

# Copy link download từ Civitai, dán vào wget
wget "https://civitai.com/api/download/models/XXXXX" -O model-name.safetensors
```

### 3. Upload model từ máy local (xem file TAI_FILE.md)

---

## 🛑 DỪNG COMFYUI

### Nếu chạy thường:
Nhấn: **Ctrl + C** trong terminal

### Nếu chạy bằng tmux:
```bash
tmux kill-session -t comfy
```

### Nếu chạy bằng nohup:
```bash
pkill -f "python main.py"
```

---

## 🔍 XỬ LÝ LỖI

### Lỗi: "Address already in use"
**Nguyên nhân:** Port 8080 đang được dùng

**Giải pháp:**
```bash
# Tìm process đang dùng port 8080
lsof -i :8080

# Kill process
kill -9 <PID>

# Hoặc đổi port khác
python main.py --listen 0.0.0.0 --port 8188
```

### Lỗi: "No module named 'torch'"
**Giải pháp:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Lỗi: "CUDA out of memory"
**Giải pháp:**
```bash
# Chạy với low VRAM mode
python main.py --listen 0.0.0.0 --port 8080 --lowvram
```

### Không mở được localhost:8080
**Kiểm tra:**
1. ComfyUI có đang chạy không? (xem terminal)
2. Port forwarding đúng chưa? (phải có `-L 8080:localhost:8080` khi SSH)
3. Chạy lại file ket-noi-vps.bat

---

## 📊 KIỂM TRA TÀI NGUYÊN

### Xem GPU:
```bash
nvidia-smi
watch -n 1 nvidia-smi  # Refresh mỗi giây
```

### Xem RAM:
```bash
free -h
```

### Xem dung lượng đĩa:
```bash
df -h
```

### Xem CPU:
```bash
htop
```

---

## 💡 TIPS HỮU ÍCH

### 1. Tự động khởi động ComfyUI
Tạo script:
```bash
cat > /workspace/start-comfy.sh << 'EOF'
#!/bin/bash
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8080
EOF

chmod +x /workspace/start-comfy.sh
```

Chạy:
```bash
/workspace/start-comfy.sh
```

### 2. Xem log ComfyUI
```bash
cd /workspace/ComfyUI
tail -f comfy.log
```

### 3. Backup models
```bash
cd /workspace/ComfyUI/models
tar -czf models-backup.tar.gz checkpoints/ loras/ vae/
```

### 4. Giải phóng RAM/VRAM
```bash
# Clear cache
sync; echo 3 > /proc/sys/vm/drop_caches

# Kill các process không dùng
pkill -f idle
```

---

## 🎯 CHECKLIST NHANH

- [ ] Kết nối VPS: `ket-noi-vps.bat`
- [ ] Vào thư mục: `cd /workspace/ComfyUI`
- [ ] Chạy ComfyUI: `python main.py --listen 0.0.0.0 --port 8080`
- [ ] Mở browser: `http://localhost:8080`
- [ ] Tải models vào: `/workspace/ComfyUI/models/checkpoints/`
- [ ] Bắt đầu sáng tạo! 🎨

---

**Chúc bạn sử dụng ComfyUI thành công!** 🚀
