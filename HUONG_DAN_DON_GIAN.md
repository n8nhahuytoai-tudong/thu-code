# HƯỚNG DẪN KẾT NỐI VPS - CỰC KỲ ĐƠN GIẢN

## ❌ LỖI BẠN ĐANG GẶP:
```
Permission denied (publickey)
```

## ✅ GIẢI PHÁP - 5 BƯỚC ĐƠN GIẢN:

---

## BƯỚC 1: MỞ COMMAND PROMPT

### Cách 1: Tìm kiếm
1. Nhấn nút **Windows** trên bàn phím (hoặc click nút Start)
2. Gõ: **cmd**
3. Click vào **Command Prompt** (màu đen)

### Cách 2: Dùng phím tắt
1. Nhấn **Windows + R**
2. Gõ: **cmd**
3. Nhấn **Enter**

→ Sẽ mở 1 cửa sổ màu đen

---

## BƯỚC 2: TẠO SSH KEY

### Trong cửa sổ Command Prompt (màu đen):

1. **Copy dòng này** (click chuột phải để paste vào CMD):
```
ssh-keygen -t ed25519 -C "vastai-key"
```

2. Nhấn **Enter**

3. Sẽ hỏi 3 câu, **CẢ 3 LẦN ĐỀU NHẤN ENTER** (không cần gõ gì):
   - Câu 1: `Enter file...` → Nhấn **Enter**
   - Câu 2: `Enter passphrase...` → Nhấn **Enter**
   - Câu 3: `Enter same passphrase...` → Nhấn **Enter**

4. Xong! Sẽ thấy chữ "Your public key has been saved..."

---

## BƯỚC 3: XEM VÀ COPY SSH KEY

### Tiếp tục trong cửa sổ Command Prompt:

1. **Copy và paste dòng này:**
```
type %USERPROFILE%\.ssh\id_ed25519.pub
```

2. Nhấn **Enter**

3. Sẽ hiện ra 1 dòng text DÀI, bắt đầu bằng `ssh-ed25519`

**VÍ DỤ:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGbZ8EmjkVV... vastai-key
```

4. **CHỌN TOÀN BỘ DÒNG TEXT ĐÓ:**
   - Dùng chuột kéo từ đầu chữ `ssh` đến hết
   - Hoặc nhấn chuột phải → chọn **Select All**
   - Nhấn chuột phải lần nữa → chọn **Copy**

---

## BƯỚC 4: THÊM KEY VÀO VAST.AI

### Mở trình duyệt (Chrome/Edge/Firefox):

1. **Vào trang này:**
```
https://cloud.vast.ai/account/
```

2. **Đăng nhập** tài khoản Vast.ai (nếu chưa đăng nhập)

3. **Tìm phần "SSH Key":**
   - Cuộn xuống tìm chữ **"SSH Key"** hoặc **"Change SSH Key"**
   - Có 1 ô trắng lớn để nhập text

4. **Xóa hết** text cũ trong ô đó (nếu có)

5. **Paste key vào:**
   - Click vào ô trắng
   - Nhấn **Ctrl + V** (hoặc chuột phải → Paste)
   - Key sẽ hiện ra trong ô

6. **Click nút "Set SSH Key"** hoặc **"Update"** hoặc **"Save"**

7. Thấy thông báo thành công → **Xong Bước 4!**

---

## BƯỚC 5: RESTART VPS

### Vẫn trên trình duyệt:

1. **Vào trang này:**
```
https://cloud.vast.ai/instances/
```

2. Sẽ thấy **danh sách VPS** của bạn

3. Tìm VPS đang chạy (có chữ **"Running"** màu xanh)

4. **Click vào VPS đó** (click vào bất kỳ chỗ nào trong hàng)

5. Sẽ thấy nhiều nút, tìm nút **"Stop"** hoặc **"Destroy"**

6. **Click "Stop"**

7. Đợi khoảng **30 giây - 1 phút**

8. VPS sẽ chuyển sang **"Stopped"** (màu xám/đỏ)

9. **Click nút "Start"** (nút cũ đã đổi thành Start)

10. Đợi VPS chuyển lại thành **"Running"** (màu xanh)

11. **Xong!**

---

## BƯỚC 6: KẾT NỐI LẠI

### Bây giờ chạy lại file .bat:

1. **Tải file này về máy:**
   - File tên: **ket-noi-vps.bat**
   - (Đã có trong repo)

2. **Double-click** vào file đó

3. Lần này sẽ **KHÔNG BỊ LỖI** nữa!

4. Sẽ thấy dòng chữ:
```
Welcome to vast.ai...
root@...
```

5. **THÀNH CÔNG!** Bạn đã vào VPS! 🎉

---

## NẾU VẪN BÁO LỖI:

### Kiểm tra lại:

**1. Đã copy đúng key chưa?**
   - Key phải bắt đầu bằng `ssh-ed25519`
   - Key phải copy HẾT, không bỏ sót

**2. Đã click "Set SSH Key" chưa?**
   - Vào lại: https://cloud.vast.ai/account/
   - Xem ô SSH Key có key chưa?

**3. Đã restart VPS chưa?**
   - **QUAN TRỌNG!** Phải Stop → đợi dừng hẳn → Start lại
   - Không restart sẽ không nhận key mới!

**4. VPS có đang Running không?**
   - Vào: https://cloud.vast.ai/instances/
   - Phải thấy chữ "Running" màu xanh

---

## TÓM TẮT 5 BƯỚC:

```
1. Mở CMD → Gõ: ssh-keygen -t ed25519 -C "vastai-key" → Enter 3 lần

2. Gõ: type %USERPROFILE%\.ssh\id_ed25519.pub → Copy dòng text

3. Vào: https://cloud.vast.ai/account/ → Paste key → Click "Set SSH Key"

4. Vào: https://cloud.vast.ai/instances/ → Stop VPS → Start lại

5. Double-click file ket-noi-vps.bat → Thành công!
```

---

## NẾU KHÔNG HIỂU, GỌI TÔI!

Bạn bị kẹt ở bước nào? Cho tôi biết:
- Bước mấy?
- Lỗi gì?
- Screenshot màn hình?

Tôi sẽ giúp cụ thể hơn! 😊
