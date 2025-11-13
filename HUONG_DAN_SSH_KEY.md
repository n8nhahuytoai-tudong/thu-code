# Hướng Dẫn Sửa Lỗi "Permission denied (publickey)"

## ❌ Lỗi bạn đang gặp:
```
root@115.231.176.132: Permission denied (publickey).
```

## 📋 Nguyên nhân:
Vast.ai yêu cầu **SSH Key** để đăng nhập VPS, không cho phép dùng password.

---

## ✅ GIẢI PHÁP - 4 BƯỚC ĐơN GIẢN

### BƯỚC 1: Chạy file setup-ssh-key.bat

1. **Double-click** file `setup-ssh-key.bat`
2. Chọn `[1]` - Tạo SSH Key mới
3. Nhấn **Enter 3 lần** (không cần đặt password)
4. Đợi key được tạo xong

---

### BƯỚC 2: Copy SSH Public Key

1. Trong cùng file `setup-ssh-key.bat`
2. Chọn `[2]` - Xem SSH Public Key
3. **Copy toàn bộ dòng text** (dạng: `ssh-ed25519 AAAA...`)

**Ví dụ:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBCD...xyz123 vastai-key
```

---

### BƯỚC 3: Thêm SSH Key vào Vast.ai

#### Cách 1: Thêm vào Account (Khuyến nghị)

1. Vào: https://cloud.vast.ai/account/
2. Tìm phần **"SSH Keys"** hoặc **"Change SSH Key"**
3. **Paste** key vào ô
4. Click **"Set SSH Key"** hoặc **"Update"**

#### Cách 2: Thêm khi thuê VPS mới

1. Khi thuê instance mới
2. Tìm phần **"SSH Key"**
3. Paste key vào
4. Thuê instance

---

### BƯỚC 4: Restart VPS (QUAN TRỌNG!)

Sau khi thêm key, **BẮT BUỘC** phải restart VPS:

1. Vào: https://cloud.vast.ai/instances/
2. Tìm instance đang chạy
3. Click **"Stop"** hoặc **"Destroy and restart"**
4. Đợi instance dừng hẳn
5. Click **"Start"** lại (nếu chọn Stop)
6. Đợi chuyển sang **"Running"** (màu xanh)

**Lưu ý:** Nếu chọn "Destroy and restart", dữ liệu trên VPS sẽ mất hết!

---

## 🚀 Test Kết Nối

Sau khi restart VPS, test lại:

### Cách 1: Dùng setup-ssh-key.bat
1. Chọn `[3]` - Test kết nối

### Cách 2: Dùng ket-noi-vps.bat
1. Double-click file `ket-noi-vps.bat`
2. Sẽ kết nối không cần password!

---

## 📝 Hướng Dẫn Chi Tiết Từng Bước (Windows)

### Nếu không dùng file .bat, làm thủ công:

#### 1. Tạo SSH Key:
```cmd
REM Mở Command Prompt (CMD)
ssh-keygen -t ed25519 -C "vastai-key"

REM Nhấn Enter 3 lần khi được hỏi
```

#### 2. Xem Public Key:
```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub
```

#### 3. Copy toàn bộ output và paste vào Vast.ai

#### 4. Test kết nối:
```cmd
ssh -p 56254 root@115.231.176.132
```

---

## 🔍 Xử Lý Lỗi Khác

### Lỗi: "Could not open a connection to your authentication agent"

**Giải pháp:**
```cmd
REM Khởi động ssh-agent
start-ssh-agent

REM Thêm key vào agent
ssh-add %USERPROFILE%\.ssh\id_ed25519
```

### Lỗi: "Bad permissions"

**Giải pháp:**
```cmd
REM Cấp quyền đúng cho file key
icacls %USERPROFILE%\.ssh\id_ed25519 /inheritance:r
icacls %USERPROFILE%\.ssh\id_ed25519 /grant:r "%USERNAME%:R"
```

### Lỗi: "Connection timed out"

**Nguyên nhân:**
- VPS đã tắt
- Port hoặc IP sai

**Giải pháp:**
1. Kiểm tra VPS có Running không
2. Kiểm tra lại thông tin SSH từ Vast.ai

---

## 💡 Tips Hữu Ích

### 1. SSH Key chỉ cần tạo 1 lần
- Dùng được cho nhiều VPS
- Không cần tạo lại mỗi lần

### 2. Sao lưu SSH Key
- Copy folder `.ssh` sang USB
- Khi đổi máy, copy lại vào `%USERPROFILE%\.ssh\`

### 3. Dùng SSH Config (Nâng cao)
```cmd
REM Tạo file config
notepad %USERPROFILE%\.ssh\config
```

Nội dung:
```
Host myvps
    HostName 115.231.176.132
    Port 56254
    User root
    IdentityFile ~/.ssh/id_ed25519
    LocalForward 8080 localhost:8080
    LocalForward 8188 localhost:8188
```

Kết nối chỉ cần:
```cmd
ssh myvps
```

---

## 🎯 Checklist Hoàn Chỉnh

- [ ] Chạy `setup-ssh-key.bat`
- [ ] Chọn [1] - Tạo SSH Key
- [ ] Chọn [2] - Copy Public Key
- [ ] Vào Vast.ai → Account → Thêm SSH Key
- [ ] Restart VPS (Stop → Start)
- [ ] Đợi VPS chuyển sang "Running"
- [ ] Chọn [3] - Test kết nối
- [ ] Hoặc chạy `ket-noi-vps.bat`
- [ ] Thành công! 🎉

---

## 📞 Nếu Vẫn Không Được

Kiểm tra:

1. **SSH Key đã được thêm vào Vast.ai chưa?**
   - Vào: https://cloud.vast.ai/account/
   - Xem phần SSH Keys có key chưa

2. **VPS đã restart sau khi thêm key chưa?**
   - Bắt buộc phải restart!

3. **File key có tồn tại không?**
   ```cmd
   dir %USERPROFILE%\.ssh\
   ```
   Phải thấy: `id_ed25519` và `id_ed25519.pub`

4. **Thông tin SSH còn đúng không?**
   - Check lại port và IP từ Vast.ai dashboard

---

**Sau khi làm xong 4 bước trên, bạn sẽ kết nối được không cần password!** ✅
