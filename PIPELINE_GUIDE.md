# 🎬 Enhanced Video Generation Pipeline

## Tổng quan

Pipeline này xử lý scenes từ Google Sheets, thêm đồng bộ nhân vật, hiệu ứng VFX, khói lửa, và tóm lược trước khi gửi đến API tạo video (Sora 2 / Veo 3).

## 📋 Quy trình xử lý

```
Google Sheets (Status: Ready)
    ↓
Filter (Lọc scenes sẵn sàng)
    ↓
Parse Scenes JSON
    ↓
[1] Character Consistency (Đồng bộ nhân vật)
    ↓
[2] VFX Enhancement (Thêm hiệu ứng)
    ↓
[3] Smoke/Fire Effects (Thêm khói lửa)
    ↓
[4] Summarize & Sync (Tóm lược)
    ↓
Update Google Sheets (Status: Processed)
    ↓
Split Into Batches (Chia scenes)
    ↓
Send to Video Generation API
    ↓
Update Google Sheets (Status: Complete)
```

## 🔧 Các Node xử lý

### 1️⃣ Character Consistency Node

**Mục đích**: Đảm bảo nhân vật có hình ảnh nhất quán qua các cảnh

**Character Profiles**:

**T-Rex**:
- Da có vân sần sùi màu xanh sẫm pha nâu đất
- Mắt vàng chanh với đồng tử đen sâu thẳm
- Răng nanh dài cong, màu trắng ngà bóng
- Cơ bắp chân sau cuồn cuộn, móng vuốt đen nhọn
- Đuôi dài khỏe, vảy lớn ở lưng
- Scale: 15m chiều cao, 40 tấn

**Pteranodon**:
- Cánh xương dài 7 mét, da cánh mỏng màu xám xanh
- Mỏ dài nhọn màu cam đậm, không có răng
- Mào đầu đỏ sẫm hình mũi mác
- Vuốt chân sắc nhọn màu đen bóng
- Mắt lớn màu đỏ tía, nhìn sắc bén
- Scale: sải cánh 7m, cân nặng 200kg

**Output**: Thêm chi tiết nhân vật vào mô tả cảnh
```
Ví dụ:
Input: "T-Rex xuất hiện bước đi uy nghi"
Output: "T-Rex xuất hiện bước đi uy nghi [răng nanh dài cong, màu trắng ngà bóng]"
```

### 2️⃣ VFX Enhancement Node

**Mục đích**: Thêm hiệu ứng visual phù hợp với hành động

**VFX Library**:
- **dust_cloud**: Đám bụi bay dày đặc (khi chạy, di chuyển)
- **tree_shake**: Cây cối rung lắc, lá rụng (môi trường rừng)
- **ground_crack**: Nứt đất lan tỏa, sỏi đá bật lên (khi nhảy, đạp mạnh)
- **impact_flash**: Tia sáng trắng xanh (khi va chạm)
- **motion_blur**: Mờ động (di chuyển tốc độ cao)
- **lens_flare**: Chớp sáng mặt trời (cảnh outdoor)
- **debris**: Mảnh vỡ cây cối bay (khi phá hủy)

**Logic tự động**:
- Cảnh có "chạy/trốn" → thêm dust_cloud + motion_blur
- Cảnh có "nhảy/tránh" → thêm ground_crack + debris
- Cảnh có "va chạm/đánh" → thêm impact_flash
- Cảnh có "rừng/cây" → thêm tree_shake

**Output**:
```
Input: "T-Rex chạy trốn trong rừng"
Output: "T-Rex chạy trốn trong rừng [VFX: đám bụi bay dày đặc; motion blur; cây cối rung lắc]"
```

### 3️⃣ Smoke/Fire Effects Node

**Mục đích**: Thêm hiệu ứng khói, lửa, nhiệt

**Effects Library**:
- **dust_impact**: Bụi bay dày từ chân đạp xuống
- **breathing_mist**: Hơi thở tạo sương mù
- **battle_dust**: Khói bụi dày bao trùm chiến đấu
- **fire_sparks**: Tia lửa nhỏ từ va chạm
- **heat_wave**: Sóng nhiệt méo mó không khí
- **impact_explosion**: Vụ nổ nhỏ bụi đất

**Logic tự động**:
- Cảnh có "chân/bước/đạp" → thêm dust_impact
- Cảnh có "gầm/tru/hàm" → thêm breathing_mist
- Cảnh có "va chạm/đụng" → thêm fire_sparks + impact_explosion
- Cảnh có "chiến/đấu" → thêm battle_dust
- Cảnh "cận cảnh" → thêm heat_wave

**Output**:
```
Input: "T-Rex tru lên, mở hàm rộng"
Output: "T-Rex tru lên, mở hàm rộng [SFX: hơi thở tạo sương mù nhẹ]"
```

### 4️⃣ Summarize & Sync Node

**Mục đích**: Phân tích và tóm lược từng cảnh để đảm bảo đồng bộ

**Phân tích**:
- **Characters**: Nhân vật xuất hiện
- **Action Type**: Chase / Combat / Close-up / Wide shot / Transition
- **Camera Angle**: Close-up / Wide angle / Medium shot
- **Mood**: Mysterious / Intense / Fearful / Action
- **Key Elements**: Các yếu tố quan trọng

**Output**: JSON structure với đầy đủ thông tin
```json
{
  "scene_number": 1,
  "original": "...",
  "enhanced": "...",
  "duration": 8,
  "analysis": {
    "characters": ["T-Rex"],
    "action_type": "Chase",
    "camera_angle": "Wide angle",
    "mood": "Intense"
  }
}
```

## 🚀 Cách sử dụng

### Option 1: Sử dụng Python Script (Standalone)

```bash
# Chạy processor trực tiếp
python3 scene_processor.py

# Output: scenes_processed.json
```

### Option 2: Sử dụng n8n Workflow

1. **Import workflow**:
   - Mở n8n
   - Import file `workflow_enhanced_video_generation.json`

2. **Cấu hình**:
   - Kết nối Google Sheets credentials
   - Cấu hình Video Generation API endpoint
   - Set environment variable `VIDEO_GEN_API_URL`

3. **Chạy workflow**:
   - Thêm scenes vào Google Sheets với status = "Ready"
   - Workflow tự động trigger mỗi phút
   - Xử lý qua 4 node enhancement
   - Gửi đến Video Generation API
   - Cập nhật status = "Complete"

### Option 3: Manual Processing

```bash
# 1. Tạo scenes file
cat > my_scenes.json << EOF
{
  "shots": [
    {"scene": "...", "duration": 8}
  ]
}
EOF

# 2. Process scenes
python3 -c "
from scene_processor import SceneProcessor
import json

with open('my_scenes.json') as f:
    data = json.load(f)

processor = SceneProcessor()
result = processor.process_scenes(data)

print(json.dumps(result['processed_shots'], indent=2, ensure_ascii=False))
"
```

## 📊 Ví dụ xử lý đầy đủ

### Input (Original Scene):
```
"T-Rex xuất hiện bước đi uy nghi qua khu rừng, tiếng chân nặng vang vọng."
```

### Output (Enhanced Scene):
```
"T-Rex xuất hiện bước đi uy nghi qua khu rừng, tiếng chân nặng vang vọng.
[răng nanh dài cong, màu trắng ngà bóng]
[VFX: cây cối rung lắc mạnh, lá rụng tung tóe]
[SFX: bụi bay dày đặc từ chân T-Rex đạp xuống đất]"
```

### Analysis:
```json
{
  "characters": ["T-Rex"],
  "action_type": "Transition",
  "camera_angle": "Medium shot",
  "mood": "Action"
}
```

## 🎯 Kết quả cuối cùng

Sau khi qua pipeline, mỗi cảnh sẽ có:

1. ✅ **Character consistency**: Nhân vật đồng bộ qua các cảnh
2. ✅ **VFX effects**: Hiệu ứng visual phù hợp
3. ✅ **Smoke/Fire effects**: Khói lửa tăng tính kịch tính
4. ✅ **Scene analysis**: Phân tích đầy đủ để sync
5. ✅ **Ready for video generation**: Sẵn sàng gửi API

## 🔗 File liên quan

- `scene_processor.py`: Script xử lý chính
- `workflow_enhanced_video_generation.json`: n8n workflow
- `scenes_trex_vs_pteranodon.json`: Scenes gốc (input)
- `scenes_processed.json`: Scenes đã xử lý (output)
- `ready_to_upload.json`: Format cho Google Sheets

## ⚙️ Cấu hình nâng cao

### Custom Character Profiles

Chỉnh sửa trong `scene_processor.py`:
```python
self.character_profiles = {
    "YourCharacter": {
        "description": "...",
        "consistent_details": [
            "chi tiết 1",
            "chi tiết 2"
        ],
        "scale": "kích thước"
    }
}
```

### Custom VFX Effects

Thêm vào VFX library:
```python
self.vfx_library = {
    "your_effect": "mô tả hiệu ứng",
    # ...
}
```

### API Integration

Trong workflow, cấu hình HTTP Request node:
```json
{
  "url": "https://api.your-video-gen.com/v1/generate",
  "method": "POST",
  "body": {
    "prompt": "{{ enhanced_scene }}",
    "duration": "{{ duration }}",
    "quality": "high",
    "model": "sora-2" // hoặc "veo-3"
  }
}
```

## 📈 Performance

- **Processing time**: ~1-2s cho 20 scenes
- **Enhancement coverage**: 100% scenes được xử lý
- **Character consistency**: Rotate details để đa dạng
- **VFX/SFX matching**: Tự động dựa trên keywords

## 🐛 Troubleshooting

**Q: Scenes không được enhance?**
A: Kiểm tra keywords trong scene description, có thể cần thêm logic matching

**Q: Character details không đúng?**
A: Update `character_profiles` trong scene_processor.py

**Q: Workflow không trigger?**
A: Kiểm tra Google Sheets status column phải chính xác là "Ready"

**Q: Video generation API fails?**
A: Kiểm tra API endpoint và credentials, xem logs của HTTP Request node
