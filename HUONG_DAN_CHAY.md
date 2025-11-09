# 🚀 HƯỚNG DẪN CHẠY YOUTUBE TO SORA 2 ADVANCED

## Bước 1: Cài đặt Python Dependencies

```bash
pip install openai opencv-python numpy yt-dlp python-docx
```

**Hoặc nếu dùng pip3:**
```bash
pip3 install openai opencv-python numpy yt-dlp python-docx
```

## Bước 2: Cài đặt FFmpeg (cần thiết cho audio)

### macOS:
```bash
brew install ffmpeg
```

### Ubuntu/Debian Linux:
```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows:
- Tải từ: https://ffmpeg.org/download.html
- Giải nén và thêm vào PATH

## Bước 3: Chuẩn bị OpenAI API Key

### Lấy API Key:
1. Đăng nhập: https://platform.openai.com/
2. Vào: API Keys → Create new secret key
3. Copy key (chỉ hiển thị 1 lần!)

### Set API Key (chọn 1 trong 3 cách):

**Cách 1: Environment Variable (khuyến nghị)**
```bash
# macOS/Linux
export OPENAI_API_KEY="sk-your-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=sk-your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

**Cách 2: Tạo file .env**
```bash
# Tạo file .env trong cùng folder
echo 'OPENAI_API_KEY=sk-your-api-key-here' > .env
```

**Cách 3: Nhập trực tiếp khi chạy**
- Script sẽ hỏi nếu không tìm thấy API key

## Bước 4: CHẠY SCRIPT

### Cách đơn giản nhất - Interactive Mode:

```bash
python3 youtube_to_sora_advanced.py
```

Sau đó nhập:
1. YouTube URL (ví dụ: https://youtube.com/watch?v=dQw4w9WgXcQ)
2. API Key (nếu chưa set environment variable)
3. Tùy chọn:
   - Sử dụng cache? (y/n) → y (tiết kiệm tiền)
   - Phân tích audio? (y/n) → y (để có transcript)

### Ví dụ chạy đầy đủ:

```bash
# Set API key
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxx"

# Chạy script
python3 youtube_to_sora_advanced.py
```

**Output sẽ như:**
```
======================================================================
YOUTUBE TO SORA 2 - ADVANCED PROMPT GENERATOR
======================================================================

Nhập YouTube URL: https://youtube.com/watch?v=example
Sử dụng cache? (y/n, mặc định: y): y
Phân tích audio/transcript? (y/n, mặc định: y): y

• Đang lấy thông tin video...
Video: Amazing Cat Video

• Đang tải video và audio...
✓ Video và audio đã tải xong
• Đang phát hiện scenes...
✓ Đã phát hiện 8 scenes
...
```

## Bước 5: Xem kết quả

Kết quả sẽ được lưu trong folder: `output_results/`

**3 files sẽ được tạo:**
```
output_results/
├── Video_Name_20250109_143052.txt      # Text report chi tiết
├── Video_Name_20250109_143052.json     # JSON data (for developers)
└── Video_Name_20250109_143052.docx     # Word document đẹp
```

## 📊 Ví dụ Output

### File TXT sẽ có:
```
======================================================================
YOUTUBE TO SORA 2 - ADVANCED ANALYSIS REPORT
======================================================================

VIDEO INFORMATION
Tên video: Amazing Cat Video
URL: https://youtube.com/watch?v=...
Thời lượng: 120s

======================================================================
PHÂN TÍCH TỔNG THỂ
======================================================================
Video mô tả một chú mèo đang chơi đùa trong vườn...

======================================================================
PHÂN TÍCH CHI TIẾT TỪNG SCENE (8 scenes)
======================================================================

SCENE 1 | 0.0s - 15.2s | Thời lượng: 15.2s
Mèo đang ngồi trên bức tường, nhìn xuống sân...
Camera: Static shot, wide angle...
Lighting: Natural daylight, warm tones...

======================================================================
SORA 2 PROMPTS (3 VARIANTS)
======================================================================

=== SHORT PROMPT ===
A playful orange cat jumping through a sunny garden, dynamic camera
tracking, vibrant colors, joyful atmosphere.

=== DETAILED PROMPT ===
A vibrant orange tabby cat playfully explores a lush green garden
filled with colorful flowers. The camera dynamically tracks the cat's
movements as it leaps and pounces. Golden hour lighting bathes the
scene in warm, inviting tones. Shallow depth of field creates a
dreamy, cinematic quality...

=== CREATIVE PROMPT ===
In a sun-drenched paradise of green, an adventurous feline spirit
dances with nature itself. The camera becomes poetry, flowing
gracefully through moments of pure joy...
```

## 🎯 Sử dụng nâng cao (Python code)

Nếu bạn muốn tích hợp vào code của mình:

```python
from youtube_to_sora_advanced import AdvancedYouTubeToSoraPrompt

# Khởi tạo
processor = AdvancedYouTubeToSoraPrompt(api_key="sk-your-key")

# Phân tích video
result = processor.process(
    youtube_url="https://youtube.com/watch?v=example",
    use_cache=True,         # Dùng cache để tiết kiệm
    analyze_audio=True      # Phân tích audio/transcript
)

# Lấy kết quả
print("Phân tích tổng thể:")
print(result['overall_analysis'])

print("\nSora Prompts:")
print(result['sora_prompts'])

print(f"\nSố scenes: {len(result['scene_analyses'])}")
```

## 🔧 Tùy chỉnh nâng cao

### Điều chỉnh Scene Detection:

```python
# Nhiều scenes hơn (nhạy hơn với thay đổi)
processor.detect_scenes(threshold=20.0, min_scene_length=10)

# Ít scenes hơn (chỉ detect thay đổi lớn)
processor.detect_scenes(threshold=40.0, min_scene_length=30)
```

### Điều chỉnh số frames phân tích:

```python
# Nhanh hơn, ít chi tiết
processor.extract_key_frames_from_scenes(frames_per_scene=2)

# Chậm hơn, rất chi tiết
processor.extract_key_frames_from_scenes(frames_per_scene=5)
```

## 💰 Chi phí dự tính

Với video 5 phút, 8 scenes:

| Component | API | Chi phí |
|-----------|-----|---------|
| Scene analysis (8 scenes x 3 frames) | GPT-4o Vision | ~$0.80 |
| Audio transcript (5 min) | Whisper | ~$0.03 |
| Overall analysis + prompts | GPT-4o | ~$0.15 |
| **TỔNG** | | **~$0.98** |

**Tiết kiệm với Cache:**
- Lần đầu: ~$0.98
- Lần sau (từ cache): $0.00 ✅

## ❌ Xử lý lỗi thường gặp

### Lỗi 1: "yt-dlp not found"
```bash
pip install yt-dlp
# hoặc
pip3 install yt-dlp
```

### Lỗi 2: "ffmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### Lỗi 3: "OpenAI API key not found"
```bash
export OPENAI_API_KEY="sk-your-key"
```

### Lỗi 4: "OpenAI API rate limit"
- Đợi 1 phút rồi chạy lại
- Hoặc nâng cấp account OpenAI

### Lỗi 5: "Video too long / Out of memory"
```python
# Giảm số frames
processor.extract_key_frames_from_scenes(frames_per_scene=2)

# Tăng threshold để có ít scenes hơn
processor.detect_scenes(threshold=40.0)
```

## 📞 Cần giúp đỡ?

Nếu gặp vấn đề:
1. Check log output - script sẽ hiển thị lỗi chi tiết
2. Đảm bảo có internet connection
3. Kiểm tra API key còn credit
4. Thử với video ngắn hơn (<2 phút) để test

## ✅ Checklist trước khi chạy

- [ ] Đã cài Python 3.8+
- [ ] Đã cài packages: `pip install openai opencv-python numpy yt-dlp python-docx`
- [ ] Đã cài ffmpeg
- [ ] Có OpenAI API Key và đã set environment variable
- [ ] Có internet connection
- [ ] Có URL YouTube hợp lệ

**Chúc bạn phân tích video thành công! 🎬✨**
