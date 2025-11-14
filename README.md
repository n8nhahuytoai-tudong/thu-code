# Character Replacement Tool
## Công cụ thay thế nhân vật trong video

Ứng dụng Python cho phép tự động phát hiện và thay thế nhân vật trong video bằng nhiều phương pháp khác nhau.

---

## ✨ Tính năng

### 🎯 Phát hiện nhân vật
- Phát hiện khuôn mặt (Face Detection)
- Phát hiện toàn thân (Full Body Detection)
- Theo dõi nhân vật qua các frame
- Xuất thông tin nhân vật ra JSON

### 🔄 Phương pháp thay thế

1. **Blur** - Làm mờ vùng nhân vật
2. **Pixelate** - Tạo hiệu ứng khảm/mosaic
3. **Color** - Tô màu đen hoặc màu tùy chọn
4. **Image** - Thay thế bằng ảnh khác

### 🎨 Giao diện

- **CLI** - Command Line Interface cho automation
- **GUI** - Giao diện đồ họa PyQt5 thân thiện

---

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- OpenCV 4.x
- PyQt5 (cho GUI)
- Hệ điều hành: Windows, Linux, macOS

---

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd thu-code
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cài đặt nâng cao (Optional)

Để sử dụng các tính năng AI nâng cao, uncomment các dòng trong `requirements.txt`:

```bash
# Cho face recognition và swapping chất lượng cao
pip install mediapipe torch torchvision ultralytics insightface
```

---

## 💻 Sử dụng

### Giao diện đồ họa (GUI)

Khởi chạy ứng dụng GUI:

```bash
python character_replacement_gui.py
```

**Hướng dẫn sử dụng GUI:**

1. Click **"Chọn video"** để chọn video đầu vào
2. Chọn **phương pháp thay thế** (blur, pixelate, color, image)
3. Nếu chọn method "image", click **"Chọn ảnh"** để chọn ảnh thay thế
4. Chọn **loại nhân vật** cần thay thế (tất cả, chỉ mặt, chỉ toàn thân)
5. Điều chỉnh **Frame skip** để tăng tốc (bỏ qua 1 số frame)
6. Chọn vị trí lưu file output
7. Click **"Bắt đầu xử lý"**

### Command Line Interface (CLI)

#### 1. Thay thế nhân vật bằng blur

```bash
python character_replacement.py input.mp4 -o output.mp4 -m blur
```

#### 2. Thay thế bằng pixelate/mosaic

```bash
python character_replacement.py input.mp4 -o output.mp4 -m pixelate
```

#### 3. Thay thế bằng ảnh khác

```bash
python character_replacement.py input.mp4 -o output.mp4 -m image -i replacement.png
```

#### 4. Chỉ thay thế khuôn mặt

```bash
python character_replacement.py input.mp4 -o output.mp4 -m blur -f face
```

#### 5. Hiển thị bounding boxes

```bash
python character_replacement.py input.mp4 -o output.mp4 -m blur -b
```

#### 6. Tăng tốc xử lý (skip frames)

```bash
python character_replacement.py input.mp4 -o output.mp4 -m blur -s 2
```

#### 7. Trích xuất thông tin nhân vật

```bash
python character_replacement.py input.mp4 -o info.json -m info
```

---

## 📖 Chi tiết tham số CLI

```
usage: character_replacement.py [-h] [-o OUTPUT] [-m {blur,pixelate,color,image,info}]
                                [-i IMAGE] [-f {face,body}] [-b] [-s SKIP]
                                input

Thay thế nhân vật trong video

positional arguments:
  input                 Đường dẫn video đầu vào

optional arguments:
  -h, --help            Hiển thị help message
  -o, --output OUTPUT   Đường dẫn video đầu ra (default: output.mp4)
  -m, --method {blur,pixelate,color,image,info}
                        Phương pháp thay thế (default: blur)
  -i, --image IMAGE     Đường dẫn ảnh thay thế (cho method=image)
  -f, --filter {face,body}
                        Lọc loại nhân vật
  -b, --bbox            Hiển thị bounding boxes
  -s, --skip SKIP       Bỏ qua n frames để tăng tốc (default: 0)
```

---

## 🎯 Ví dụ sử dụng

### Ví dụ 1: Blur tất cả nhân vật

```bash
python character_replacement.py demo.mp4 -o demo_blur.mp4 -m blur
```

### Ví dụ 2: Mosaic chỉ khuôn mặt

```bash
python character_replacement.py demo.mp4 -o demo_face_mosaic.mp4 -m pixelate -f face
```

### Ví dụ 3: Thay thế bằng ảnh avatar

```bash
python character_replacement.py demo.mp4 -o demo_replaced.mp4 -m image -i avatar.png
```

### Ví dụ 4: Xử lý nhanh với frame skip

```bash
python character_replacement.py long_video.mp4 -o output.mp4 -m blur -s 3
```

### Ví dụ 5: Debug với bounding boxes

```bash
python character_replacement.py demo.mp4 -o demo_debug.mp4 -m blur -b
```

---

## 📁 Cấu trúc dự án

```
thu-code/
├── character_replacement.py           # Module chính - CLI
├── character_replacement_gui.py       # Giao diện GUI
├── requirements.txt                   # Dependencies
├── README.md                          # Tài liệu này
├── workflow_state_manager.pyd         # State manager (legacy)
└── examples/                          # (Tạo thêm nếu cần)
    ├── demo_input.mp4
    └── demo_output.mp4
```

---

## 🔧 API Reference

### Class: `CharacterReplacer`

#### Constructor

```python
replacer = CharacterReplacer(video_path: str)
```

#### Methods

##### 1. `get_video_info() -> dict`

Lấy thông tin video

**Returns:**
```python
{
    "filename": str,
    "path": str,
    "resolution": str,  # "1920x1080"
    "fps": float,
    "total_frames": int,
    "duration_seconds": float
}
```

##### 2. `detect_characters(frame: np.ndarray) -> List[dict]`

Phát hiện nhân vật trong 1 frame

**Returns:**
```python
[
    {
        "type": "face" | "body",
        "id": int,
        "bbox": {"x": int, "y": int, "w": int, "h": int},
        "center": {"x": int, "y": int}
    }
]
```

##### 3. `replace_character_blur(frame, character, blur_strength=51) -> np.ndarray`

Thay thế bằng blur

##### 4. `replace_character_pixelate(frame, character, pixel_size=20) -> np.ndarray`

Thay thế bằng pixelate

##### 5. `replace_character_color(frame, character, color=(0,0,0)) -> np.ndarray`

Thay thế bằng màu

##### 6. `replace_character_image(frame, character, replacement_image_path) -> np.ndarray`

Thay thế bằng ảnh

##### 7. `process_video(...) -> dict`

Xử lý toàn bộ video

**Parameters:**
- `output_path: str` - Đường dẫn output
- `replacement_method: str` - "blur" | "pixelate" | "color" | "image"
- `replacement_image: Optional[str]` - Path ảnh thay thế
- `character_filter: Optional[str]` - "face" | "body" | None
- `show_bboxes: bool` - Hiển thị boxes
- `frame_skip: int` - Bỏ qua frames

**Returns:**
```python
{
    "start_time": str,
    "end_time": str,
    "input_video": str,
    "output_video": str,
    "method": str,
    "frames_processed": int,
    "characters_replaced": int,
    "processing_errors": int
}
```

##### 8. `extract_characters_info(output_json, frame_step=30) -> dict`

Trích xuất timeline nhân vật

---

## 🎓 Ví dụ Code

### Ví dụ Python Script

```python
from character_replacement import CharacterReplacer

# Khởi tạo
replacer = CharacterReplacer("input.mp4")

# Lấy info
info = replacer.get_video_info()
print(f"Video: {info['resolution']}, {info['duration_seconds']:.1f}s")

# Xử lý video
stats = replacer.process_video(
    output_path="output.mp4",
    replacement_method="blur",
    character_filter="face",
    show_bboxes=True
)

print(f"Processed {stats['frames_processed']} frames")
print(f"Replaced {stats['characters_replaced']} characters")
```

### Ví dụ xử lý custom

```python
import cv2
from character_replacement import CharacterReplacer

replacer = CharacterReplacer("input.mp4")

# Đọc 1 frame
ret, frame = replacer.cap.read()

# Phát hiện nhân vật
characters = replacer.detect_characters(frame)
print(f"Found {len(characters)} characters")

# Thay thế từng nhân vật
for char in characters:
    if char["type"] == "face":
        frame = replacer.replace_character_pixelate(frame, char)
    else:
        frame = replacer.replace_character_blur(frame, char)

# Lưu frame
cv2.imwrite("output_frame.jpg", frame)
```

---

## 🔬 Kỹ thuật sử dụng

### 1. Face Detection

Sử dụng **Haar Cascade Classifier** từ OpenCV:
- Model: `haarcascade_frontalface_default.xml`
- Phát hiện khuôn mặt nhìn thẳng
- Tốc độ: Nhanh (~60 FPS trên CPU)
- Độ chính xác: Trung bình-Cao

### 2. Body Detection

Sử dụng **Haar Cascade** cho full body:
- Model: `haarcascade_fullbody.xml`
- Phát hiện toàn thân người
- Tốc độ: Nhanh
- Độ chính xác: Trung bình

### 3. Nâng cấp với Deep Learning (Optional)

Để độ chính xác cao hơn, có thể sử dụng:
- **YOLOv8** - Object detection
- **MediaPipe** - Face mesh, pose estimation
- **InsightFace** - Face recognition, swapping
- **Detectron2** - Instance segmentation

---

## ⚡ Tối ưu hiệu năng

### Tips để xử lý nhanh hơn:

1. **Frame Skip**: Sử dụng `-s` để bỏ qua frames
   ```bash
   python character_replacement.py video.mp4 -o out.mp4 -s 2
   ```

2. **Giảm resolution**: Resize video trước khi xử lý
   ```bash
   ffmpeg -i input.mp4 -vf scale=640:360 input_small.mp4
   ```

3. **GPU Acceleration**: Cài OpenCV với CUDA support
   ```bash
   pip install opencv-contrib-python-headless
   ```

4. **Multiprocessing**: Xử lý nhiều video cùng lúc

---

## 🐛 Troubleshooting

### Lỗi: "Không thể mở video"

**Nguyên nhân:** Codec không được hỗ trợ

**Giải pháp:** Chuyển đổi sang MP4 H.264
```bash
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
```

### Lỗi: "Cascade classifier không load được"

**Nguyên nhân:** OpenCV chưa cài đầy đủ

**Giải pháp:**
```bash
pip uninstall opencv-python
pip install opencv-python==4.10.0.84
```

### Hiệu năng chậm

**Giải pháp:**
- Sử dụng frame skip: `-s 2` hoặc `-s 3`
- Giảm resolution video
- Xử lý trên máy có GPU

### Phát hiện không chính xác

**Giải pháp:**
- Điều chỉnh parameters trong `detect_characters()`
- Sử dụng deep learning models (YOLOv8, MediaPipe)
- Kiểm tra lighting và chất lượng video

---

## 🛣️ Roadmap

### Version 1.1 (Planned)
- [ ] Thêm YOLOv8 detection
- [ ] Face tracking qua frames
- [ ] Batch processing nhiều videos
- [ ] Export timeline dạng Excel

### Version 1.2 (Future)
- [ ] Real-time video processing
- [ ] Face swapping với deep learning
- [ ] Background removal
- [ ] Integration với FFmpeg

### Version 2.0 (Future)
- [ ] Web interface
- [ ] Cloud processing
- [ ] API endpoints
- [ ] Mobile app

---

## 📝 License

MIT License - Xem file LICENSE để biết thêm chi tiết

---

## 👥 Đóng góp

Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Liên hệ

Nếu có câu hỏi hoặc đề xuất, vui lòng:
- Tạo Issue trên GitHub
- Email: [your-email@example.com]

---

## 🙏 Credits

- OpenCV Team - Computer Vision library
- PyQt Team - GUI framework
- Haar Cascade Models - Face/Body detection

---

## 📚 Tài liệu tham khảo

- [OpenCV Documentation](https://docs.opencv.org/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Face Detection with OpenCV](https://docs.opencv.org/master/db/d28/tutorial_cascade_classifier.html)

---

**Version:** 1.0.0
**Last Updated:** 2025-11-14
**Language:** Python 3.8+
