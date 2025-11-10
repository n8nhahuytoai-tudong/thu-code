# 🎬 YouTube to Sora 2 - BLOCKBUSTER ANALYZER v2.2

## 🌟 Hollywood Production Standards

Phân tích video YouTube theo **tiêu chuẩn phim bom tấn Hollywood**, tạo prompts chuyên nghiệp cho Sora 2.

---

## 🎯 Tính năng đặc biệt v2.2

### 🎬 Cinematography Analysis
- **Camera movements**: Dolly/crane/steadicam/tracking/handheld/gimbal
- **Camera angles**: Eye-level/high/low/dutch/overhead/worm's-eye
- **Shot types**: Wide/full/medium/close-up/extreme close-up
- **Lens specs**: Focal length (18mm/35mm/50mm/85mm/200mm)
- **Depth of field**: Shallow (f/1.4)/medium/deep (f/16)
- **Focus techniques**: Rack focus/selective/deep focus
- **Composition**: Rule of thirds/golden ratio/symmetry
- **Frame analysis**: Headroom, lead room, safe areas
- **Aspect ratio**: 16:9/2.39:1/1.85:1/IMAX

### 💡 Professional Lighting
- **Lighting setups**: 3-point/Rembrandt/butterfly/split/natural
- **Key light**: Position, intensity, quality (hard/soft)
- **Fill ratio**: High contrast/balanced/flat
- **Color temperature**: Kelvin values (2700K-7000K)
- **Practical lights**: Visible sources in frame
- **Light quality**: Hard shadows vs soft diffused
- **Direction**: Top/side/back lighting
- **Atmosphere**: Haze/fog/volumetric lighting

### 🎨 Color Grading & LUT Analysis
- **Color palette**: Warm/cool/complementary/analogous
- **LUT styles**: Teal-orange/bleach bypass/cinematic/naturalistic
- **Saturation**: Vibrant/desaturated/selective color
- **Contrast approach**: High/lifted blacks/crushed
- **Mood through color**: Emotional color coding
- **Film stock simulation**: Digital cinema/film look

### 👥 Character Physical Specifications
Mô tả CỰC KỲ chi tiết:
- **Height estimates**: 160cm/170cm/185cm
- **Build & weight**: Athletic 75kg, slim 55kg, muscular 90kg
- **Skin tone chính xác**: Pale ivory/fair/tan/olive/bronze/brown/deep brown/ebony
- **Hair details**:
  - Color: Platinum blonde/golden/light brown/chestnut/dark brown/black/auburn/gray/silver
  - Style: Slicked back/messy/wavy/curly/straight/braided/dreadlocks
  - Length: Buzz cut/short/medium/shoulder-length/long/very long
- **Facial features**: Angular/soft/chiseled, jawline, cheekbones, eye color
- **Body proportions**: Head-to-body ratio (1:7, 1:8), leg length, shoulders
- **Costume design**:
  - Era: Contemporary/period/futuristic/fantasy
  - Type: Casual/formal/tactical/uniform
  - Colors: Dominant + accent colors
  - Materials: Leather/silk/cotton/metal/synthetic
  - Fit: Tailored/fitted/loose/oversized
  - Accessories: Jewelry/watches/glasses/hats/weapons
- **Performance**: Body language, facial expressions, eye line

### 🐾 Animal/Creature Detailed Specs
- **Species & breed**: Specific identification
- **Size dimensions**:
  - Height at shoulder: 30cm/70cm/160cm
  - Body length + tail length
  - Weight estimates: 3kg cat, 35kg dog, 500kg horse
- **Physical characteristics**:
  - Coat color & pattern: Solid/spotted/striped/mottled
  - Texture: Fluffy/sleek/rough/shiny
  - Features: Ears, tail, eyes, teeth, claws
  - Body proportions: Head:body:legs ratio
- **Movement & behavior**: Gait, speed, actions

### 🏞️ Production Design Analysis
- **Location assessment**: Practical/studio/green screen
- **Set design quality**: Detail level, period accuracy
- **Props & dressing**: Attention to detail
- **Architecture**: Style, period, scale
- **World-building**: Consistency, believability
- **Depth layers**: Foreground/mid/background elements

### ✨ VFX & Post-Production
- **CGI usage**: None/minimal/moderate/heavy
- **Quality assessment**: Professional/amateur (1-10 scale)
- **Compositing**: Green screen, matte paintings, seamless/visible
- **Particle effects**: Smoke/dust/sparks/magic/explosions
- **Digital enhancement**: Sky replacement, cleanup, beauty work
- **Motion graphics**: HUD elements, text overlays

### 🎭 Story & Genre Analysis
- **Story structure**: Three-act structure breakdown
- **Character arcs**: Development tracking
- **Dramatic tension**: Conflict analysis
- **Pacing**: Rhythm, tempo changes, story beats
- **Genre conventions**: Action/drama/sci-fi/horror/comedy/thriller
- **Tone analysis**: Serious/dark/light/epic/intimate

### 📊 Quality Scoring System
Đánh giá từ 1-10:
- **Camera work**: Stability, movement, framing
- **Lighting**: Setup complexity, mood creation
- **Color grading**: Consistency, artistic vision
- **VFX quality**: Realism, integration
- **Production value**: Budget level impression
- **Cinematic quality**: Overall Hollywood comparison
- **Blockbuster score**: AAA/studio/mid-budget/indie

### 🎵 Audio Analysis (if available)
- **Dialogue**: Transcript with timing
- **Sound design indicators**: Quality assessment
- **Music/score**: Mood analysis
- **Audio production**: Professional level

---

## 📋 So sánh các phiên bản

| Feature | v1.0 | v2.1 | v2.2 Blockbuster |
|---------|------|------|------------------|
| Max scenes | 20 | 999 | 999 |
| Character details | Basic | Height, weight, skin, hair | + Body proportions, costume materials, accessories |
| Animal details | Basic | Species, size, colors | + Breed, exact measurements, coat texture, behavior |
| Camera analysis | Basic | Movement, angle | + Lens specs, aperture, focus techniques, aspect ratio |
| Lighting | Basic | Mood | + Setup types, color temp, key/fill/back, practicals |
| Color grading | None | Basic | + LUT styles, saturation, contrast, mood through color |
| Production design | None | Basic | + Set quality, props, world-building, depth layers |
| VFX analysis | None | None | + CGI usage, compositing, quality scoring |
| Story structure | None | None | + 3-act structure, character arcs, pacing |
| Genre analysis | None | None | + Genre conventions, tone, tropes |
| Quality scoring | None | None | + 1-10 scale for all technical aspects |
| Output folder | output_results | output_results | output_blockbuster |
| Prompt length | 50-150w | 60-200w | 70-250w |

---

## 🚀 Cài đặt

### 1. Python packages
```bash
pip install openai opencv-python numpy yt-dlp
```

### 2. yt-dlp
```bash
# macOS
brew install yt-dlp

# Windows
winget install yt-dlp

# Linux
sudo apt install yt-dlp
```

### 3. OpenAI API Key
Tạo file `.env`:
```
OPENAI_API_KEY=sk-your-api-key-here
```

---

## 🎬 Cách sử dụng

### Command line
```bash
python youtube_to_sora_blockbuster_v2.2.py
```

Nhập:
- YouTube URL
- API key (nếu chưa có .env)
- Options (cache, audio)

### Python code
```python
from youtube_to_sora_blockbuster_v2 import YouTubeToSoraBlockbusterAnalyzer

analyzer = YouTubeToSoraBlockbusterAnalyzer(api_key="sk-xxx")

result = analyzer.analyze(
    youtube_url="https://youtube.com/watch?v=...",
    use_cache=True,
    analyze_audio=True
)

# Access results
print(result['blockbuster_analysis'])
print(result['sora_prompts'])
```

---

## 📁 Output Files

Tất cả lưu trong folder **`output_blockbuster/`**:

### 1. TXT File
```
Video_Title_BLOCKBUSTER_20250110_143022.txt
```
Bao gồm:
- Video metadata
- Blockbuster-level overall analysis:
  * Story structure & narrative
  * Characters in-depth
  * Cinematography analysis
  * Lighting design
  * Color grading & visual style
  * Production design
  * VFX & post-production
  * Technical quality assessment (scored)
  * Genre & style
  * Overall production value
  * Sora 2 generation insights
- Scene-by-scene breakdown (Hollywood standards)
- Transcript
- 3 Sora 2 prompts (blockbuster quality)

### 2. JSON File
```json
{
  "video_info": {...},
  "blockbuster_analysis": "...",
  "scenes": [...],
  "transcript": {...},
  "sora_prompts": "...",
  "version": "2.2-BLOCKBUSTER",
  "analysis_standards": [
    "hollywood_cinematography",
    "professional_lighting",
    "color_grading_analysis",
    ...
  ]
}
```

### 3. Markdown File
Formatted report với sections:
- Blockbuster-level overall analysis
- Scene-by-scene technical breakdown
- Transcript
- Sora 2 prompts
- Analysis standards checklist

---

## 🎨 Sora 2 Prompts - Blockbuster Level

### 1. CONCISE BLOCKBUSTER PROMPT (70-90 words)
Súc tích nhưng packed with details:
```
A tall athletic man (185cm, 80kg) with olive skin and dark brown
short hair, wearing a fitted navy tactical jacket, runs through a
dystopian cityscape at sunset. Steadicam tracking shot at eye level,
35mm lens f/2.8 shallow DOF. 3-point lighting with warm 3200K key
from left, cool rim light. Teal-orange grading, high contrast.
Cyberpunk aesthetic with neon accents. 2.39:1 anamorphic.
Blockbuster production value.
```

### 2. DETAILED TECHNICAL PROMPT (180-250 words)
Full specifications:
```
CHARACTERS: Tall athletic protagonist (approximately 185cm, 80kg)
with olive skin tone, angular facial features, dark brown hair in
modern fade cut (short sides, textured top). Wearing fitted navy
blue tactical jacket (synthetic material, high collar), black cargo
pants, combat boots. Body proportions: 1:8 head-to-body ratio,
broad shoulders, narrow waist, long legs. Running with determined
expression.

CINEMATOGRAPHY: Steadicam tracking shot following character from
behind-side at eye level. 35mm lens, f/2.8 aperture for shallow
depth of field (subject sharp, background bokeh). Smooth forward
dolly movement matching running speed. 2.39:1 anamorphic aspect
ratio. Rule of thirds composition with character on left third.

LIGHTING: Professional 3-point setup. Warm key light (3200K) from
camera left 45°, soft quality through diffusion. Cool rim light
(5600K) from back right for edge separation. Low ambient fill.
Practical neon signs as motivated color accents. Golden hour natural
backlight.

COLOR GRADING: Cinematic teal-orange LUT. Desaturated mid-tones,
vibrant accent colors. High contrast with slightly lifted blacks.
Warm highlights, cool shadows. Film grain overlay.

ENVIRONMENT: Dystopian urban street, wet pavement reflections,
neon signage depth, atmospheric haze. Cyberpunk aesthetic.

GENRE: Sci-fi action thriller. Fast-paced, intense mood. AAA
blockbuster production quality.
```

### 3. CINEMATIC MASTERPIECE PROMPT (150-200 words)
Artistic vision:
```
In the style of Denis Villeneuve's Blade Runner 2049 meets
Christopher Nolan's action choreography: A lone figure - embodiment
of determination in physical form (tall, athletic build with warrior's
proportions) - races through twilight's dying light. His olive-toned
skin catches the amber glow of a setting sun that bleeds through
dystopian towers, dark hair wind-swept in motion's poetry.

Steadicam glides behind him, intimate yet epic - we're not observers
but companions in his desperate flight. Shallow focus isolates him
from the chaos of neon-drenched decay, his navy jacket a spot of
military precision in anarchic urban wilderness.

Light becomes character: warm key sculpts determination into his
features while cool rim light crowns him in hope's last gleam. The
city breathes through practical neons - cyan, magenta, gold - each
a story untold. Teal-orange grading speaks of futures both warm and
cold, human and machine.

Anamorphic 2.39:1 frames not just action but emotion - the loneliness
of heroism, the weight of purpose. Every technical choice serves one
truth: this moment matters.

Blockbuster craftsmanship meets auteur vision. Cinema as art.
```

---

## 💡 Ví dụ đầu ra

### Before (Basic):
```
A man walking in a street at sunset
```

### After (Blockbuster v2.2):
```
Medium shot of a tall athletic man (185cm, 80kg) with olive skin tone,
short dark brown hair in modern fade, wearing a fitted navy blue
button-down shirt (cotton, rolled sleeves) and dark gray chinos,
walking with confident stride through an urban street at golden hour.
Steadicam tracking shot at eye level following from front-side, 50mm
lens at f/2.0 for shallow depth of field with soft bokeh background.
Natural key light from setting sun (3200K) positioned camera right
creating warm rim light, filled softly with ambient skylight. Cinematic
teal-orange color grading with vibrant saturation and lifted blacks for
dreamy atmosphere. Contemporary urban environment with depth layers:
out-of-focus pedestrians in background, street furniture mid-ground,
clean composition following rule of thirds. 2.39:1 aspect ratio.
Documentary-meets-narrative style. Indie film production value with
professional polish. Peaceful, contemplative mood.
```

---

## ⚙️ Configuration

File `youtube_to_sora_blockbuster_v2.2.py`, class `Config`:

```python
class Config:
    SCENE_THRESHOLD = 30.0       # Scene detection sensitivity
    MIN_SCENE_LENGTH = 15        # Min frames per scene
    FRAMES_PER_SCENE = 4         # Frames to analyze per scene

    MAX_SCENES_TO_ANALYZE = 999  # Unlimited!

    VISION_MODEL = "gpt-4o"      # OpenAI vision model
    TEXT_MODEL = "gpt-4o"
    WHISPER_MODEL = "whisper-1"

    OUTPUT_DIR = "output_blockbuster"  # Output folder
```

Có thể chỉnh:
- `SCENE_THRESHOLD`: 20-40 (thấp = nhiều scenes, cao = ít scenes)
- `FRAMES_PER_SCENE`: 2-6 (nhiều = chi tiết hơn, đắt hơn)
- `MAX_SCENES_TO_ANALYZE`: Giới hạn nếu muốn tiết kiệm

---

## 💰 Chi phí

**OpenAI GPT-4o Vision** với phân tích blockbuster:
- 1 scene (~4 frames + long prompt): **$0.08 - $0.15**
- Video 30 scenes: **$2.4 - $4.5**
- Video 50 scenes: **$4.0 - $7.5**
- Video 100 scenes: **$8.0 - $15.0**

**Cao hơn v2.1** vì:
- Prompts dài hơn (3500 tokens)
- Max output tokens cao hơn (4000 tokens)
- Phân tích chi tiết hơn

### Cách tiết kiệm:
1. **Dùng cache** (use_cache=True)
2. **Test video ngắn trước**
3. **Giảm FRAMES_PER_SCENE** từ 4 → 3
4. **Tăng SCENE_THRESHOLD** để ít scenes hơn

---

## 📊 Technical Terms Glossary

### Camera
- **Dolly**: Camera di chuyển trên ray/wheels
- **Crane**: Camera trên cần cẩu (lên xuống)
- **Steadicam**: Gimbal ổn định cầm tay
- **Tracking**: Theo chuyển động của subject
- **Pan**: Quay ngang (left/right)
- **Tilt**: Nghiêng dọc (up/down)
- **Dutch angle**: Nghiêng chéo

### Lenses
- **Wide (18-35mm)**: Góc rộng, depth
- **Normal (50mm)**: Mắt người
- **Portrait (85mm)**: Chân dung đẹp
- **Telephoto (100-200mm)**: Nén không gian
- **f/1.4-2.8**: Aperture lớn = shallow DOF
- **f/8-16**: Aperture nhỏ = deep DOF

### Lighting
- **3-point**: Key + Fill + Back light
- **Rembrandt**: Triangle of light on cheek
- **Butterfly**: Light from above, shadow under nose
- **Practical**: Visible light sources in frame
- **2700-3500K**: Warm (sunset, tungsten)
- **5500-7000K**: Cool (daylight, overcast)

### Color Grading
- **Teal-Orange**: Hollywood blockbuster look
- **Bleach Bypass**: Desaturated, contrasty
- **LUT**: Look-up table for color transform
- **Lifted blacks**: Không crush đen hoàn toàn

---

## 🎯 Use Cases

### 1. Filmmakers
Phân tích phim/trailer để học technical execution

### 2. Sora 2 Creators
Tạo prompts chuyên nghiệp cho video generation

### 3. Film Students
Học cinematography, lighting, color grading từ examples

### 4. Video Analysts
Breakdown technical aspects của productions

### 5. Content Creators
Nâng cấp production value cho content

---

## 🐛 Troubleshooting

### "API key not found"
**Fix**: Tạo file `.env` với `OPENAI_API_KEY=sk-xxx`

### "yt-dlp not found"
**Fix**:
```bash
pip install yt-dlp
# hoặc
brew install yt-dlp
```

### "Rate limit exceeded"
**Fix**:
- Đợi 1 phút
- Nâng cấp OpenAI tier
- Thêm delays giữa API calls

### "Out of memory"
**Fix**:
- Giảm MAX_VIDEO_HEIGHT từ 1080 → 720
- Giảm FRAMES_PER_SCENE từ 4 → 3

### Video quá dài (>200 scenes)
**Fix**:
- Cắt video thành parts
- Hoặc tăng SCENE_THRESHOLD
- Hoặc set MAX_SCENES_TO_ANALYZE = 100

---

## 📝 Tips & Best Practices

### 1. Video Selection
✅ **Good for analysis:**
- Professional productions
- Music videos với high production value
- Movie trailers
- Commercial ads
- Cinematic YouTube content

❌ **Not ideal:**
- Vlogs tĩnh
- Screen recordings
- Low-res videos
- Livestreams

### 2. Optimal Video Length
- **2-5 minutes**: Ideal, $3-10
- **5-10 minutes**: Good, $10-25
- **10+ minutes**: Expensive, $25+

### 3. Scene Detection
Nếu quá nhiều scenes (>100):
```python
Config.SCENE_THRESHOLD = 40.0  # Tăng từ 30
Config.MIN_SCENE_LENGTH = 30   # Tăng từ 15
```

### 4. Quality Check
Luôn kiểm tra output đầu tiên:
- Xem scene breakdown có chính xác không
- Character descriptions có đủ chi tiết không
- Technical terms có chính xác không

### 5. Prompt Editing
Sora prompts có thể cần edit:
- Remove details không cần thiết
- Adjust cho specific requirements
- Combine elements từ multiple prompts

---

## 🔄 Workflow Recommendations

### Standard Workflow:
1. **Test với video ngắn** (30s-1min)
2. **Review output** để adjust settings
3. **Chạy full video**
4. **Review detailed analysis**
5. **Edit prompts** nếu cần
6. **Use in Sora 2**

### Pro Workflow:
1. Analyze multiple similar videos
2. Compare technical approaches
3. Identify patterns (lighting/color/camera)
4. Create custom prompt templates
5. Apply to Sora 2 generation
6. Iterate based on results

---

## 🎓 Learning Resources

### Cinematography
- "Cinematography: Theory and Practice" - Blain Brown
- "Shot by Shot" - Steven D. Katz
- MasterClass: Roger Deakins

### Lighting
- "Set Lighting Technician's Handbook" - Harry Box
- "Painting with Light" - John Alton

### Color Grading
- "Color Correction Handbook" - Alexis Van Hurkman
- DaVinci Resolve tutorials

---

## 📞 Support

Issues:
1. Check API key valid
2. Check yt-dlp installed
3. Check internet connection
4. Review error logs
5. Try with shorter video
6. Check OpenAI account has credits

---

## 🔮 Future Enhancements

Planned for v2.3:
- [ ] Shot-by-shot timeline visualization
- [ ] Automatic LUT identification
- [ ] Film reference matching
- [ ] Director style classification
- [ ] Automated quality scoring
- [ ] Batch processing multiple videos
- [ ] Custom prompt templates
- [ ] Shot list generation
- [ ] Storyboard suggestions

---

## 🏆 Version Comparison

**Choose v2.0** if: Basic needs, low budget
**Choose v2.1** if: Need character/animal details
**Choose v2.2 Blockbuster** if: Professional use, maximum detail, learning cinematography

---

## 📜 License

MIT License - Free to use and modify

---

## 🙏 Credits

- OpenAI GPT-4o Vision for analysis
- yt-dlp for video downloading
- OpenCV for frame extraction
- Whisper for transcription

---

**Made with 🎬 for filmmakers, creators, and Sora 2 enthusiasts**

*Transform any YouTube video into Hollywood-grade analysis and professional Sora 2 prompts*
