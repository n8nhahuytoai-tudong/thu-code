# 🚀 HƯỚNG DẪN NHANH - ENCODE TOÀN BỘ VIDEO

## ⚡ Cách dùng (Windows)

### Bước 1: Double click file này
```
run_video_to_json_full.ps1
```

### Bước 2: Chọn video
- Hộp thoại mở ra → chọn file `1234.mp4`

### Bước 3: Chọn chế độ
```
1 - FULL (khuyến nghị) → Mỗi 2 giây, ~20 frames
2 - DETAILED → Mỗi 1 giây, ~40 frames
3 - VERY DETAILED → Mỗi 0.5 giây, ~80 frames
```

**→ Nhập số `1` rồi Enter**

### Bước 4: Đợi
- Script sẽ chạy 1-2 phút
- File `1234_full.json` sẽ được tạo (~15-20 MB)

### Bước 5: Upload lên GitHub
```bash
git add 1234_full.json
git commit -m "Add full 40s video JSON"
git push
```

## ✅ XONG!

File JSON sẽ chứa **toàn bộ 40s video**, tôi sẽ xem và viết prompts chính xác!

---

## 🐛 Nếu gặp lỗi PowerShell

### Lỗi: "cannot be loaded because running scripts is disabled"

Mở PowerShell as Administrator và chạy:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Sau đó chạy lại script.

---

## 📝 Hoặc chạy trực tiếp Python

```bash
python video_to_json_full.py 1234.mp4 --interval 120
```

Đơn giản vậy thôi! 🎬
