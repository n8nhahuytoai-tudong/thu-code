# 🔧 Sửa lỗi nhanh - Video Analyzer

## ⚠️ Lỗi thường gặp

### 1. Lỗi: "got an unexpected keyword argument 'proxies'"

**Nguyên nhân:** Version anthropic library không khớp

**Giải pháp:**
```bash
pip uninstall anthropic -y
pip install anthropic==0.39.0
```

---

### 2. Lỗi: "File không tồn tại" khi dùng URL YouTube

**Nguyên nhân:** Dùng sai parameter

❌ **SAI:**
```bash
python video_analyzer.py --input https://youtube.com/watch?v=xxx
```

✅ **ĐÚNG:**
```bash
python video_analyzer.py --url https://youtube.com/watch?v=xxx
```

**Hoặc dùng menu:**
```bash
start.bat
# Chọn [2] hoặc [4]
```

---

### 3. Lỗi: "No module named 'cv2'" hoặc "scenedetect"

**Giải pháp:**
```bash
cd ..
pip install -r requirements.txt
cd video_analyzer
```

Hoặc cài riêng:
```bash
pip install opencv-python scenedetect[opencv] yt-dlp anthropic tqdm python-dotenv
```

---

### 4. Lỗi: "ANTHROPIC_API_KEY not found"

**Cách 1: Tạo file .env**
```bash
copy .env.example .env
notepad .env
```

Thêm vào:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

**Cách 2: Chạy không AI**
```bash
python video_analyzer.py --input video.mp4 --no-ai
```

---

### 5. Download YouTube thất bại - "nsig extraction failed" / "Requested format is not available"

**⚠️ Đây là lỗi phổ biến nhất với YouTube!**

**Nguyên nhân:**
- yt-dlp version cũ
- YouTube thay đổi signature algorithm
- Video có giới hạn khu vực hoặc yêu cầu đăng nhập

**Giải pháp 1: UPDATE yt-dlp (BẮT BUỘC)**
```bash
pip install --upgrade yt-dlp
```

**Nếu vẫn lỗi, GỠ VÀ CÀI LẠI:**
```bash
pip uninstall yt-dlp -y
pip install yt-dlp
```

**Giải pháp 2: Thử video khác**
```bash
# Test với video public đơn giản
python video_analyzer.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --no-ai
```

**Giải pháp 3: Download thủ công**
```bash
# Download bằng web browser hoặc tool khác
# Sau đó dùng --input
python video_analyzer.py --input downloaded_video.mp4 --no-ai
```

**Giải pháp 4: Kiểm tra video có bị giới hạn không**
- Thử mở video trên browser
- Nếu yêu cầu đăng nhập → download thủ công
- Nếu bị chặn khu vực → dùng VPN hoặc video khác

---

### 6. Video dài, phát hiện quá nhiều cảnh

**Giải pháp: Tăng threshold**
```bash
python video_analyzer.py --input video.mp4 --threshold 35 --min-scene-len 30
```

---

### 7. AI phân tích quá chậm

**Giải pháp 1: Dùng brief**
```bash
python video_analyzer.py --input video.mp4 --detail-level brief
```

**Giải pháp 2: Không dùng AI**
```bash
python video_analyzer.py --input video.mp4 --no-ai
```

---

## ✅ Kiểm tra cài đặt

```bash
python --version          # >= 3.8
pip list | findstr opencv
pip list | findstr anthropic
pip list | findstr yt-dlp
```

---

## 🚀 Test nhanh

```bash
# Test không AI
python video_analyzer.py --help

# Test với video ngắn
python video_analyzer.py --input test.mp4 --no-ai --threshold 30
```

---

## 📞 Vẫn lỗi?

1. Kiểm tra Python version >= 3.8
2. Gỡ và cài lại dependencies
3. Xem lại đường dẫn file/URL
4. Chạy ở chế độ `--no-ai` để test
