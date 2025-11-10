# 🚀 Quick Start - YouTube to Sora 2 Analyzer

Bắt đầu trong 5 phút!

---

## ⚡ Cài đặt nhanh

### 1. Install dependencies
```bash
pip install openai opencv-python numpy yt-dlp
```

### 2. Install yt-dlp
```bash
# macOS/Linux
brew install yt-dlp

# Windows
winget install yt-dlp

# Hoặc dùng pip
pip install yt-dlp
```

### 3. Tạo API key file
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

Lấy API key tại: https://platform.openai.com/api-keys

---

## 🎬 Chọn version

### Version 2.2 - BLOCKBUSTER (Khuyến nghị) ⭐
✅ Phân tích Hollywood-level
✅ Chi tiết nhất
✅ Học được nhiều nhất

```bash
python youtube_to_sora_blockbuster_v2.2.py
```

### Version 2.1 - STANDARD
✅ Chi tiết nhân vật/con vật
✅ Rẻ hơn ~30%

```bash
python youtube_to_sora_advanced_v2.py
```

**Xem so sánh chi tiết**: `VERSION_COMPARISON.md`

---

## 💻 Chạy ngay

### Cách 1: Command Line (đơn giản nhất)

```bash
# Blockbuster version
python youtube_to_sora_blockbuster_v2.2.py

# Nhập:
# 1. YouTube URL: https://youtube.com/watch?v=...
# 2. Sử dụng cache? y
# 3. Phân tích audio? y
```

### Cách 2: Python Code

```python
# Blockbuster version
from youtube_to_sora_blockbuster_v2 import YouTubeToSoraBlockbusterAnalyzer

analyzer = YouTubeToSoraBlockbusterAnalyzer(api_key="sk-xxx")

result = analyzer.analyze(
    youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
    use_cache=True,
    analyze_audio=True
)

# Xem kết quả
print("=== OVERALL ANALYSIS ===")
print(result['blockbuster_analysis'])

print("\n=== SORA PROMPTS ===")
print(result['sora_prompts'])
```

---

## 📁 Kết quả output

### Blockbuster v2.2
Files trong folder `output_blockbuster/`:
- `Video_Title_BLOCKBUSTER_20250110_143022.txt` - Full report
- `Video_Title_BLOCKBUSTER_20250110_143022.json` - Structured data
- `Video_Title_BLOCKBUSTER_20250110_143022.md` - Formatted

### Standard v2.1
Files trong folder `output_results/`:
- `Video_Title_20250110_143022.txt`
- `Video_Title_20250110_143022.json`
- `Video_Title_20250110_143022.md`

---

## 🎯 Test với video ngắn

**Khuyến nghị cho lần đầu**: Dùng video 30 giây - 2 phút để test

Ví dụ videos phù hợp:
- Music video snippet
- Movie trailer
- Commercial ad
- Short film

**Tránh**:
- Livestreams
- Vlogs tĩnh
- Screen recordings
- Video quá dài (>10 phút)

---

## 💰 Chi phí ước tính

| Video length | Scenes | Cost (v2.1) | Cost (v2.2) |
|--------------|--------|-------------|-------------|
| 30s - 1min | 5-10 | $0.5 - $1.0 | $0.8 - $1.5 |
| 1-2 min | 10-20 | $1.0 - $2.0 | $1.6 - $3.0 |
| 2-5 min | 20-50 | $2.0 - $5.0 | $3.2 - $7.5 |
| 5-10 min | 50-100 | $5.0 - $10.0 | $8.0 - $15.0 |

**Tip**: Dùng cache (use_cache=True) để tránh phân tích lại!

---

## 🎨 Sora Prompts Output

Mỗi video sẽ có **3 prompts**:

### 1. CONCISE (70-90 words)
Ngắn gọn, đủ thông tin chính

### 2. DETAILED TECHNICAL (180-250 words)
Chi tiết đầy đủ:
- Character: height, weight, skin, hair, costume
- Camera: lens, aperture, movement
- Lighting: setup, color temp
- Color grading: LUT style

### 3. CINEMATIC MASTERPIECE (150-200 words)
Nghệ thuật, cảm xúc, film references

**Tất cả bằng TIẾNG ANH** (chuẩn Sora 2)

---

## 🔧 Troubleshooting nhanh

### "OpenAI API key not found"
```bash
# Tạo file .env
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### "yt-dlp not found"
```bash
pip install yt-dlp
```

### "Rate limit exceeded"
Đợi 1 phút hoặc upgrade OpenAI plan

### Video không tải được
- Check URL valid
- Check internet
- Try different video

---

## 📊 Xem kết quả

### TXT file (dễ đọc nhất)
```bash
# macOS/Linux
cat output_blockbuster/Video_Title_BLOCKBUSTER_*.txt

# Windows
type output_blockbuster\Video_Title_BLOCKBUSTER_*.txt
```

### JSON file (for coding)
```python
import json
with open('output_blockbuster/Video_Title_BLOCKBUSTER_20250110.json') as f:
    data = json.load(f)
    print(data['sora_prompts'])
```

### Markdown file (GitHub/Notion)
Upload lên GitHub hoặc import vào Notion

---

## 🎓 Example Workflow

### Workflow cho người mới:

1. **Test video ngắn** (1 phút)
   ```bash
   python youtube_to_sora_blockbuster_v2.2.py
   ```

2. **Review output** trong `output_blockbuster/`
   - Mở file .txt để xem analysis
   - Kéo xuống cuối xem 3 Sora prompts

3. **Copy prompt yêu thích**
   - Chọn 1 trong 3 prompts
   - Copy vào Sora 2

4. **Generate video** trong Sora 2

5. **So sánh** original vs generated
   - Điều chỉnh prompt nếu cần
   - Iterate!

### Workflow cho pro:

1. Analyze 3-5 videos cùng style
2. Compare technical approaches
3. Identify patterns
4. Create custom prompt template
5. Batch generate với Sora 2

---

## 💡 Tips hữu ích

### 1. Cache = tiền
```python
analyzer.analyze(use_cache=True)  # Luôn bật!
```

### 2. Video ngắn = rẻ
2 phút video tốt hơn 10 phút video dở

### 3. Check scenes trước
Nếu quá nhiều scenes (>100), video sẽ đắt

### 4. Professional videos = better results
- ✅ Music videos
- ✅ Movie trailers
- ✅ Commercials
- ❌ Vlogs
- ❌ Livestreams

### 5. Edit prompts
Prompts AI-generated có thể cần điều chỉnh nhẹ

---

## 📚 Đọc thêm

- **Full docs v2.2**: `README_BLOCKBUSTER.md`
- **Full docs v2.1**: `README_V2.md`
- **So sánh versions**: `VERSION_COMPARISON.md`

---

## 🎬 Example Videos to Try

### Beginner (easy, cheap):
- Short commercials (30s)
- Music video clips (1min)
- Movie trailers (2min)

### Intermediate:
- Full music videos (3-4min)
- Short films (5min)
- Product videos (3min)

### Advanced (expensive):
- Long-form content (10min+)
- Documentary clips
- Complex narratives

---

## 🚨 Common Mistakes

### ❌ Quên set API key
```bash
# Fix: Tạo .env file
echo "OPENAI_API_KEY=sk-xxx" > .env
```

### ❌ Video quá dài lần đầu
**Fix**: Start với 1-2 phút

### ❌ Không dùng cache
**Fix**: Luôn use_cache=True

### ❌ Dùng video chất lượng thấp
**Fix**: Chọn videos HD với good production

---

## ⚡ One-Liner Commands

### Install all
```bash
pip install openai opencv-python numpy yt-dlp && brew install yt-dlp
```

### Setup API key
```bash
read -p "Enter OpenAI API key: " KEY && echo "OPENAI_API_KEY=$KEY" > .env
```

### Quick run
```bash
python youtube_to_sora_blockbuster_v2.2.py
```

### View latest result
```bash
ls -t output_blockbuster/*.txt | head -1 | xargs cat
```

---

## 🎯 Next Steps

1. ✅ Cài đặt dependencies
2. ✅ Setup API key
3. ✅ Test với video ngắn
4. ✅ Review output
5. ✅ Try với Sora 2
6. Read full documentation
7. Experiment với settings
8. Share your results!

---

## 💬 Need Help?

1. Check `README_BLOCKBUSTER.md` for detailed info
2. Review `VERSION_COMPARISON.md` to choose version
3. Check error logs in terminal
4. Verify API key valid
5. Test internet connection

---

## 🎉 You're Ready!

```bash
python youtube_to_sora_blockbuster_v2.2.py
```

**Happy analyzing! 🎬**

---

*Từ YouTube → Hollywood-level analysis → Perfect Sora 2 prompts*
