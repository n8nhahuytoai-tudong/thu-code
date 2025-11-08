#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Video to JSON Converter - Chuyen doi video thanh JSON"""

import json
import base64
import os
import sys

try:
    import cv2
except ImportError:
    print("ERROR: opencv-python chua duoc cai dat!")
    print("Chay lenh: pip install opencv-python")
    input("Nhan Enter de thoat...")
    sys.exit(1)

def video_to_json(video_path, extract_frames=True, frame_interval=30, max_frames=10):
    """Chuyen video thanh JSON"""

    print(f"\nDang xu ly: {video_path}")

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"ERROR: Khong the mo video!")
        return None

    # Lay thong tin video
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

    print(f"\nThong tin video:")
    print(f"  Do phan giai: {width}x{height}")
    print(f"  FPS: {fps:.2f}")
    print(f"  Tong frames: {frame_count}")
    print(f"  Thoi luong: {duration:.2f}s ({result['video_info']['duration_formatted']})")
    print(f"  Kich thuoc: {result['video_info']['filesize_mb']} MB")

    # Extract frames
    if extract_frames and frame_count > 0:
        frames_to_extract = min(max_frames, max(1, frame_count // frame_interval))
        print(f"\nDang extract {frames_to_extract} frames...")

        for i in range(frames_to_extract):
            frame_position = min(i * frame_interval, frame_count - 1)
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
            ret, frame = video.read()

            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')

                result["frames"].append({
                    "frame_number": frame_position,
                    "timestamp_seconds": round(frame_position / fps, 2),
                    "image_base64": frame_base64,
                    "image_format": "jpeg"
                })
                print(f"  [OK] Frame {i+1}/{frames_to_extract} (vi tri: {frame_position})")

    video.release()
    return result


def main():
    print("=" * 60)
    print("       CHUYEN DOI VIDEO THANH JSON")
    print("=" * 60)

    # Lay duong dan video
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        print("\nNhap duong dan video (hoac keo tha file vao day):")
        video_path = input("> ").strip().strip('"')

    if not os.path.exists(video_path):
        print(f"\nERROR: File khong ton tai: {video_path}")
        input("\nNhan Enter de thoat...")
        sys.exit(1)

    # Hoi co extract frames khong
    print("\nBan co muon extract frames khong?")
    print("  1 - Co (file JSON se lon hon, chua hinh anh)")
    print("  2 - Khong (chi lay thong tin video, file nho)")

    choice = input("\nChon (1/2, Enter = 1): ").strip()
    extract_frames = (choice != "2")

    frame_interval = 30
    max_frames = 10

    if extract_frames:
        interval_input = input("\nKhoang cach giua cac frames (Enter = 30): ").strip()
        if interval_input:
            frame_interval = int(interval_input)

        max_input = input("So frames toi da (Enter = 10): ").strip()
        if max_input:
            max_frames = int(max_input)

    # Xu ly video
    result = video_to_json(video_path, extract_frames, frame_interval, max_frames)

    if result is None:
        input("\nNhan Enter de thoat...")
        sys.exit(1)

    # Luu JSON
    video_dir = os.path.dirname(os.path.abspath(video_path))
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_file = os.path.join(video_dir, f"{video_name}_info.json")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print("       HOAN THANH!")
    print(f"{'=' * 60}")
    print(f"\nFile JSON da luu tai:")
    print(f"  {output_file}")
    print(f"\nKich thuoc file: {os.path.getsize(output_file) / 1024:.2f} KB")

    if extract_frames:
        print(f"So frames da extract: {len(result['frames'])}")

    # Mo file
    open_choice = input("\nMo file JSON? (y/n): ").strip().lower()
    if open_choice == 'y':
        os.startfile(output_file)

    # Mo thu muc
    folder_choice = input("Mo thu muc chua file? (y/n): ").strip().lower()
    if folder_choice == 'y':
        os.startfile(video_dir)

    print("\nCam on ban da su dung!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDa huy!")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nNhan Enter de thoat...")
