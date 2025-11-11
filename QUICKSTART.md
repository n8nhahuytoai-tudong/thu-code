# 🚀 Quick Start Guide

## Cài đặt trong 3 phút

### 1. Cài dependencies
```bash
pip install -r requirements.txt
```

### 2. Tạo file .env với API key
```bash
# Cách 1: Copy template
cp .env.example .env
# Sau đó mở .env và thêm API key của bạn

# Cách 2: Tạo trực tiếp
echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
```

**Lấy API key**: https://platform.openai.com/api-keys

### 3. Kiểm tra cài đặt
```bash
python test_installation.py
```

Nếu thấy "✓ TẤT CẢ ĐÃ SẴN SÀNG!" → OK!

### 4. Chạy
```bash
python youtube_scene_by_scene_analyzer.py
```

Nhập YouTube URL và chờ!

---

## Output

```
output_scenes/
  VideoTitle_20250111_123456/
    scene_0000/
      FIRST_frame.jpg   ← Ảnh đầu cảnh
      LAST_frame.jpg    ← Ảnh cuối cảnh
      sora_prompt.txt   ← Prompt 150-200 words
    scene_0001/
      ...
    00_SUMMARY.txt
    scenes_data.json
```

---

## Troubleshooting nhanh

**"yt-dlp not found"**
```bash
pip install yt-dlp
```

**"OpenAI API key not found"**
```bash
# Kiểm tra file .env tồn tại
cat .env

# Nếu không có, tạo mới
echo "OPENAI_API_KEY=sk-your-key" > .env
```

**"No module named cv2"**
```bash
pip install opencv-python
```

---

## Chi phí

~$0.05 - $0.10 per video (GPT-4o Vision)

---

**Đọc đầy đủ**: README.md
