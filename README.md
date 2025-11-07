# 🎬 Enhanced Video Generation System

Hệ thống tạo video AI với pipeline xử lý scenes đầy đủ: đồng bộ nhân vật, VFX, hiệu ứng khói lửa và tóm lược.

## 📋 Tổng quan

Dự án này cung cấp một pipeline hoàn chỉnh để:
1. Tạo kịch bản phân cảnh với AI (GPT-4)
2. **Đồng bộ nhân vật** (Character Consistency)
3. **Thêm hiệu ứng VFX** (Visual Effects)
4. **Thêm khói lửa** (Smoke/Fire Effects)
5. **Tóm lược và sync scenes** (Scene Analysis)
6. Gửi đến API tạo video (Sora 2 / Veo 3)

## 🗂️ Cấu trúc dự án

```
thu-code/
├── scenes_trex_vs_pteranodon.json    # Scenes gốc (20 cảnh T-Rex vs Pteranodon)
├── scene_processor.py                 # Script xử lý chính với 4 nodes
├── demo_pipeline.py                   # Demo chi tiết từng bước
├── upload_scenes_to_sheets.py        # Upload lên Google Sheets
├── workflow_enhanced_video_generation.json  # n8n workflow đầy đủ
├── My workflow 7.json                # n8n AI chat workflow
├── scenes_processed.json             # Output đã xử lý
├── ready_to_upload.json              # Format cho Google Sheets
├── PIPELINE_GUIDE.md                 # Hướng dẫn chi tiết
└── README.md                         # File này
```

## 🚀 Quick Start

### 1. Chạy Demo Pipeline

```bash
python3 demo_pipeline.py
```

Output sẽ hiển thị:
- Chi tiết xử lý từng node cho 3 scenes đầu
- Statistics tổng quan
- Phân tích action types, mood, camera angles
- File output: `scenes_processed_demo.json`

### 2. Xử lý Scenes

```bash
python3 scene_processor.py
```

Output: `scenes_processed.json` với đầy đủ enhancement

### 3. Sử dụng n8n Workflow

**A. Chat Workflow (Tạo kịch bản)**:
1. Import `My workflow 7.json` vào n8n
2. Kết nối Google Sheets
3. Chat với AI để tạo scenes
4. Scenes được lưu vào Google Sheets với status="Ready"

**B. Processing Workflow (Xử lý & tạo video)**:
1. Import `workflow_enhanced_video_generation.json`
2. Cấu hình Video Generation API endpoint
3. Workflow tự động:
   - Trigger khi có scenes mới (status="Ready")
   - Xử lý qua 4 nodes enhancement
   - Gửi đến API tạo video
   - Update status="Complete"

## 🎯 Pipeline Nodes

### Node 1: Character Consistency 🎭

**Mục đích**: Đảm bảo nhân vật có hình ảnh nhất quán

**Character Profiles**:
- **T-Rex**: Da xanh sẫm có vân, mắt vàng chanh, răng trắng ngà, 15m cao
- **Pteranodon**: Cánh xám xanh 7m, mỏ cam đậm, mào đỏ sẫm, mắt đỏ tía

**Example**:
```
Input:  "T-Rex xuất hiện bước đi"
Output: "T-Rex xuất hiện bước đi [răng nanh dài cong, màu trắng ngà bóng]"
```

### Node 2: VFX Enhancement ✨

**VFX Library**: dust_cloud, tree_shake, ground_crack, impact_flash, motion_blur, lens_flare, debris

**Auto-detection**:
- "chạy/trốn" → dust_cloud + motion_blur
- "nhảy/tránh" → ground_crack + debris
- "va chạm" → impact_flash

**Example**:
```
Input:  "T-Rex chạy trốn trong rừng"
Output: "T-Rex chạy trốn trong rừng [VFX: đám bụi bay; motion blur; cây rung]"
```

### Node 3: Smoke/Fire Effects 🔥

**Effects Library**: dust_impact, breathing_mist, battle_dust, fire_sparks, heat_wave, impact_explosion

**Auto-detection**:
- "chân/bước" → dust_impact
- "gầm/tru" → breathing_mist
- "va chạm" → fire_sparks + explosion
- "chiến đấu" → battle_dust

**Example**:
```
Input:  "T-Rex tru lên mở hàm rộng"
Output: "T-Rex tru lên mở hàm rộng [SFX: hơi thở tạo sương mù nhẹ]"
```

### Node 4: Scene Summarization 📊

**Phân tích**:
- Characters: Nhân vật xuất hiện
- Action Type: Chase / Combat / Close-up / Wide shot
- Camera Angle: Close-up / Wide / Medium
- Mood: Mysterious / Intense / Fearful / Action

**Output**: JSON structure với đầy đủ metadata

## 📊 Demo Results

Từ demo với 20 scenes T-Rex vs Pteranodon:

**Enhancement Coverage**:
- Character Details: 10% scenes (khi có nhân vật)
- VFX Effects: 65% scenes
- Smoke/Fire Effects: 70% scenes
- Overall: 48.3% enhancement coverage

**Scene Distribution**:
- Action Types: 60% Transition, 10% Chase, 10% Combat, 10% Close-up, 10% Wide
- Moods: 75% Action, 10% Fearful, 10% Intense, 5% Mysterious
- Camera: 75% Medium, 15% Wide, 10% Close-up

**Enhancement Stats**:
- Average +120 chars per scene (~150% increase)
- Total video duration: 160s (2.7 minutes)

## 🔧 API Integration

### Video Generation API Format

```json
POST https://api.sora.openai.com/v1/generate
{
  "prompt": "Enhanced scene description with [character] [VFX] [SFX]",
  "duration": 8,
  "scene_number": 1,
  "quality": "high",
  "model": "sora-2"
}
```

### Google Sheets Format

| id | scenes | status | task id | video link |
|----|--------|--------|---------|------------|
| trex_001 | {"shots":[...]} | Ready | | |

## 📝 Ví dụ đầy đủ

### Input (Original):
```
"Pteranodon phát hiện T-Rex và bắt đầu lao xuống truy đuổi."
```

### Processing Steps:

**Node 1 - Character**:
```
"Pteranodon phát hiện T-Rex và bắt đầu lao xuống truy đuổi.
[mỏ dài nhọn màu cam đậm, không có răng]"
```

**Node 2 - VFX**:
```
"... [mỏ dài nhọn màu cam đậm, không có răng]
[VFX: motion blur khi di chuyển nhanh]"
```

**Node 3 - Effects**:
```
"... [VFX: motion blur khi di chuyển nhanh]
[SFX: khói bụi dày bao trùm chiến đấu]"
```

**Node 4 - Summary**:
```json
{
  "characters": ["T-Rex", "Pteranodon"],
  "action_type": "Chase",
  "camera_angle": "Wide angle",
  "mood": "Intense"
}
```

## 🛠️ Customization

### Thêm Character mới

Edit `scene_processor.py`:
```python
self.character_profiles["NewCharacter"] = {
    "description": "Mô tả",
    "consistent_details": ["chi tiết 1", "chi tiết 2"],
    "scale": "kích thước"
}
```

### Thêm VFX mới

```python
self.vfx_library["new_effect"] = "mô tả hiệu ứng"
```

### Custom Auto-detection

Thêm logic trong `add_vfx_effects()`:
```python
if 'keyword' in scene_lower:
    vfx_to_add.append(self.vfx_library["effect_name"])
```

## 📖 Documentation

Chi tiết đầy đủ xem: **[PIPELINE_GUIDE.md](PIPELINE_GUIDE.md)**

## 🎥 Sample Output

Scenes đã xử lý sẵn sàng cho video generation:
- ✅ Character consistency across all scenes
- ✅ VFX added to 13/20 scenes
- ✅ Smoke/fire effects in 14/20 scenes
- ✅ Complete scene analysis and metadata
- ✅ Ready for Sora 2 / Veo 3 API

## 🔄 Workflow Diagram

```
┌─────────────────────┐
│  Google Sheets      │ status="Ready"
│  (Input Scenes)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Filter             │ Check status="Ready"
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Parse JSON         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 🎭 Node 1:          │ Character Consistency
│ Character Sync      │ + Nhân vật details
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ ✨ Node 2:          │ VFX Enhancement
│ Add VFX             │ + Visual effects
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 🔥 Node 3:          │ Smoke/Fire Effects
│ Add Effects         │ + Smoke, fire, heat
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 📊 Node 4:          │ Scene Analysis
│ Summarize & Sync    │ + Metadata, analysis
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Update Status       │ status="Processed"
│ (Google Sheets)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Split Batches       │ Chia scenes để xử lý
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Send to Video API   │ Sora 2 / Veo 3
│ (For each scene)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Update Complete     │ status="Complete"
│ + Video links       │ + video_url
└─────────────────────┘
```

## 📦 Dependencies

```
Python 3.x
- json (built-in)
- re (built-in)
```

n8n workflow yêu cầu:
- Google Sheets integration
- HTTP Request node
- Function node
- Split In Batches node

## 🎓 Use Cases

1. **AI Video Generation**: Tạo video từ kịch bản text
2. **Story Visualization**: Chuyển truyện thành scenes có thể tạo video
3. **Content Creation**: Tạo nội dung video marketing/education
4. **Game Cutscenes**: Thiết kế cutscene cho game
5. **Film Pre-production**: Storyboard và pre-viz

## 📄 License

MIT License - Free to use and modify

## 🤝 Contributing

Contributions welcome! Đặc biệt:
- Thêm character profiles mới
- Mở rộng VFX library
- Cải thiện auto-detection logic
- Tích hợp với video generation platforms khác

## 📧 Support

Xem chi tiết tại `PIPELINE_GUIDE.md` hoặc chạy `python3 demo_pipeline.py` để xem demo.

---

Made with ❤️ for AI Video Generation
