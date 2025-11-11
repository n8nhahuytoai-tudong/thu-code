#!/usr/bin/env python3
"""
Video Analyzer - Tool phân tích video tự động
Phát hiện cảnh, mô tả nội dung, và tạo báo cáo chi tiết

Sử dụng:
    python video_analyzer.py --input video.mp4
    python video_analyzer.py --url https://youtube.com/watch?v=xxx
    python video_analyzer.py --input video.mp4 --no-ai (không dùng AI)
"""

import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules import (
    VideoDownloader,
    SceneDetector,
    FrameExtractor,
    AIAnalyzer,
    ReportGenerator
)


class VideoAnalyzer:
    """Main Video Analyzer class"""

    def __init__(
        self,
        threshold: float = 27.0,
        min_scene_len: int = 15,
        use_ai: bool = True,
        detail_level: str = "detailed",
        language: str = "vi"
    ):
        """
        Khởi tạo Video Analyzer

        Args:
            threshold: Ngưỡng phát hiện cảnh
            min_scene_len: Độ dài tối thiểu của cảnh (frames)
            use_ai: Sử dụng AI để phân tích nội dung
            detail_level: Mức độ chi tiết ("brief", "detailed", "very_detailed")
            language: Ngôn ngữ mô tả ("vi", "en")
        """
        self.downloader = VideoDownloader(output_dir="./video_analyzer/temp")
        self.scene_detector = SceneDetector(threshold=threshold, min_scene_len=min_scene_len)
        self.frame_extractor = FrameExtractor(output_dir="./video_analyzer/output/frames")
        self.report_generator = ReportGenerator(output_dir="./video_analyzer/output/reports")

        self.use_ai = use_ai
        self.detail_level = detail_level
        self.language = language

        if use_ai:
            try:
                self.ai_analyzer = AIAnalyzer()
            except Exception as e:
                print(f"⚠️  Không thể khởi tạo AI Analyzer: {e}")
                print("   → Chạy ở chế độ không có AI")
                self.use_ai = False

    def analyze_video(
        self,
        video_path: str = None,
        video_url: str = None,
        output_formats: list = None
    ) -> dict:
        """
        Phân tích video hoàn chỉnh

        Args:
            video_path: Đường dẫn file video local
            video_url: URL video để download
            output_formats: List format output ["json", "html", "markdown"]

        Returns:
            Dict chứa đường dẫn các file báo cáo
        """
        if output_formats is None:
            output_formats = ["json", "html", "markdown"]

        print("=" * 70)
        print("🎬 VIDEO ANALYZER - Công cụ phân tích video tự động")
        print("=" * 70)

        # Step 1: Lấy video
        if video_url:
            print("\n[1/6] Đang tải video từ URL...")
            try:
                video_path = self.downloader.download(video_url)
            except Exception as e:
                print(f"❌ Lỗi khi tải video: {e}")
                return None

        elif video_path:
            print("\n[1/6] Kiểm tra file video local...")
            try:
                video_path = self.downloader.validate_local_file(video_path)
                print(f"✓ File hợp lệ: {video_path}")
            except Exception as e:
                print(f"❌ Lỗi: {e}")
                return None
        else:
            print("❌ Cần cung cấp --input hoặc --url")
            return None

        # Step 2: Lấy thông tin video
        print("\n[2/6] Đang phân tích thông tin video...")
        try:
            video_info = self.scene_detector.get_video_info(video_path)
            print(f"   📹 Video: {video_info['filename']}")
            print(f"   📐 Độ phân giải: {video_info['width']}x{video_info['height']}")
            print(f"   ⏱️  Thời lượng: {self._format_duration(video_info['duration'])}")
            print(f"   🎞️  FPS: {video_info['fps']:.2f}")
        except Exception as e:
            print(f"❌ Lỗi khi đọc video info: {e}")
            return None

        # Step 3: Phát hiện cảnh
        print("\n[3/6] Đang phát hiện các cảnh trong video...")
        try:
            scenes = self.scene_detector.detect_scenes(video_path, method="content")

            if not scenes:
                print("⚠️  Không phát hiện được cảnh nào!")
                return None

            print(f"   ✓ Phát hiện {len(scenes)} cảnh")

            # Hiển thị danh sách scenes
            for scene in scenes[:5]:  # Hiển thị 5 cảnh đầu
                start = self._format_duration(scene['start_time'])
                end = self._format_duration(scene['end_time'])
                print(f"      • Cảnh {scene['scene_number']}: {start} - {end} ({scene['duration']:.1f}s)")

            if len(scenes) > 5:
                print(f"      ... và {len(scenes) - 5} cảnh khác")

        except Exception as e:
            print(f"❌ Lỗi khi phát hiện cảnh: {e}")
            return None

        # Step 4: Extract frames
        print("\n[4/6] Đang extract frames từ các cảnh...")
        try:
            scenes_with_frames = self.frame_extractor.extract_scene_frames(
                video_path,
                scenes,
                extract_first=True,
                extract_last=True,
                extract_middle=True
            )
        except Exception as e:
            print(f"❌ Lỗi khi extract frames: {e}")
            return None

        # Step 5: Phân tích bằng AI (nếu được bật)
        if self.use_ai and hasattr(self, 'ai_analyzer'):
            print(f"\n[5/6] Đang phân tích nội dung cảnh bằng AI (mức độ: {self.detail_level})...")
            try:
                analyzed_scenes = self.ai_analyzer.analyze_all_scenes(
                    scenes_with_frames,
                    language=self.language,
                    detail_level=self.detail_level,
                    delay=0.5
                )
            except Exception as e:
                print(f"⚠️  Lỗi khi phân tích AI: {e}")
                print("   → Tiếp tục mà không có mô tả AI")
                analyzed_scenes = scenes_with_frames
        else:
            print("\n[5/6] Bỏ qua phân tích AI (chế độ không AI)")
            analyzed_scenes = scenes_with_frames

        # Step 6: Tạo báo cáo
        print(f"\n[6/6] Đang tạo báo cáo ({', '.join(output_formats)})...")
        try:
            report_files = self.report_generator.generate_report(
                video_info,
                analyzed_scenes,
                formats=output_formats
            )
        except Exception as e:
            print(f"❌ Lỗi khi tạo báo cáo: {e}")
            return None

        # Hoàn thành
        print("\n" + "=" * 70)
        print("✅ HOÀN TẤT PHÂN TÍCH!")
        print("=" * 70)
        print("\n📄 Báo cáo đã được tạo:")
        for format_name, file_path in report_files.items():
            print(f"   • {format_name.upper()}: {file_path}")

        return report_files

    def _format_duration(self, seconds: float) -> str:
        """Format thời gian"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


def main():
    """Main function"""
    # Load environment variables
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Video Analyzer - Phân tích video tự động",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python video_analyzer.py --input my_video.mp4
  python video_analyzer.py --url https://youtube.com/watch?v=xxx
  python video_analyzer.py --input video.mp4 --detail-level very_detailed
  python video_analyzer.py --input video.mp4 --no-ai --threshold 20
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--input', '-i',
        type=str,
        help='Đường dẫn đến file video local'
    )
    input_group.add_argument(
        '--url', '-u',
        type=str,
        help='URL video (YouTube, Vimeo, etc.)'
    )

    # Scene detection options
    parser.add_argument(
        '--threshold', '-t',
        type=float,
        default=27.0,
        help='Ngưỡng phát hiện cảnh (mặc định: 27.0, càng thấp càng nhạy)'
    )
    parser.add_argument(
        '--min-scene-len',
        type=int,
        default=15,
        help='Độ dài tối thiểu của cảnh (frames, mặc định: 15)'
    )

    # AI options
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Không sử dụng AI để phân tích nội dung'
    )
    parser.add_argument(
        '--detail-level',
        choices=['brief', 'detailed', 'very_detailed'],
        default='detailed',
        help='Mức độ chi tiết mô tả (mặc định: detailed)'
    )
    parser.add_argument(
        '--language', '-l',
        choices=['vi', 'en'],
        default='vi',
        help='Ngôn ngữ mô tả (mặc định: vi)'
    )

    # Output options
    parser.add_argument(
        '--formats', '-f',
        nargs='+',
        choices=['json', 'html', 'markdown'],
        default=['json', 'html', 'markdown'],
        help='Format báo cáo (mặc định: tất cả)'
    )

    args = parser.parse_args()

    # Kiểm tra API key nếu dùng AI
    if not args.no_ai:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("⚠️  Không tìm thấy ANTHROPIC_API_KEY")
            print("   Để sử dụng AI analysis, vui lòng:")
            print("   1. Tạo file .env trong thư mục video_analyzer/")
            print("   2. Thêm dòng: ANTHROPIC_API_KEY=your_api_key_here")
            print("   hoặc chạy với --no-ai để bỏ qua phân tích AI\n")

            use_ai = input("Tiếp tục không có AI? (y/n): ").lower() == 'y'
            if not use_ai:
                sys.exit(1)
            args.no_ai = True

    # Khởi tạo analyzer
    analyzer = VideoAnalyzer(
        threshold=args.threshold,
        min_scene_len=args.min_scene_len,
        use_ai=not args.no_ai,
        detail_level=args.detail_level,
        language=args.language
    )

    # Phân tích video
    result = analyzer.analyze_video(
        video_path=args.input,
        video_url=args.url,
        output_formats=args.formats
    )

    if result:
        print("\n✨ Chúc bạn sử dụng tool hiệu quả!")
        sys.exit(0)
    else:
        print("\n❌ Phân tích thất bại!")
        sys.exit(1)


if __name__ == "__main__":
    main()
