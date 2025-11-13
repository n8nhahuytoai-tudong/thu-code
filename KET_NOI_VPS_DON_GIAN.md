# Hướng Dẫn Kết Nối VPS Đơn Giản Nhất

## Thông tin VPS của bạn
- **Host:** ssh6.vast.ai
- **Port:** 30195
- **User:** root
- **Port Forward:** 8080:localhost:8080

---

## 🚀 Cách 1: Tạo SSH Config (KHUYẾN NGHỊ - DỄ NHẤT)

### Bước 1: Tạo/sửa file SSH config
```bash
# Mở file config
nano ~/.ssh/config
# hoặc
code ~/.ssh/config
```

### Bước 2: Thêm cấu hình này vào file:
```
Host myvps
    HostName ssh6.vast.ai
    Port 30195
    User root
    LocalForward 8080 localhost:8080
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Bước 3: Kết nối siêu đơn giản:
```bash
ssh myvps
```

**Chỉ cần gõ 2 chữ!** Không cần nhớ port, host, user gì cả! 🎉

---

## 🔑 Cách 2: Tạo SSH Key (Không cần nhập password)

### Bước 1: Tạo SSH key (nếu chưa có)
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Nhấn Enter 3 lần (không cần password)
```

### Bước 2: Copy key lên VPS
```bash
ssh-copy-id -p 30195 root@ssh6.vast.ai
```

### Bước 3: Kết nối (không cần password nữa!)
```bash
ssh myvps
# hoặc nếu chưa setup config:
ssh -p 30195 root@ssh6.vast.ai
```

---

## 📝 Cách 3: Tạo Script/Alias Nhanh

### Thêm alias vào ~/.bashrc hoặc ~/.zshrc:
```bash
# Mở file
nano ~/.bashrc  # hoặc ~/.zshrc nếu dùng zsh

# Thêm dòng này vào cuối file:
alias vps='ssh -p 30195 root@ssh6.vast.ai -L 8080:localhost:8080'
```

### Reload config:
```bash
source ~/.bashrc  # hoặc source ~/.zshrc
```

### Kết nối:
```bash
vps
```

---

## 💻 Cách 4: Dùng VS Code Remote SSH (Coding trên VPS)

### Bước 1: Cài extension
- Mở VS Code
- Cài extension: **Remote - SSH** (của Microsoft)

### Bước 2: Kết nối
1. Nhấn `F1` hoặc `Ctrl+Shift+P`
2. Gõ: `Remote-SSH: Connect to Host`
3. Chọn `Configure SSH Hosts...`
4. Chọn `~/.ssh/config`
5. Thêm config như Cách 1 ở trên
6. Lưu file
7. Nhấn `F1` lại, chọn `Remote-SSH: Connect to Host`
8. Chọn `myvps`

**Bây giờ bạn code trực tiếp trên VPS như máy local!** 🎨

---

## 🔧 Cách 5: Script Tự Động Kết Nối

### Tạo file script:
```bash
nano ~/connect-vps.sh
```

### Nội dung:
```bash
#!/bin/bash
echo "🚀 Đang kết nối VPS..."
ssh -p 30195 root@ssh6.vast.ai -L 8080:localhost:8080
```

### Cấp quyền thực thi:
```bash
chmod +x ~/connect-vps.sh
```

### Kết nối:
```bash
~/connect-vps.sh
```

---

## ⚡ KẾT HỢP TẤT CẢ (GIẢI PHÁP HOÀN HẢO)

### 1. Setup lần đầu:
```bash
# Tạo SSH key
ssh-keygen -t ed25519 -C "vps-key"

# Copy key lên VPS
ssh-copy-id -p 30195 root@ssh6.vast.ai

# Tạo SSH config
cat >> ~/.ssh/config << 'EOF'

Host myvps
    HostName ssh6.vast.ai
    Port 30195
    User root
    IdentityFile ~/.ssh/id_ed25519
    LocalForward 8080 localhost:8080
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes

EOF

# Tạo alias
echo "alias vps='ssh myvps'" >> ~/.bashrc
source ~/.bashrc
```

### 2. Từ giờ chỉ cần:
```bash
vps
```

**Xong! Kết nối trong 1 giây!** ⚡

---

## 🎯 So Sánh Các Cách

| Phương pháp | Độ dễ | Tốc độ | Tính năng |
|-------------|-------|--------|-----------|
| **SSH Config** | ⭐⭐⭐⭐⭐ | Nhanh | Tốt nhất |
| **SSH Key** | ⭐⭐⭐⭐ | Nhanh | Bảo mật |
| **Alias** | ⭐⭐⭐⭐⭐ | Nhanh | Đơn giản |
| **VS Code** | ⭐⭐⭐⭐⭐ | Trung bình | Code trực tiếp |
| **Script** | ⭐⭐⭐ | Nhanh | Tùy biến |

---

## 🛠️ Bonus: Các lệnh hữu ích sau khi kết nối

### Kiểm tra hệ thống:
```bash
# Xem tài nguyên
htop

# Xem GPU
nvidia-smi

# Xem dung lượng
df -h

# Xem RAM
free -h
```

### Chạy lệnh dài (không sợ mất kết nối):
```bash
# Cài tmux
apt install tmux

# Chạy session
tmux new -s work

# Detach: Ctrl+B rồi nhấn D
# Attach lại: tmux attach -t work
```

### Upload/Download nhanh:
```bash
# Từ máy local upload lên VPS
scp -P 30195 file.txt root@ssh6.vast.ai:/workspace/

# Từ VPS download về
scp -P 30195 root@ssh6.vast.ai:/workspace/output.mp4 ./
```

---

## 🎓 Khuyến nghị của tôi

**Làm theo thứ tự này:**

1. ✅ Setup SSH Config (Cách 1)
2. ✅ Tạo SSH Key (Cách 2)
3. ✅ Thêm alias `vps` (Cách 3)
4. ✅ Cài VS Code Remote SSH nếu cần code (Cách 4)

**Kết quả:**
- Kết nối chỉ cần gõ: `vps`
- Không cần nhập password
- Code trực tiếp trên VPS bằng VS Code
- Tự động forward port 8080

---

## ❓ Xử lý lỗi thường gặp

### Lỗi "Connection refused":
```bash
# Kiểm tra VPS có đang chạy không
ping ssh6.vast.ai
```

### Lỗi "Permission denied":
```bash
# Kiểm tra quyền file key
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 700 ~/.ssh
```

### Lỗi "Port already in use":
```bash
# Tìm process đang dùng port 8080
lsof -i :8080
# hoặc
netstat -tulpn | grep 8080

# Kill process
kill -9 <PID>
```

---

**Chúc bạn kết nối thành công! 🎊**
