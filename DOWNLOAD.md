# VIDEO ANALYZER TOOL - FINAL VERSION

## DOWNLOAD LINK

**Download ZIP trực tiếp từ GitHub:**

```
https://github.com/n8nhahuytoai-tudong/thu-code/archive/refs/heads/claude/task-one-011CV1DsaKRtFBF1DKtpEyEC.zip
```

**Hoặc clone bằng Git:**

```bash
git clone -b claude/task-one-011CV1DsaKRtFBF1DKtpEyEC https://github.com/n8nhahuytoai-tudong/thu-code.git
```

---

## HƯỚNG DẪN CÀI ĐẶT NHANH (3 BƯỚC)

### Bước 1: Giải nén file ZIP

Giải nén file ZIP vào thư mục bất kỳ, ví dụ: `F:\video_analyzer\`

### Bước 2: Cài đặt Python libraries

Mở CMD trong thư mục `video_analyzer` và chạy:

```bash
cd video_analyzer
pip install opencv-python scenedetect yt-dlp anthropic tqdm python-dotenv
```

Hoặc dùng file cài tự động:

```bash
install.bat
```

### Bước 3: Chạy tool

**Cách 1: Dùng menu (dễ nhất)**

```bash
start.bat
```

Chọn:
- `[1]` - Phân tích file video local + AI
- `[2]` - Phân tích URL YouTube + AI
- `[3]` - Phân tích file video local (KHÔNG AI - nhanh)
- `[4]` - Phân tích URL YouTube (KHÔNG AI - nhanh) ← KHUYẾN NGHỊ

**Cách 2: Command line**

```bash
# Với URL YouTube (không cần AI key)
python video_analyzer.py --url "https://youtube.com/watch?v=xxx" --no-ai

# Với file local
python video_analyzer.py --input "F:\video.mp4" --no-ai
```

---

## CÁC FILE TRONG TOOL

```
video_analyzer/
├── modules/
│   ├── __init__.py
│   ├── video_downloader.py     ← Download từ YouTube
│   ├── scene_detector.py       ← Phát hiện cảnh
│   ├── frame_extractor.py      ← Extract ảnh
│   ├── ai_analyzer.py          ← AI analysis (optional)
│   └── report_generator.py     ← Tạo báo cáo
├── output/
│   ├── frames/                 ← Ảnh các cảnh
│   └── reports/                ← Báo cáo HTML/JSON/MD
├── temp/                       ← Video tạm
├── video_analyzer.py           ← Main script
├── start.bat                   ← Menu Windows
├── run.bat                     ← Quick run
├── install.bat                 ← Cài đặt tự động
├── README.md                   ← Hướng dẫn đầy đủ
├── HUONGDAN.txt                ← Hướng dẫn tiếng Việt
├── QUICKFIX.md                 ← Sửa lỗi nhanh
├── .env.example                ← Template API key
└── .gitignore
```

---

## TÍNH NĂNG

✅ Tải video từ YouTube/URL tự động
✅ Phát hiện tất cả cảnh trong video
✅ Extract ảnh đầu/giữa/cuối mỗi cảnh
✅ Phân tích nội dung bằng AI (optional)
✅ Tạo báo cáo HTML đẹp với ảnh
✅ Hỗ trợ video dài, không bỏ sót cảnh
✅ 3-level fallback cho YouTube download
✅ Xử lý fragment loss và HLS issues

---

## VÍ DỤ NHANH

```bash
# Test với file local (không AI)
python video_analyzer.py --input "F:\my_video.mp4" --no-ai

# Test với YouTube (không AI)
python video_analyzer.py --url "https://youtube.com/watch?v=dQw4w9WgXcQ" --no-ai

# Điều chỉnh threshold (video dài, muốn ít cảnh hơn)
python video_analyzer.py --input video.mp4 --no-ai --threshold 35
```

---

## KẾT QUẢ

Sau khi chạy xong, bạn sẽ có:

**1. Frames ảnh:**
```
output/frames/[video_name]/
├── scene_001_first.jpg
├── scene_001_middle.jpg
├── scene_001_last.jpg
├── scene_002_first.jpg
└── ...
```

**2. Báo cáo:**
```
output/reports/
├── [video_name]_report.html   ← MỞ FILE NÀY xem kết quả
├── [video_name]_report.json
└── [video_name]_report.md
```

---

## LƯU Ý QUAN TRỌNG

### Với URL YouTube:

- **PHẢI CHỌN [4] hoặc dùng --url**, KHÔNG dùng [1] hoặc --input
- Update yt-dlp thường xuyên: `pip install --upgrade yt-dlp`
- Nếu download lỗi → Tải video thủ công rồi dùng --input

### Với AI Analysis:

- Cần ANTHROPIC_API_KEY trong file `.env`
- Get API key tại: https://console.anthropic.com/
- Hoặc dùng `--no-ai` để bỏ qua (vẫn có scene detection + frames)

### Threshold:

- **Thấp (20-25)** = Nhạy hơn, phát hiện nhiều cảnh
- **Mặc định (27)** = Cân bằng
- **Cao (30-35)** = Ít cảnh hơn, dùng cho video dài

---

## SỬA LỖI NHANH

### Lỗi: "No module named 'cv2'"

```bash
pip install opencv-python
```

### Lỗi: YouTube download failed - "nsig extraction failed"

**⚠️ LỖI PHỔ BIẾN NHẤT - BẮT BUỘC PHẢI UPDATE YT-DLP!**

**Cách 1: Dùng file update tự động (Windows)**
```bash
update_ytdlp.bat
```

**Cách 2: Update thủ công**
```bash
pip uninstall yt-dlp -y
pip install yt-dlp
```

**Hoặc:**
```bash
pip install --upgrade yt-dlp
```

**Sau khi update, thử lại:**
```bash
start.bat
# Chọn [4] - URL không AI
```

**Nếu vẫn lỗi:**
Tải video thủ công rồi:
```bash
python video_analyzer.py --input downloaded_video.mp4 --no-ai
```

### Lỗi: anthropic client error

```bash
pip install --upgrade anthropic
```

Hoặc chạy không AI:

```bash
python video_analyzer.py --input video.mp4 --no-ai
```

---

## HỖ TRỢ

Xem thêm:
- `README.md` - Hướng dẫn đầy đủ
- `HUONGDAN.txt` - Hướng dẫn tiếng Việt
- `QUICKFIX.md` - Troubleshooting

---

**Version: 1.0.4 Final**
**Updated: 2025-01-11**
**Latest fixes:**
- ✅ Added 5-level fallback: best → worst → 360p → any format → bestvideo+bestaudio
- ✅ Better error messages for nsig extraction failures
- ✅ Added update_ytdlp.bat for easy yt-dlp updates
- ✅ Enhanced QUICKFIX.md with nsig error solutions
- ✅ Fixed auto-fallback when format not available
- ✅ Fixed file finding after download (handles files without extensions)
- ✅ All known bugs fixed and tested
