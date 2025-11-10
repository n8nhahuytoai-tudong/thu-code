# YouTube to Sora 2 Analyzer - Version 2.1

## 🚀 Tính năng mới

### Version 2.1 - Detailed Character & Animal Analysis
- ✅ **Không giới hạn số scenes** (từ 20 → 999)
- ✅ **Phân tích nhân vật cực chi tiết**: chiều cao, cân nặng, màu da, tóc, hình dáng, quần áo, tỷ lệ cơ thể
- ✅ **Phân tích con vật cực chi tiết**: loài, kích thước, màu sắc, đặc điểm, tỷ lệ
- ✅ **Prompts chuyên nghiệp hơn** cho Sora 2
- ✅ Export 3 định dạng: TXT, JSON, Markdown

---

## 📋 Yêu cầu

### 1. Cài đặt Python packages
```bash
pip install openai opencv-python numpy yt-dlp
```

### 2. Cài đặt yt-dlp
```bash
# macOS
brew install yt-dlp

# Windows
winget install yt-dlp

# Linux
sudo apt install yt-dlp
```

### 3. OpenAI API Key
Tạo file `.env` với nội dung:
```
OPENAI_API_KEY=sk-your-api-key-here
```

Hoặc nhập trực tiếp khi chạy.

---

## 🎯 Cách sử dụng

### Cách 1: Command line (đơn giản)
```bash
python youtube_to_sora_advanced_v2.py
```

Sau đó nhập:
- YouTube URL
- API key (nếu chưa có trong .env)
- Chọn options

### Cách 2: Trong code Python
```python
from youtube_to_sora_advanced_v2 import YouTubeToSoraAnalyzer

# Khởi tạo
analyzer = YouTubeToSoraAnalyzer(api_key="sk-your-key")

# Phân tích video
result = analyzer.analyze(
    youtube_url="https://www.youtube.com/watch?v=...",
    use_cache=True,
    analyze_audio=True
)

# Kết quả
print(result['sora_prompts'])
```

---

## 📊 Output

### File outputs (trong folder `output_results/`):

#### 1. **TXT File** - Full report
```
Video_Title_20250110_143022.txt
```
Bao gồm:
- Video metadata
- Overall analysis
- Scene-by-scene breakdown (chi tiết nhân vật/con vật)
- Transcript
- Sora 2 prompts (3 variants)

#### 2. **JSON File** - Structured data
```json
{
  "video_info": {...},
  "overall_analysis": "...",
  "scenes": [...],
  "transcript": {...},
  "sora_prompts": "...",
  "version": "2.1"
}
```

#### 3. **Markdown File** - Formatted report
```markdown
# YouTube to Sora 2 - Analysis Report
...
```

---

## 🎨 Sora Prompts

Mỗi video sẽ tạo ra **3 prompts**:

### 1. SHORT PROMPT (60-80 words)
Súc tích, hành động chính, có chi tiết quan trọng

### 2. DETAILED PROMPT (150-200 words)
- Mô tả chi tiết nhân vật: height, body type, skin tone, hair, clothing, proportions
- Mô tả chi tiết con vật: species, size, weight, colors, proportions
- Camera movements cụ thể
- Lighting setup
- Environment
- Actions

### 3. CINEMATIC PROMPT (120-160 words)
- Nghệ thuật, metaphor
- Film references
- Emotional tone
- Artistic techniques

**Tất cả prompts đều bằng TIẾNG ANH**

---

## 💡 Ví dụ chi tiết nhân vật

### Trước (Version 1.0):
```
"A man walking in the street"
```

### Sau (Version 2.1):
```
"A tall athletic man (approximately 185cm, 80kg) with olive skin tone,
short dark brown hair styled in a modern fade, wearing a fitted navy
blue button-down shirt and dark gray chinos. Body proportions: broad
shoulders, narrow waist, long legs. Walking with confident stride
through urban street..."
```

---

## 💡 Ví dụ chi tiết con vật

### Trước:
```
"A dog running"
```

### Sau:
```
"A medium-sized Golden Retriever (approximately 60cm tall at shoulder,
30kg), with long golden-blonde wavy coat, dark brown eyes, black nose.
Body proportions: well-balanced, medium-length legs, long bushy tail.
Running energetically across green grass..."
```

---

## ⚙️ Cấu hình

Trong file `youtube_to_sora_advanced_v2.py`, class `Config`:

```python
class Config:
    # Scene detection
    SCENE_THRESHOLD = 30.0       # Độ nhạy phát hiện scene
    MIN_SCENE_LENGTH = 15        # Độ dài tối thiểu (frames)
    FRAMES_PER_SCENE = 4         # Số frames phân tích/scene

    # Limits
    MAX_SCENES_TO_ANALYZE = 999  # Không giới hạn!

    # API
    VISION_MODEL = "gpt-4o"
    TEXT_MODEL = "gpt-4o"
    WHISPER_MODEL = "whisper-1"
```

---

## 💰 Chi phí API

**OpenAI GPT-4o Vision** khá đắt, ước tính:
- 1 scene (~4 frames): $0.05 - $0.10
- Video 50 scenes: $2.5 - $5.0
- Video 100 scenes: $5.0 - $10.0

**Lưu ý**: Version mới phân tích TẤT CẢ scenes nên chi phí cao hơn!

### Cách tiết kiệm:
1. Dùng cache (use_cache=True)
2. Giảm FRAMES_PER_SCENE từ 4 → 2-3
3. Tăng SCENE_THRESHOLD để có ít scenes hơn

---

## 🐛 Troubleshooting

### Lỗi: "OpenAI API key không tìm thấy"
**Giải pháp**: Tạo file `.env` hoặc nhập key trực tiếp

### Lỗi: "yt-dlp not found"
**Giải pháp**:
```bash
pip install yt-dlp
# hoặc
brew install yt-dlp
```

### Lỗi: "Rate limit exceeded"
**Giải pháp**: Đợi 1 phút hoặc nâng cấp OpenAI account

### Video quá dài (>100 scenes)
**Giải pháp**:
- Chấp nhận chi phí cao
- Hoặc cắt video thành nhiều phần ngắn hơn

---

## 📝 Changelog

### v2.1 (2025-01-10)
- ✅ Bỏ giới hạn MAX_SCENES (20 → 999)
- ✅ Thêm phân tích chi tiết nhân vật (height, weight, skin, hair, clothes, proportions)
- ✅ Thêm phân tích chi tiết con vật (species, size, weight, colors, proportions)
- ✅ Tăng max_tokens cho prompts (1500 → 2000-3000)
- ✅ Export thêm Markdown format
- ✅ Cải thiện prompts cho Sora 2

### v2.0 (Original)
- Scene detection
- Audio transcription
- Basic visual analysis
- 3 prompt variants
- Cache support

---

## 📞 Hỗ trợ

Nếu có vấn đề:
1. Kiểm tra API key hợp lệ
2. Kiểm tra yt-dlp đã cài đặt
3. Kiểm tra internet connection
4. Xem log errors trong terminal

---

## 🎉 Tips sử dụng

1. **Test với video ngắn trước** (<2 phút) để tiết kiệm chi phí
2. **Dùng cache** để không phải phân tích lại
3. **Kiểm tra output_results/** để xem kết quả
4. **Chỉnh SCENE_THRESHOLD** nếu phát hiện quá nhiều/ít scenes
5. **Video có nhân vật rõ mặt** sẽ cho kết quả tốt nhất

---

Made with ❤️ for Sora 2 creators
