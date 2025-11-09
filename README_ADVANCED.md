# YouTube to Sora 2 - Advanced Prompt Generator 🎬

Phân tích video YouTube chi tiết và tạo prompts chuyên nghiệp cho Sora 2 AI video generation.

## ✨ Tính năng nâng cao

### So sánh phiên bản Basic vs Advanced

| Tính năng | Basic | Advanced |
|-----------|-------|----------|
| Số frames phân tích | 5 (cố định) | Nhiều (tự động theo scenes) |
| Scene detection | ❌ | ✅ Tự động phát hiện scenes |
| Audio/Transcript | ❌ | ✅ Whisper API |
| Phân tích từng scene | ❌ | ✅ Chi tiết từng scene |
| Visual composition | ❌ | ✅ Màu sắc, lighting, contrast |
| Camera analysis | ❌ | ✅ Movement, composition |
| Multiple prompts | ❌ | ✅ 3 variants (short/detailed/creative) |
| Caching | ❌ | ✅ Tái sử dụng kết quả |
| Progress tracking | ❌ | ✅ Hiển thị tiến trình |
| Export formats | TXT, DOCX | TXT, DOCX, JSON |

### Các tính năng chi tiết

#### 1. **Scene Detection thông minh**
- Tự động phát hiện các scenes khác nhau trong video
- Sử dụng computer vision để detect scene changes
- Trích xuất key frames từ mỗi scene

#### 2. **Audio & Transcript Analysis**
- Sử dụng OpenAI Whisper để chuyển đổi speech-to-text
- Hỗ trợ nhiều ngôn ngữ (auto-detect)
- Phân tích nội dung lời thoại

#### 3. **Visual Composition Analysis**
- Phân tích màu sắc dominant
- Đo brightness và contrast
- Classify color mood (dark/bright/warm/cool)

#### 4. **Camera Movement Detection**
- Phát hiện camera movements (pan, zoom, tracking)
- Phân tích composition techniques
- Rule of thirds, symmetry, depth

#### 5. **Multiple Prompt Variants**
- **Short Prompt** (50-70 words): Ngắn gọn, hành động chính
- **Detailed Prompt** (120-150 words): Chi tiết đầy đủ
- **Creative Prompt** (100-130 words): Nghệ thuật, cinematic

#### 6. **Caching System**
- Lưu kết quả phân tích
- Tái sử dụng cho cùng một video
- Tiết kiệm API costs

#### 7. **Comprehensive Reports**
- Scene-by-scene breakdown
- Visual composition metrics
- Transcript integration
- Multiple export formats

## 📦 Cài đặt

### 1. Cài đặt Python dependencies

```bash
pip install -r requirements_advanced.txt
```

### 2. Cài đặt system dependencies

#### macOS:
```bash
brew install ffmpeg yt-dlp
```

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
pip install yt-dlp
```

#### Windows:
```bash
# Cài ffmpeg từ https://ffmpeg.org/download.html
pip install yt-dlp
```

### 3. Cài đặt optional dependencies

```bash
# Để export file DOCX
pip install python-docx
```

## 🚀 Sử dụng

### Cách 1: Interactive Mode (Đơn giản nhất)

```bash
python youtube_to_sora_advanced.py
```

Sau đó nhập:
- YouTube URL
- OpenAI API Key (nếu chưa set environment variable)
- Các tùy chọn (cache, audio analysis)

### Cách 2: Set Environment Variable

```bash
# Set API key
export OPENAI_API_KEY="your-api-key-here"

# Chạy script
python youtube_to_sora_advanced.py
```

### Cách 3: Sử dụng như Python module

```python
from youtube_to_sora_advanced import AdvancedYouTubeToSoraPrompt

# Khởi tạo
processor = AdvancedYouTubeToSoraPrompt(api_key="your-api-key")

# Xử lý video
result = processor.process(
    youtube_url="https://youtube.com/watch?v=...",
    use_cache=True,
    analyze_audio=True
)

# Kết quả
print(result['overall_analysis'])
print(result['sora_prompts'])
```

### Cách 4: Tùy chỉnh nâng cao

```python
processor = AdvancedYouTubeToSoraPrompt(
    api_key="your-api-key",
    cache_dir="my_cache"  # Thư mục cache tùy chỉnh
)

# Tùy chỉnh scene detection
processor.detect_scenes(
    threshold=30.0,  # Độ nhạy detect scenes (càng thấp càng nhiều scenes)
    min_scene_length=15  # Độ dài tối thiểu của scene (frames)
)

# Tùy chỉnh số frames mỗi scene
processor.extract_key_frames_from_scenes(
    frames_per_scene=5  # Số frames trích xuất từ mỗi scene
)
```

## 📊 Kết quả Output

### 1. File TXT (text report)
```
output_results/Video_Name_20250109_143052.txt
```
- Phân tích tổng thể
- Chi tiết từng scene
- Transcript
- 3 variants của Sora prompts

### 2. File DOCX (formatted document)
```
output_results/Video_Name_20250109_143052.docx
```
- Format đẹp, dễ đọc
- Tables, headings
- Sẵn sàng để share

### 3. File JSON (programmatic access)
```
output_results/Video_Name_20250109_143052.json
```
- Structured data
- Dễ parse và xử lý
- Tích hợp vào apps

## 🎯 Ví dụ Output

### Overall Analysis:
```
TÓNG TẮT CỐT TRUYỆN:
Video mô tả một chuyến phiêu lưu của một chú chó qua rừng...

PHONG CÁCH HÌNH ẢNH:
Màu sắc ấm, ánh sáng tự nhiên, cinematography chuyên nghiệp...

KỸ THUẬT QUAY:
Sử dụng nhiều camera movements, từ static shots đến tracking shots...
```

### Sora 2 Prompts:
```
=== SHORT PROMPT ===
A golden retriever running through autumn forest, dynamic tracking shot,
warm sunlight filtering through trees, cinematic composition.

=== DETAILED PROMPT ===
A joyful golden retriever bounds energetically through a vibrant autumn
forest, leaves crunching beneath its paws. Camera tracks smoothly alongside,
capturing the dog's expressive face and flowing movement. Warm golden hour
sunlight filters through orange and red foliage, creating a magical
atmosphere. Shallow depth of field, professional cinematography,
heartwarming mood.

=== CREATIVE PROMPT ===
Through a kaleidoscope of autumn colors, a golden retriever dances with
pure joy, embodying the spirit of freedom. The camera becomes a companion,
flowing gracefully through the enchanted forest. Sunbeams paint golden
streaks across the scene, transforming reality into a dreamlike adventure.
Cinematic poetry in motion.
```

## ⚙️ Tùy chỉnh

### Scene Detection Threshold

Điều chỉnh độ nhạy phát hiện scenes:

```python
# Nhiều scenes hơn (nhạy hơn)
processor.detect_scenes(threshold=20.0)

# Ít scenes hơn (ít nhạy hơn)
processor.detect_scenes(threshold=40.0)
```

### Frames per Scene

Số frames phân tích mỗi scene:

```python
# Phân tích ít hơn, nhanh hơn
processor.extract_key_frames_from_scenes(frames_per_scene=2)

# Phân tích nhiều hơn, chi tiết hơn
processor.extract_key_frames_from_scenes(frames_per_scene=5)
```

### Disable Audio Analysis

Nếu không cần transcript (tiết kiệm API cost):

```python
result = processor.process(
    youtube_url="...",
    analyze_audio=False  # Skip audio analysis
)
```

### Disable Caching

Không dùng cache (luôn phân tích mới):

```python
result = processor.process(
    youtube_url="...",
    use_cache=False
)
```

## 💰 Chi phí API

### OpenAI API Costs (ước tính)

| Component | Model | Cost per video (5 min) |
|-----------|-------|------------------------|
| Vision API | gpt-4o | ~$0.50-1.00 |
| Whisper API | whisper-1 | ~$0.03 |
| Text generation | gpt-4o | ~$0.10-0.20 |
| **Total** | | **~$0.63-1.23** |

**Tiết kiệm với Cache:**
- Lần đầu: $0.63-1.23
- Lần sau (từ cache): $0.00

## 🔧 Troubleshooting

### Lỗi: "yt-dlp not found"
```bash
pip install yt-dlp
```

### Lỗi: "ffmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### Lỗi: "OpenAI API key not found"
```bash
export OPENAI_API_KEY="your-key"
```

### Video quá dài (>10 phút)
- Sử dụng fewer frames per scene
- Tăng scene detection threshold
- Consider analyzing only portion of video

### Out of memory
- Giảm số frames per scene
- Process shorter videos
- Close other applications

## 📝 Changelog

### v2.0 (Advanced) - 2025-01-09
- ✅ Scene detection tự động
- ✅ Audio/transcript analysis
- ✅ Visual composition analysis
- ✅ Camera movement detection
- ✅ Multiple prompt variants
- ✅ Caching system
- ✅ Progress tracking
- ✅ JSON export

### v1.0 (Basic)
- ✅ Basic frame extraction
- ✅ Simple video analysis
- ✅ Single prompt generation

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] GPU acceleration for scene detection
- [ ] Support for local video files
- [ ] Batch processing multiple videos
- [ ] Web UI interface
- [ ] More export formats (PDF, Markdown)
- [ ] Custom prompt templates

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- OpenAI API (GPT-4o, Whisper)
- yt-dlp for video downloading
- OpenCV for video processing

---

**Made with ❤️ for Sora 2 creators**
