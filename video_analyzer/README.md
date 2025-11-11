# 🎬 Video Analyzer

**Công cụ phân tích video tự động** - Phát hiện cảnh, mô tả nội dung chi tiết bằng AI, và tạo báo cáo đẹp mắt.

## ✨ Tính năng

- 🔍 **Phát hiện cảnh tự động**: Sử dụng PySceneDetect
- 📸 **Extract frames**: Lấy ảnh đầu, giữa, cuối mỗi cảnh
- 🤖 **Phân tích AI**: Claude Vision API mô tả chi tiết
- 📊 **Báo cáo đẹp mắt**: Export JSON, HTML, Markdown
- 🌐 **Hỗ trợ nhiều nguồn**: File local hoặc URL (YouTube, etc.)
- ⚙️ **Tùy chỉnh linh hoạt**: Điều chỉnh ngưỡng, mức độ chi tiết

## 🚀 Cài đặt

### Cách 1: Tự động (Windows)

```bash
# Double-click file start.bat
# Chọn option [5] để cài đặt dependencies
```

### Cách 2: Thủ công

```bash
cd video_analyzer
pip install -r ../requirements.txt
```

### Cách 3: Cài riêng lẻ

```bash
pip install opencv-python==4.10.0.84
pip install scenedetect[opencv]==0.6.4
pip install yt-dlp==2024.12.23
pip install anthropic==0.39.0
pip install tqdm==4.67.1
pip install python-dotenv==1.0.1
```

### Setup API Key (nếu dùng AI)

```bash
# Tạo file .env
copy .env.example .env

# Chỉnh sửa .env và thêm API key
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

Lấy API key tại: https://console.anthropic.com/

## 📖 Cách sử dụng

### Dùng Menu (Dễ nhất - Windows)

```bash
start.bat
```

Sau đó chọn:
- **[1]** - Video local + AI
- **[2]** - URL YouTube + AI
- **[3]** - Video local không AI (nhanh)
- **[4]** - URL không AI (nhanh)

### Dùng Command Line

**Phân tích video local:**
```bash
python video_analyzer.py --input my_video.mp4
```

**Phân tích từ URL YouTube:**
```bash
python video_analyzer.py --url "https://youtube.com/watch?v=xxx"
```

**Không dùng AI (nhanh, không cần API key):**
```bash
python video_analyzer.py --input video.mp4 --no-ai
```

**Điều chỉnh mức độ chi tiết:**
```bash
# Ngắn gọn
python video_analyzer.py --input video.mp4 --detail-level brief

# Chi tiết (mặc định)
python video_analyzer.py --input video.mp4 --detail-level detailed

# Rất chi tiết
python video_analyzer.py --input video.mp4 --detail-level very_detailed
```

**Thay đổi ngưỡng phát hiện cảnh:**
```bash
# Nhiều cảnh hơn (nhạy hơn)
python video_analyzer.py --input video.mp4 --threshold 20

# Ít cảnh hơn
python video_analyzer.py --input video.mp4 --threshold 35
```

## 📊 Output

Tool sẽ tạo:

### 1. Frames ảnh
```
output/frames/[video_name]/
├── scene_001_first.jpg
├── scene_001_middle.jpg
├── scene_001_last.jpg
├── scene_002_first.jpg
└── ...
```

### 2. Báo cáo JSON
```json
{
  "video_info": {...},
  "scenes": [
    {
      "scene_number": 1,
      "start_time": 0.0,
      "end_time": 5.2,
      "description": "Mô tả chi tiết...",
      "frames": {...}
    }
  ]
}
```

### 3. Báo cáo HTML
File HTML đẹp mắt với:
- Thống kê tổng quan
- Thông tin video
- Chi tiết từng cảnh + ảnh
- Responsive design

### 4. Báo cáo Markdown
Format text dễ đọc

## 🎯 Use Cases

**Phân tích video marketing:**
```bash
python video_analyzer.py --url "https://youtube.com/watch?v=xxx" --detail-level very_detailed
```

**Tạo storyboard:**
```bash
python video_analyzer.py --input movie.mp4 --threshold 30 --formats html
```

**Indexing video dài (không AI):**
```bash
python video_analyzer.py --input long_video.mp4 --no-ai --threshold 25
```

## 🔧 Troubleshooting

### Lỗi: "got an unexpected keyword argument 'proxies'"

```bash
pip uninstall anthropic -y
pip install anthropic==0.39.0
```

### Lỗi: "File không tồn tại" với URL

Phải dùng `--url` thay vì `--input` cho YouTube:

```bash
# ✅ Đúng
python video_analyzer.py --url "https://youtube.com/watch?v=xxx"

# ❌ Sai
python video_analyzer.py --input "https://youtube.com/watch?v=xxx"
```

### Lỗi: "ANTHROPIC_API_KEY not found"

**Giải pháp 1:** Tạo file .env
```bash
copy .env.example .env
# Thêm API key vào file .env
```

**Giải pháp 2:** Chạy không AI
```bash
python video_analyzer.py --input video.mp4 --no-ai
```

### Video dài quá nhiều cảnh

```bash
# Tăng threshold và min scene length
python video_analyzer.py --input video.mp4 --threshold 35 --min-scene-len 30
```

## 🔑 Tùy chọn đầy đủ

```
--input, -i          Đường dẫn file video local
--url, -u            URL video (YouTube, Vimeo, etc.)
--threshold, -t      Ngưỡng phát hiện cảnh (mặc định: 27.0)
--min-scene-len      Độ dài tối thiểu cảnh (frames, mặc định: 15)
--no-ai              Không dùng AI phân tích
--detail-level       brief | detailed | very_detailed
--language, -l       vi | en
--formats, -f        json html markdown
```

## 📄 Files

```
video_analyzer/
├── modules/
│   ├── __init__.py
│   ├── video_downloader.py    # Download/validate video
│   ├── scene_detector.py      # Phát hiện cảnh
│   ├── frame_extractor.py     # Extract frames
│   ├── ai_analyzer.py         # Phân tích AI
│   └── report_generator.py    # Tạo báo cáo
├── output/
│   ├── frames/                # Frames đã extract
│   └── reports/               # Báo cáo
├── temp/                      # Video tạm (từ URL)
├── video_analyzer.py          # Main script
├── start.bat                  # Menu Windows
├── .env.example               # Template API key
├── .gitignore
└── README.md
```

## ⚡ Quick Start

```bash
# 1. Cài đặt
pip install -r requirements.txt

# 2. Setup API key (tùy chọn)
copy .env.example .env
# Chỉnh sửa .env

# 3. Chạy
python video_analyzer.py --url "https://youtube.com/watch?v=xxx" --no-ai
```

## 💡 Tips

- Dùng `--no-ai` để phân tích nhanh không cần API key
- Threshold thấp (20-25) = nhiều cảnh hơn
- Threshold cao (30-35) = ít cảnh hơn
- `detail-level brief` nhanh hơn nhưng ít chi tiết
- Video dài nên dùng `--no-ai` để tiết kiệm thời gian

---

**Made with ❤️ using Claude AI**
