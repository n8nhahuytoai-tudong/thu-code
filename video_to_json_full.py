#!/usr/bin/env python3
"""
Script để encode TOÀN BỘ video thành JSON
Sẽ extract nhiều frames hơn để cover hết 40s
"""

import cv2
import json
import base64
import os
from pathlib import Path

def video_to_json_full(video_path, output_json='video_full.json', frame_interval=2):
    """
    Convert video to JSON với nhiều frames

    Args:
        video_path: Đường dẫn đến file video
        output_json: Tên file JSON output
        frame_interval: Khoảng cách giữa các frames (giây).
                       Mặc định = 2 giây (20 frames cho video 40s)
    """

    print(f"🎬 Đang đọc video: {video_path}")

    # Mở video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception(f"❌ Không thể mở video: {video_path}")

    # Lấy thông tin video
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)

    print(f"📊 Thông tin video:")
    print(f"   - Độ phân giải: {width}x{height}")
    print(f"   - FPS: {fps}")
    print(f"   - Tổng frames: {total_frames}")
    print(f"   - Thời lượng: {duration:.2f}s")
    print(f"   - Kích thước: {file_size_mb:.2f} MB")
    print()

    # Tính frames cần extract
    frames_to_extract = []
    current_time = 0
    while current_time <= duration:
        frame_num = int(current_time * fps)
        if frame_num < total_frames:
            frames_to_extract.append({
                'frame_number': frame_num,
                'timestamp': current_time
            })
        current_time += frame_interval

    print(f"📸 Sẽ extract {len(frames_to_extract)} frames (mỗi {frame_interval}s)")
    print(f"   Từ 0s đến {duration:.2f}s")
    print()

    # Extract frames
    frames_data = []

    for i, frame_info in enumerate(frames_to_extract):
        frame_num = frame_info['frame_number']
        timestamp = frame_info['timestamp']

        # Seek đến frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()

        if not ret:
            print(f"⚠️  Không đọc được frame {frame_num}")
            continue

        # Encode sang JPEG
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

        # Convert sang base64
        base64_str = base64.b64encode(buffer).decode('utf-8')

        frames_data.append({
            'frame_number': frame_num,
            'timestamp_seconds': round(timestamp, 2),
            'image_base64': base64_str,
            'image_format': 'jpeg'
        })

        print(f"   ✅ Frame {i+1}/{len(frames_to_extract)}: {timestamp:.1f}s (frame #{frame_num})")

    cap.release()

    # Tạo JSON output
    output_data = {
        'video_info': {
            'filename': os.path.basename(video_path),
            'filepath': str(Path(video_path).absolute()),
            'filesize_mb': round(file_size_mb, 2),
            'resolution': {
                'width': width,
                'height': height
            },
            'fps': fps,
            'total_frames': total_frames,
            'duration_seconds': round(duration, 2),
            'duration_formatted': f"{int(duration//60)}:{int(duration%60):02d}",
            'frames_extracted': len(frames_data),
            'frame_interval_seconds': frame_interval
        },
        'frames': frames_data
    }

    # Lưu JSON
    print(f"\n💾 Đang lưu JSON...")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    output_size_mb = os.path.getsize(output_json) / (1024 * 1024)

    print(f"\n✅ HOÀN THÀNH!")
    print(f"   📄 File JSON: {output_json}")
    print(f"   📦 Kích thước: {output_size_mb:.2f} MB")
    print(f"   🖼️  Đã extract: {len(frames_data)} frames")
    print(f"   ⏱️  Coverage: 0s - {duration:.2f}s")


if __name__ == '__main__':
    # Cấu hình
    VIDEO_PATH = '1234.mp4'  # Thay đường dẫn video của bạn
    OUTPUT_JSON = '123_full.json'
    FRAME_INTERVAL = 2  # Mỗi 2 giây lấy 1 frame

    # Nếu muốn nhiều frames hơn, giảm FRAME_INTERVAL:
    # - 2 giây = ~20 frames cho video 40s (file JSON ~15-20MB)
    # - 1 giây = ~40 frames (file JSON ~30-40MB)
    # - 0.5 giây = ~80 frames (file JSON ~60-80MB)

    print("=" * 60)
    print("🎬 VIDEO TO JSON - FULL VERSION")
    print("=" * 60)
    print()

    try:
        video_to_json_full(
            video_path=VIDEO_PATH,
            output_json=OUTPUT_JSON,
            frame_interval=FRAME_INTERVAL
        )
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
