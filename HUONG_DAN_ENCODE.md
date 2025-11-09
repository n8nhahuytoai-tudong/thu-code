# 🎬 HƯỚNG DẪN ENCODE TOÀN BỘ VIDEO

## 📋 Yêu cầu

- Python 3.6+
- opencv-python (tự động cài đặt)
- File video gốc `1234.mp4`

## 🚀 Cách sử dụng (Windows)

### Cách 1: Chạy file .bat (Đơn giản nhất)

1. Copy file video `1234.mp4` vào thư mục này
2. Double click `run_encode_full.bat`
3. Đợi script chạy xong
4. File `123_full.json` sẽ được tạo ra

### Cách 2: Chạy Python trực tiếp

```bash
# Cài opencv
pip install opencv-python

# Chạy script
python video_to_json_full.py
```

## ⚙️ Tùy chỉnh

Mở file `video_to_json_full.py` và sửa các thông số:

```python
VIDEO_PATH = '1234.mp4'          # Đường dẫn video
OUTPUT_JSON = '123_full.json'    # Tên file output
FRAME_INTERVAL = 2               # Mỗi bao nhiêu giây lấy 1 frame
```

### Gợi ý FRAME_INTERVAL:

| Interval | Số frames (40s video) | Kích thước JSON | Mục đích |
|----------|----------------------|-----------------|-----------|
| 4 giây | ~10 frames | ~5 MB | Xem nhanh |
| 2 giây | ~20 frames | ~15-20 MB | **Khuyến nghị** |
| 1 giây | ~40 frames | ~30-40 MB | Chi tiết cao |
| 0.5 giây | ~80 frames | ~60-80 MB | Rất chi tiết |

## 📤 Sau khi encode xong

1. File `123_full.json` sẽ chứa TOÀN BỘ video (0-40s)
2. Upload file này lên GitHub hoặc share cho tôi
3. Tôi sẽ xem đầy đủ và viết prompts chính xác hơn!

## ⚠️ Lưu ý

- File JSON sẽ rất lớn (15-20 MB với interval 2s)
- Có thể mất 1-2 phút để encode
- Đảm bảo đủ dung lượng ổ đĩa

## 🐛 Troubleshooting

**Lỗi: "Không tìm thấy video"**
→ Đảm bảo file `1234.mp4` ở cùng thư mục với script

**Lỗi: "No module named cv2"**
→ Chạy: `pip install opencv-python`

**File JSON quá lớn**
→ Tăng FRAME_INTERVAL lên 3 hoặc 4 giây

## 📧 Hỗ trợ

Nếu gặp lỗi, chụp màn hình error và gửi cho tôi!
