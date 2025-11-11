# YouTube to Sora 2 - Scene-by-Scene Analyzer

Phân tích video YouTube và tạo prompt Sora 2 chi tiết cho từng cảnh.

## ✨ Features

- 🎬 Tự động phát hiện cảnh (scene detection)
- 📸 Xuất ảnh đầu + ảnh cuối cho mỗi cảnh
- 🎨 Tạo prompt cinema chi tiết (150-200 words) cho MỖI cảnh
- 📁 Export có tổ chức theo folders
- 🎯 Tiêu chuẩn Hollywood: camera, lighting, color grading, etc.

## 📋 Yêu cầu hệ thống

- Python 3.8+
- OpenAI API key (GPT-4o Vision)
- Internet connection

## 🚀 Cài đặt

### Bước 1: Clone/Download repository

```bash
cd thu-code
```

### Bước 2: Cài đặt Python packages

```bash
pip install -r requirements.txt
```

**Hoặc cài thủ công:**

```bash
pip install opencv-python numpy openai yt-dlp
```

### Bước 3: Tạo file .env với API key

```bash
# Copy template
cp .env.example .env

# Hoặc tạo mới
echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
```

**Lấy OpenAI API key:**
1. Vào https://platform.openai.com/api-keys
2. Tạo key mới
3. Copy và paste vào file `.env`

### Bước 4: Kiểm tra cài đặt

```bash
# Test Python
python --version

# Test packages
python -c "import cv2, numpy, openai; print('✓ All packages installed')"

# Test yt-dlp
yt-dlp --version
```

## 💻 Cách sử dụng

### Cách 1: Interactive mode

```bash
python youtube_scene_by_scene_analyzer.py
```

Sau đó nhập:
- YouTube URL
- OpenAI API key (nếu chưa có trong .env)

### Cách 2: Script mode (sửa code)

```python
from youtube_scene_by_scene_analyzer import SceneBySceneAnalyzer

analyzer = SceneBySceneAnalyzer(api_key="sk-your-key")
result = analyzer.analyze("https://youtube.com/watch?v=...")
```

## 📁 Output structure

```
output_scenes/
  VideoTitle_20250111_123456/
    ├── scene_0000/
    │   ├── FIRST_frame.jpg      # Ảnh đầu cảnh
    │   ├── LAST_frame.jpg       # Ảnh cuối cảnh
    │   └── sora_prompt.txt      # Prompt 150-200 words
    │
    ├── scene_0001/
    │   ├── FIRST_frame.jpg
    │   ├── LAST_frame.jpg
    │   └── sora_prompt.txt
    │
    ├── 00_SUMMARY.txt           # Tổng quan
    └── scenes_data.json         # Dữ liệu JSON
```

## 📝 Ví dụ Prompt Output

```
Wide establishing shot tracking left to right across rain-soaked
urban street at night, 35mm lens f/2.8 creating shallow depth of
field, eye-level camera height 170cm, smooth gimbal movement. Male
protagonist ~185cm tall, athletic build 75kg, tan olive skin, short
dark brown hair 3cm messy style, wearing fitted black tactical vest
with cargo pants and leather boots, walking purposefully through frame.
Low-key 3-point lighting setup with hard key from camera left 45°
simulating street lamp (cool 5600K), 1:4 fill ratio creating high
contrast, practical neon signs casting pink and blue accents (3200K).
Teal-orange cinematic LUT with desaturated overall palette, lifted
blacks in shadows, high contrast grade. Volumetric haze creating
visible light shafts through rain particles. 2.39:1 anamorphic aspect
ratio. Noir action atmosphere reminiscent of John Wick cinematography.
Blockbuster production value.
```

## 🎯 Prompt bao gồm

✅ **Camera specs**: Shot type, movement, angle, lens focal length, aperture, DOF
✅ **Characters**: Height (cm), build, weight (kg), skin tone, hair details, costume
✅ **Animals**: Species, size, weight, colors, features (nếu có)
✅ **Lighting**: Setup type, key position, color temp (Kelvin), practicals
✅ **Color grading**: Palette, LUT style, saturation, contrast
✅ **Environment**: Location, set design, time of day, weather, VFX
✅ **Action**: Story beats, movement, pacing, emotional mood
✅ **Style reference**: Comparable films/directors, production value

## ⚙️ Configuration

Chỉnh sửa trong `.env`:

```bash
# Scene detection sensitivity (cao hơn = ít cảnh hơn)
SCENE_THRESHOLD=30.0

# Video resolution khi download
MAX_VIDEO_HEIGHT=1080

# AI model
VISION_MODEL=gpt-4o
```

## 🐛 Troubleshooting

### Lỗi: "OpenAI API key not found"
```bash
# Kiểm tra .env file tồn tại
ls -la .env

# Kiểm tra nội dung
cat .env
```

### Lỗi: "yt-dlp not found"
```bash
# Cài lại
pip install --upgrade yt-dlp

# Hoặc
pip install yt-dlp --force-reinstall
```

### Lỗi: "No module named 'cv2'"
```bash
pip install opencv-python
```

### Video download thất bại
```bash
# Test trực tiếp
yt-dlp "https://youtube.com/watch?v=..."

# Nếu lỗi region block, thử:
yt-dlp --geo-bypass "URL"
```

### API rate limit
- Giảm tốc độ: thêm `time.sleep(2)` trong code
- Upgrade OpenAI plan
- Dùng API key khác

## 💰 Chi phí ước tính

**GPT-4o Vision pricing** (tính theo 1000 tokens):
- Input: $2.50 / 1M tokens
- Output: $10.00 / 1M tokens

**Ước tính cho 1 video:**
- 10 scenes × 2 images/scene = 20 images
- Mỗi image ~1000 tokens
- Mỗi prompt output ~300 tokens
- **Tổng**: ~$0.05 - $0.10 per video

## 📚 Files trong project

- `youtube_scene_by_scene_analyzer.py` - Main script
- `youtube_to_sora_blockbuster.py` - Version cũ (full analysis)
- `requirements.txt` - Python dependencies
- `.env.example` - Template cho API key
- `README.md` - File này

## 🤝 Support

Issues: https://github.com/n8nhahuytoai-tudong/thu-code/issues

## 📄 License

MIT License

---

**Happy prompting!** 🎬✨
