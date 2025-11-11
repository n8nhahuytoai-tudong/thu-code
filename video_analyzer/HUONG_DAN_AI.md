# 🤖 Hướng dẫn sử dụng AI để phân tích chi tiết

## ⚠️ Tại sao báo cáo "Chưa có mô tả"?

Nếu báo cáo của bạn hiển thị **"Chưa có mô tả"** cho tất cả các cảnh, đó là vì bạn đã chọn chế độ **KHÔNG AI** (option [3] hoặc [4]).

```
Cảnh 1: Chưa có mô tả
Cảnh 2: Chưa có mô tả
...
```

Để có **mô tả chi tiết** cho từng cảnh, bạn cần:
1. ✅ Có API key từ Anthropic
2. ✅ Chạy ở chế độ **CÓ AI** (option [1] hoặc [2])

---

## 📝 Cách lấy API Key từ Anthropic

### Bước 1: Đăng ký tài khoản

1. Truy cập: https://console.anthropic.com/
2. Đăng ký tài khoản mới (hoặc đăng nhập nếu đã có)
3. Xác nhận email

### Bước 2: Lấy API Key

1. Vào **Settings** → **API Keys**
2. Click **Create Key**
3. Đặt tên cho key (ví dụ: "Video Analyzer")
4. Copy key (bắt đầu với `sk-ant-...`)

⚠️ **LƯU Ý:** Key chỉ hiển thị 1 lần, hãy lưu lại ngay!

### Bước 3: Cấu hình API Key

**Cách 1: Tạo file .env** (khuyến nghị)

```bash
# Trong thư mục video_analyzer
notepad .env
```

Thêm vào file:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

**Cách 2: Set biến môi trường** (Windows)

```bash
setx ANTHROPIC_API_KEY "sk-ant-api03-xxxxxxxxxxxxx"
```

Sau đó **khởi động lại terminal**.

---

## 🎯 Cách chạy với AI

### Option 1: Video local với AI

```bash
start.bat
# Chọn [1] - Phan tich video local (co AI)
# Nhập đường dẫn file video
```

### Option 2: URL YouTube với AI

```bash
start.bat
# Chọn [2] - Phan tich tu URL YouTube (co AI)
# Nhập URL video
```

### Option 3: Command line

**Video local:**
```bash
python video_analyzer.py --input "path/to/video.mp4"
```

**YouTube URL:**
```bash
python video_analyzer.py --url "https://youtube.com/watch?v=xxxxx"
```

**Tùy chỉnh độ chi tiết:**
```bash
# Mô tả ngắn gọn (nhanh, tiết kiệm)
python video_analyzer.py --input video.mp4 --detail-level brief

# Mô tả chi tiết (chậm hơn, đầy đủ hơn)
python video_analyzer.py --input video.mp4 --detail-level detailed

# Mô tả rất chi tiết (chậm nhất, rất đầy đủ)
python video_analyzer.py --input video.mp4 --detail-level comprehensive
```

---

## 📊 Kết quả với AI vs Không AI

### KHÔNG AI (--no-ai)
```
✅ Nhanh (vài giây)
✅ Không tốn tiền API
❌ Không có mô tả cảnh
❌ Chỉ có thông tin kỹ thuật
```

**Báo cáo:**
```markdown
Cảnh 1: Chưa có mô tả
Cảnh 2: Chưa có mô tả
```

### CÓ AI (với ANTHROPIC_API_KEY)
```
✅ Mô tả chi tiết từng cảnh
✅ Phân tích nội dung
✅ Nhận diện đối tượng
❌ Chậm hơn (tùy số cảnh)
❌ Tốn phí API (~$0.003/ảnh)
```

**Báo cáo:**
```markdown
Cảnh 1: Video mở đầu với logo công ty trên nền trắng,
        có hiệu ứng fade in mượt mà. Góc quay chính diện,
        ánh sáng đều, không có chuyển động.

Cảnh 2: Chuyển sang cảnh người phát biểu đứng trong
        phòng họp, áo vest xanh navy, đang trình bày
        slide với biểu đồ tăng trưởng...
```

---

## 💰 Chi phí API

Anthropic tính phí theo:
- **Input tokens**: Text prompt
- **Output tokens**: Mô tả được tạo
- **Images**: Mỗi ảnh frame

**Ước tính:**
- Video 2 phút, 10 cảnh
- 3 frames/cảnh = 30 ảnh
- Brief mode: ~$0.10 - $0.20
- Detailed mode: ~$0.30 - $0.50

**Tips tiết kiệm:**
1. Dùng `--detail-level brief` cho video dài
2. Tăng `--threshold` để giảm số cảnh
3. Test với `--no-ai` trước

---

## 📄 Xuất file Word (.docx)

Báo cáo sẽ tự động tạo cả file **Word (.docx)** với:
- ✅ Bảng tóm tắt đẹp mắt
- ✅ Hình ảnh frames nhúng trong Word
- ✅ Format chuyên nghiệp
- ✅ Sẵn sàng in hoặc gửi email

**Vị trí file:**
```
output/reports/
  ├── video_name_report.docx    ← File Word
  ├── video_name_report.html
  ├── video_name_report.json
  └── video_name_report.md
```

---

## ❓ FAQ

**Q: Tôi không có tiền mua API key, có cách nào không?**

A: Anthropic có credit miễn phí khi đăng ký mới ($5). Bạn cũng có thể:
- Dùng chế độ `--no-ai` (miễn phí hoàn toàn)
- Chỉ phân tích những video quan trọng với AI
- Dùng `--detail-level brief` để tiết kiệm

**Q: Lỗi "ANTHROPIC_API_KEY not found"?**

A: Kiểm tra:
1. File `.env` có tồn tại trong thư mục `video_analyzer`?
2. Key có format đúng: `ANTHROPIC_API_KEY=sk-ant-...`?
3. Đã khởi động lại terminal sau khi set biến môi trường?

**Q: AI phân tích sai hoặc không chính xác?**

A:
- Thử `--detail-level comprehensive` cho độ chính xác cao hơn
- Kiểm tra chất lượng video (độ phân giải thấp → khó phân tích)
- Một số loại video phức tạp có thể khó nhận diện

**Q: Tôi muốn file Word nhưng không có mô tả AI?**

A: Được! Chạy `--no-ai` vẫn tạo file Word, chỉ là mô tả sẽ là "Chưa có mô tả".

---

## 🚀 Ví dụ đầy đủ

```bash
# 1. Update yt-dlp (nếu dùng YouTube)
pip install --upgrade yt-dlp

# 2. Cài python-docx (nếu cần Word)
pip install python-docx

# 3. Tạo file .env với API key
echo ANTHROPIC_API_KEY=sk-ant-xxxxx > .env

# 4. Chạy phân tích
python video_analyzer.py --url "https://youtube.com/watch?v=xxxxx" --detail-level brief

# 5. Mở file Word
start output/reports/video_name_report.docx
```

---

**Chúc bạn phân tích video thành công! 🎉**
