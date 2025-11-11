# 🎬 Video Analyzer

**Công cụ phân tích video tự động** - Phát hiện cảnh, mô tả nội dung chi tiết bằng AI, và tạo báo cáo đẹp mắt.

## ✨ Tính năng

- 🔍 **Phát hiện cảnh tự động**: Sử dụng thuật toán Content Detection để tìm các thay đổi cảnh
- 📸 **Extract frames**: Lấy ảnh đầu, giữa, cuối mỗi cảnh
- 🤖 **Phân tích AI**: Sử dụng Claude Vision API để mô tả chi tiết nội dung từng cảnh
- 📊 **Báo cáo đẹp mắt**: Export sang JSON, HTML, Markdown
- 🌐 **Hỗ trợ nhiều nguồn**: File local hoặc URL (YouTube, Vimeo, etc.)
- ⚙️ **Tùy chỉnh linh hoạt**: Điều chỉnh ngưỡng, mức độ chi tiết, ngôn ngữ

## 🚀 Cài đặt

### 1. Clone repository hoặc copy thư mục `video_analyzer`

```bash
cd video_analyzer
```

### 2. Cài đặt dependencies

```bash
pip install -r ../requirements.txt
```

Các thư viện chính:
- `opencv-python`: Xử lý video
- `scenedetect`: Phát hiện cảnh
- `yt-dlp`: Download video từ URL
- `anthropic`: Claude AI API
- `tqdm`: Progress bar

### 3. Setup API Key (nếu dùng AI)

Tạo file `.env` trong thư mục `video_analyzer/`:

```bash
cp .env.example .env
```

Chỉnh sửa `.env` và thêm API key của bạn:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

> 💡 Lấy API key tại: https://console.anthropic.com/

## 📖 Cách sử dụng

### Cơ bản

**Phân tích video local:**
```bash
python video_analyzer.py --input my_video.mp4
```

**Phân tích video từ URL:**
```bash
python video_analyzer.py --url https://youtube.com/watch?v=xxx
```

### Tùy chọn nâng cao

**Chạy không có AI (chỉ phát hiện cảnh và extract frames):**
```bash
python video_analyzer.py --input video.mp4 --no-ai
```

**Thay đổi mức độ chi tiết:**
```bash
# Mô tả ngắn gọn
python video_analyzer.py --input video.mp4 --detail-level brief

# Mô tả chi tiết (mặc định)
python video_analyzer.py --input video.mp4 --detail-level detailed

# Mô tả cực kỳ chi tiết
python video_analyzer.py --input video.mp4 --detail-level very_detailed
```

**Thay đổi ngưỡng phát hiện cảnh:**
```bash
# Ngưỡng thấp hơn = nhạy hơn, nhiều cảnh hơn
python video_analyzer.py --input video.mp4 --threshold 20

# Ngưỡng cao hơn = ít cảnh hơn
python video_analyzer.py --input video.mp4 --threshold 35
```

**Chọn ngôn ngữ mô tả:**
```bash
# Tiếng Việt (mặc định)
python video_analyzer.py --input video.mp4 --language vi

# Tiếng Anh
python video_analyzer.py --input video.mp4 --language en
```

**Chọn format báo cáo:**
```bash
# Chỉ JSON
python video_analyzer.py --input video.mp4 --formats json

# JSON và HTML
python video_analyzer.py --input video.mp4 --formats json html

# Tất cả (mặc định)
python video_analyzer.py --input video.mp4 --formats json html markdown
```

### Tất cả tùy chọn

```
Options:
  --input, -i           Đường dẫn file video local
  --url, -u             URL video (YouTube, Vimeo, etc.)
  --threshold, -t       Ngưỡng phát hiện cảnh (mặc định: 27.0)
  --min-scene-len       Độ dài tối thiểu cảnh (frames, mặc định: 15)
  --no-ai               Không dùng AI phân tích
  --detail-level        Mức độ chi tiết: brief, detailed, very_detailed
  --language, -l        Ngôn ngữ: vi, en
  --formats, -f         Format báo cáo: json, html, markdown
```

## 📁 Cấu trúc thư mục

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
│   │   └── [video_name]/
│   │       ├── scene_001_first.jpg
│   │       ├── scene_001_middle.jpg
│   │       ├── scene_001_last.jpg
│   │       └── ...
│   └── reports/               # Báo cáo
│       ├── [video_name]_report.json
│       ├── [video_name]_report.html
│       └── [video_name]_report.md
├── temp/                      # Video tạm (từ URL)
├── video_analyzer.py          # Main script
├── .env                       # API keys (git ignored)
├── .env.example               # Template
├── .gitignore
└── README.md
```

## 📊 Output

Tool sẽ tạo ra:

### 1. Frames ảnh
Mỗi cảnh có 3 frames:
- `scene_XXX_first.jpg` - Frame đầu
- `scene_XXX_middle.jpg` - Frame giữa
- `scene_XXX_last.jpg` - Frame cuối

### 2. Báo cáo JSON
Chứa toàn bộ dữ liệu phân tích:
```json
{
  "video_info": { ... },
  "scenes": [
    {
      "scene_number": 1,
      "start_time": 0.0,
      "end_time": 5.2,
      "duration": 5.2,
      "description": "Mô tả chi tiết...",
      "frames": { ... }
    }
  ],
  "summary": { ... }
}
```

### 3. Báo cáo HTML
File HTML đẹp mắt với:
- Thống kê tổng quan
- Thông tin video
- Chi tiết từng cảnh kèm ảnh
- Responsive design

### 4. Báo cáo Markdown
Format text dễ đọc, có thể xem trên GitHub

## 🎯 Use Cases

### 1. Phân tích video marketing
```bash
python video_analyzer.py --url https://youtube.com/watch?v=xxx \
  --detail-level very_detailed \
  --language vi
```

### 2. Tạo storyboard từ video
```bash
python video_analyzer.py --input movie.mp4 \
  --threshold 30 \
  --formats html
```

### 3. Indexing video dài (không cần AI)
```bash
python video_analyzer.py --input long_video.mp4 \
  --no-ai \
  --threshold 25
```

### 4. Phân tích chi tiết cho AI training
```bash
python video_analyzer.py --input training_video.mp4 \
  --detail-level very_detailed \
  --formats json
```

## ⚙️ Cách hoạt động

1. **Video Input**: Nhận video từ file hoặc URL
2. **Scene Detection**: Phát hiện thay đổi cảnh dựa trên content
3. **Frame Extraction**: Extract 3 frames từ mỗi cảnh
4. **AI Analysis** (nếu bật): Gửi frames đến Claude Vision để phân tích
5. **Report Generation**: Tạo báo cáo dưới nhiều format

## 🔧 Troubleshooting

### Lỗi: "Không thể mở video"
- Kiểm tra đường dẫn file
- Đảm bảo video format được hỗ trợ (mp4, avi, mov, mkv, etc.)
- Cài đặt đầy đủ opencv: `pip install opencv-python`

### Lỗi: "ANTHROPIC_API_KEY not found"
- Tạo file `.env` từ `.env.example`
- Thêm API key hợp lệ
- Hoặc chạy với `--no-ai`

### Video dài bị quá nhiều cảnh
- Tăng `--threshold` (ví dụ: 35-40)
- Tăng `--min-scene-len` (ví dụ: 30-45 frames)

### AI phân tích quá lâu
- Dùng `--detail-level brief`
- Hoặc `--no-ai` nếu không cần mô tả

### Download video từ URL thất bại
- Kiểm tra URL có hợp lệ
- Một số site cần cookies/auth (chưa hỗ trợ)
- Thử download thủ công rồi dùng `--input`

## 🚀 Tối ưu hóa

### Video dài (>30 phút)
```bash
python video_analyzer.py --input long_video.mp4 \
  --threshold 30 \
  --min-scene-len 30 \
  --detail-level brief
```

### Video ngắn chất lượng cao
```bash
python video_analyzer.py --input short_video.mp4 \
  --threshold 20 \
  --detail-level very_detailed
```

### Batch processing nhiều video
Tạo script bash:
```bash
#!/bin/bash
for video in *.mp4; do
  python video_analyzer.py --input "$video" --detail-level detailed
done
```

## 📝 License

MIT License - Tự do sử dụng và chỉnh sửa

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Issues và Pull Requests tại repository chính.

## 📧 Liên hệ

Nếu có vấn đề hoặc câu hỏi, vui lòng tạo issue.

---

**Made with ❤️ using Claude AI**
