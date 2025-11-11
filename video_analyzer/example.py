#!/usr/bin/env python3
"""
Ví dụ sử dụng Video Analyzer như một library
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules import (
    VideoDownloader,
    SceneDetector,
    FrameExtractor,
    AIAnalyzer,
    ReportGenerator
)


def example_basic():
    """Ví dụ cơ bản: Phát hiện cảnh không dùng AI"""
    print("=" * 60)
    print("VÍ DỤ 1: Phát hiện cảnh cơ bản (không AI)")
    print("=" * 60)

    # Đường dẫn video (thay đổi theo video của bạn)
    video_path = "your_video.mp4"

    # 1. Detect scenes
    detector = SceneDetector(threshold=27.0)
    video_info = detector.get_video_info(video_path)
    scenes = detector.detect_scenes(video_path)

    print(f"\nVideo: {video_info['filename']}")
    print(f"Tìm thấy {len(scenes)} cảnh")

    # 2. Extract frames
    extractor = FrameExtractor()
    scenes_with_frames = extractor.extract_scene_frames(
        video_path,
        scenes,
        extract_first=True,
        extract_last=True
    )

    # 3. Generate report
    generator = ReportGenerator()
    reports = generator.generate_report(
        video_info,
        scenes_with_frames,
        formats=["json", "html"]
    )

    print("\n✓ Hoàn thành!")
    print("Báo cáo:", reports)


def example_with_ai():
    """Ví dụ nâng cao: Phân tích với AI"""
    print("=" * 60)
    print("VÍ DỤ 2: Phân tích video với AI")
    print("=" * 60)

    video_path = "your_video.mp4"

    # Setup
    detector = SceneDetector(threshold=27.0, min_scene_len=15)
    extractor = FrameExtractor()
    analyzer = AIAnalyzer()  # Cần ANTHROPIC_API_KEY trong .env
    generator = ReportGenerator()

    # Pipeline
    print("\n1. Phát hiện cảnh...")
    video_info = detector.get_video_info(video_path)
    scenes = detector.detect_scenes(video_path)

    print("\n2. Extract frames...")
    scenes_with_frames = extractor.extract_scene_frames(
        video_path,
        scenes,
        extract_first=True,
        extract_middle=True,
        extract_last=True
    )

    print("\n3. Phân tích AI (có thể mất vài phút)...")
    analyzed_scenes = analyzer.analyze_all_scenes(
        scenes_with_frames,
        language="vi",
        detail_level="detailed",
        delay=0.5
    )

    # In kết quả
    print("\n" + "=" * 60)
    print("KẾT QUẢ PHÂN TÍCH")
    print("=" * 60)
    for scene in analyzed_scenes[:3]:  # Hiển thị 3 cảnh đầu
        print(f"\nCảnh {scene['scene_number']}:")
        print(f"  Thời gian: {scene['start_time']:.1f}s - {scene['end_time']:.1f}s")
        print(f"  Mô tả: {scene.get('description', 'N/A')[:200]}...")

    print("\n4. Tạo báo cáo...")
    reports = generator.generate_report(
        video_info,
        analyzed_scenes,
        formats=["json", "html", "markdown"]
    )

    print("\n✓ Hoàn thành!")
    for fmt, path in reports.items():
        print(f"  {fmt}: {path}")


def example_custom_analysis():
    """Ví dụ: Phân tích tùy chỉnh với prompt riêng"""
    print("=" * 60)
    print("VÍ DỤ 3: Phân tích tùy chỉnh")
    print("=" * 60)

    # Giả sử bạn đã có frames
    frames = [
        "output/frames/video/scene_001_first.jpg",
        "output/frames/video/scene_001_last.jpg"
    ]

    analyzer = AIAnalyzer()

    custom_prompt = """
    Phân tích chi tiết cảnh này theo các góc độ:
    1. Cảm xúc chủ đạo
    2. Màu sắc và ánh sáng
    3. Composition và góc quay
    4. Yếu tố kỹ thuật điện ảnh

    Trả lời bằng tiếng Việt, chi tiết và chuyên nghiệp.
    """

    try:
        result = analyzer.analyze_with_custom_prompt(frames, custom_prompt)
        print("\nKết quả phân tích:")
        print(result)
    except Exception as e:
        print(f"Lỗi: {e}")


def example_download_from_url():
    """Ví dụ: Download video từ URL và phân tích"""
    print("=" * 60)
    print("VÍ DỤ 4: Download và phân tích video từ URL")
    print("=" * 60)

    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Thay bằng URL thực

    # Download
    downloader = VideoDownloader(output_dir="./temp")
    try:
        print(f"\nDownloading: {url}")
        video_path = downloader.download(url)
        print(f"✓ Đã download: {video_path}")

        # Phân tích như bình thường
        detector = SceneDetector()
        scenes = detector.detect_scenes(video_path)
        print(f"✓ Tìm thấy {len(scenes)} cảnh")

    except Exception as e:
        print(f"Lỗi: {e}")


def main():
    """Main function"""
    print("\n🎬 VIDEO ANALYZER - EXAMPLES\n")
    print("Chọn ví dụ để chạy:")
    print("  1. Phát hiện cảnh cơ bản (không AI)")
    print("  2. Phân tích với AI (cần API key)")
    print("  3. Phân tích tùy chỉnh")
    print("  4. Download từ URL")
    print("  0. Thoát")

    try:
        choice = input("\nNhập lựa chọn (0-4): ").strip()

        if choice == "1":
            example_basic()
        elif choice == "2":
            example_with_ai()
        elif choice == "3":
            example_custom_analysis()
        elif choice == "4":
            example_download_from_url()
        elif choice == "0":
            print("Tạm biệt!")
        else:
            print("Lựa chọn không hợp lệ!")

    except KeyboardInterrupt:
        print("\n\nĐã hủy!")
    except Exception as e:
        print(f"\nLỗi: {e}")


if __name__ == "__main__":
    main()
