# 🎯 HƯỚNG DẪN ĐƠN GIẢN NHẤT - CHỈ COPY & PASTE

## 📌 BẠN ĐANG Ở ĐÂU?

Bạn thấy dòng chữ này trong màn hình đen:
```
(main) root@C.27832257:/workspace$
```

➡️ **Nghĩa là:** Bạn đã VÀO VPS thành công rồi! 🎉

---

## 🎨 MUỐN CHẠY COMFYUI?

### Bước 1: Copy dòng này
```bash
ls /workspace/ComfyUI
```

### Bước 2: Paste vào màn hình đen (cửa sổ SSH)
- **Cách paste:** Click chuột phải
- Hoặc nhấn: **Shift + Insert**

### Bước 3: Nhấn **Enter**

### Bạn sẽ thấy 1 trong 2 trường hợp:

#### ✅ Trường hợp 1: Thấy nhiều chữ (main.py, models, output...)
➡️ **Có ComfyUI rồi!** Làm tiếp bước dưới

#### ❌ Trường hợp 2: Báo lỗi "No such file or directory"
➡️ **Chưa có ComfyUI**, cần cài đặt

**→ Hãy cho tôi biết bạn gặp trường hợp nào?**

---

## 🚀 NẾU ĐÃ CÓ COMFYUI (Trường hợp 1):

### Copy từng dòng này, paste vào, nhấn Enter:

```bash
cd /workspace/ComfyUI
```
*(Vào thư mục ComfyUI)*

```bash
python main.py --listen 0.0.0.0 --port 8080
```
*(Chạy ComfyUI)*

### Đợi khoảng 10-30 giây, sẽ thấy dòng chữ:
```
To see the GUI go to: http://0.0.0.0:8080
```

### Mở trình duyệt trên Windows, vào:
```
http://localhost:8080
```

**🎉 XONG! ComfyUI đã chạy!**

---

## 📥 NẾU CHƯA CÓ COMFYUI (Trường hợp 2):

### Copy từng dòng, paste, nhấn Enter (chờ mỗi lệnh chạy xong):

```bash
cd /workspace
```

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
```
*(Đợi khoảng 1-2 phút)*

```bash
cd ComfyUI
```

```bash
pip install -r requirements.txt
```
*(Đợi khoảng 3-5 phút)*

```bash
python main.py --listen 0.0.0.0 --port 8080
```

### Mở trình duyệt:
```
http://localhost:8080
```

**🎉 XONG!**

---

## 📦 TẢI MODEL (Sau khi ComfyUI đã chạy)

### MỞ CỬA SỔ CMD MỚI (không đóng cửa sổ cũ)

1. Nhấn **Windows + R**
2. Gõ: **cmd**
3. Nhấn **Enter**

### Trong cửa sổ CMD mới, gõ:

```cmd
scp -P 56254 "C:\Users\Admin\Desktop\model.safetensors" root@47.74.34.39:/workspace/ComfyUI/models/checkpoints/
```

**LƯU Ý:**
- Thay `C:\Users\Admin\Desktop\model.safetensors` bằng vị trí file model của bạn
- Hoặc kéo file model vào cửa sổ CMD để tự động điền đường dẫn

### Hoặc đơn giản hơn: Dùng file upload-file.bat

1. Double-click file **upload-file.bat**
2. Chọn **[3]** - Upload model
3. Kéo file model vào
4. Enter

**🎉 XONG!**

---

## 🛑 DỪNG COMFYUI

Trong cửa sổ SSH (màu đen đang chạy ComfyUI):
- Nhấn: **Ctrl + C**

---

## 🔄 CHẠY LẠI COMFYUI

### Copy paste 2 dòng này:

```bash
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8080
```

---

## ❓ CÂU HỎI THƯỜNG GẶP

### Q: Tôi paste lệnh vào nhưng không thấy gì?
**A:** Đó là bình thường! SSH không hiển thị text khi paste. Cứ paste xong nhấn **Enter**

### Q: Làm sao biết lệnh đã chạy xong?
**A:** Khi thấy dòng `root@...:/workspace$` xuất hiện lại ➡️ Lệnh đã xong

### Q: Lỡ đóng cửa sổ SSH?
**A:** Không sao! Mở lại file **ket-noi-vps.bat** là được

### Q: ComfyUI không mở được?
**A:**
1. Kiểm tra cửa sổ SSH có đang chạy ComfyUI không (thấy nhiều dòng chữ xuất hiện)
2. Đợi thêm 30 giây
3. Refresh trình duyệt (F5)

---

## 📋 TÓM TẮT SIÊU NHANH

```
1. Mở ket-noi-vps.bat → Kết nối VPS
2. Paste: cd /workspace/ComfyUI
3. Paste: python main.py --listen 0.0.0.0 --port 8080
4. Mở browser: http://localhost:8080
5. XONG!
```

---

**🎯 BÂY GIỜ HÃY THỬ BƯỚC 1:**

Paste dòng này vào cửa sổ SSH của bạn:
```bash
ls /workspace/ComfyUI
```

Rồi cho tôi biết bạn thấy gì! 😊
