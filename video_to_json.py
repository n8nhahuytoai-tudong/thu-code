#!/usr/bin/env python3
"""
Script chuyển đổi video thành JSON
Hỗ trợ extract metadata và frames từ video
"""

import json
import base64
import os
import sys
from typing import Dict, List, Any


def video_to_json_with_opencv(video_path: str, extract_frames: bool = True,
                               frame_interval: int = 30, max_frames: int = 10) -> Dict[str, Any]:
    """
    Chuyển đổi video thành JSON sử dụng OpenCV

    Args:
        video_path: Đường dẫn đến file video
        extract_frames: Có extract frames hay không
        frame_interval: Lấy 1 frame sau mỗi N frames
        max_frames: Số frame tối đa để extract

    Returns:
        Dictionary chứa thông tin video và frames (nếu có)
    """
    try:
        import cv2
    except ImportError:
        print("Error: OpenCV chưa được cài đặt. Chạy: pip install opencv-python")
        sys.exit(1)

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise ValueError(f"Không thể mở video: {video_path}")

    # Lấy metadata
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0

    result = {
        "video_info": {
            "filename": os.path.basename(video_path),
            "filepath": os.path.abspath(video_path),
            "filesize_mb": round(os.path.getsize(video_path) / (1024 * 1024), 2),
            "resolution": {
                "width": width,
                "height": height
            },
            "fps": round(fps, 2),
            "total_frames": frame_count,
            "duration_seconds": round(duration, 2),
            "duration_formatted": f"{int(duration // 60)}:{int(duration % 60):02d}"
        },
        "frames": []
    }

    # Extract frames nếu cần
    if extract_frames:
        frames_to_extract = min(max_frames, frame_count // frame_interval)
        print(f"Đang extract {frames_to_extract} frames...")

        for i in range(frames_to_extract):
            frame_position = i * frame_interval
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
            ret, frame = video.read()

            if ret:
                # Encode frame thành base64
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')

                result["frames"].append({
                    "frame_number": frame_position,
                    "timestamp_seconds": round(frame_position / fps, 2),
                    "image_base64": frame_base64,
                    "image_format": "jpeg"
                })
                print(f"  ✓ Frame {i+1}/{frames_to_extract} (position: {frame_position})")

    video.release()
    return result


def video_to_json_with_ffmpeg(video_path: str) -> Dict[str, Any]:
    """
    Chuyển đổi video thành JSON sử dụng ffprobe (từ ffmpeg)
    Chỉ lấy metadata, không extract frames

    Args:
        video_path: Đường dẫn đến file video

    Returns:
        Dictionary chứa thông tin video
    """
    import subprocess

    try:
        # Chạy ffprobe để lấy thông tin video
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        video_data = json.loads(result.stdout)

        # Extract thông tin quan trọng
        video_stream = next((s for s in video_data.get('streams', [])
                           if s['codec_type'] == 'video'), None)

        if not video_stream:
            raise ValueError("Không tìm thấy video stream")

        format_info = video_data.get('format', {})

        return {
            "video_info": {
                "filename": os.path.basename(video_path),
                "filepath": os.path.abspath(video_path),
                "filesize_mb": round(float(format_info.get('size', 0)) / (1024 * 1024), 2),
                "resolution": {
                    "width": video_stream.get('width'),
                    "height": video_stream.get('height')
                },
                "codec": video_stream.get('codec_name'),
                "fps": eval(video_stream.get('r_frame_rate', '0/1')),
                "duration_seconds": round(float(format_info.get('duration', 0)), 2),
                "bitrate": int(format_info.get('bit_rate', 0)),
                "format": format_info.get('format_name')
            }
        }

    except FileNotFoundError:
        print("Error: ffprobe chưa được cài đặt. Cài đặt ffmpeg để sử dụng.")
        sys.exit(1)
    except Exception as e:
        raise ValueError(f"Lỗi khi xử lý video: {e}")


def main():
    if len(sys.argv) < 2:
        print("Sử dụng: python video_to_json.py <video_path> [options]")
        print("\nOptions:")
        print("  --no-frames          Không extract frames")
        print("  --interval N         Lấy 1 frame sau mỗi N frames (mặc định: 30)")
        print("  --max-frames N       Số frame tối đa (mặc định: 10)")
        print("  --output FILE        File JSON output (mặc định: video_info.json)")
        print("  --method METHOD      Phương pháp: opencv hoặc ffmpeg (mặc định: opencv)")
        print("\nVí dụ:")
        print("  python video_to_json.py video.mp4")
        print("  python video_to_json.py video.mp4 --no-frames --output info.json")
        print("  python video_to_json.py video.mp4 --interval 60 --max-frames 5")
        sys.exit(1)

    video_path = sys.argv[1]

    if not os.path.exists(video_path):
        print(f"Error: File không tồn tại: {video_path}")
        sys.exit(1)

    # Parse arguments
    extract_frames = '--no-frames' not in sys.argv
    frame_interval = 30
    max_frames = 10
    output_file = 'video_info.json'
    method = 'opencv'

    for i, arg in enumerate(sys.argv):
        if arg == '--interval' and i + 1 < len(sys.argv):
            frame_interval = int(sys.argv[i + 1])
        elif arg == '--max-frames' and i + 1 < len(sys.argv):
            max_frames = int(sys.argv[i + 1])
        elif arg == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
        elif arg == '--method' and i + 1 < len(sys.argv):
            method = sys.argv[i + 1].lower()

    print(f"Đang xử lý video: {video_path}")
    print(f"Phương pháp: {method}")

    # Chuyển đổi video thành JSON
    if method == 'ffmpeg':
        result = video_to_json_with_ffmpeg(video_path)
    else:
        result = video_to_json_with_opencv(
            video_path,
            extract_frames=extract_frames,
            frame_interval=frame_interval,
            max_frames=max_frames
        )

    # Lưu vào file JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Đã lưu kết quả vào: {output_file}")
    print(f"  Kích thước file: {os.path.getsize(output_file) / 1024:.2f} KB")

    if extract_frames and 'frames' in result:
        print(f"  Số frames đã extract: {len(result['frames'])}")


if __name__ == '__main__':
    main()
