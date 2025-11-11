"""
Module để tải video từ URL hoặc xử lý file local
"""

import os
import yt_dlp
from pathlib import Path
from typing import Optional


class VideoDownloader:
    """Download video từ URL hoặc sử dụng file local"""

    def __init__(self, output_dir: str = "./temp"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, output_filename: Optional[str] = None) -> str:
        """
        Download video từ URL

        Args:
            url: URL của video (YouTube, Vimeo, etc.)
            output_filename: Tên file output (optional)

        Returns:
            Đường dẫn đến file video đã download
        """
        if output_filename is None:
            output_filename = "downloaded_video.mp4"

        output_path = self.output_dir / output_filename

        # Cấu hình yt-dlp với nhiều format fallback
        ydl_opts = {
            # Thử nhiều format khác nhau
            'format': (
                'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/'
                'bestvideo+bestaudio/best'
            ),
            'outtmpl': str(output_path.with_suffix('')),  # Không thêm .mp4 ở đây
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
            'merge_output_format': 'mp4',  # Merge thành mp4
            # Thêm options để bypass một số giới hạn
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'no_color': True,
            'extract_flat': False,
        }

        print(f"Đang tải video từ: {url}")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get info trước để check
                info = ydl.extract_info(url, download=False)
                print(f"   Tiêu đề: {info.get('title', 'N/A')}")
                print(f"   Thời lượng: {info.get('duration', 0):.0f}s")

                # Download
                ydl.download([url])

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)

            # Nếu lỗi format, thử cách khác
            if "Requested format is not available" in error_msg or "nsig extraction failed" in error_msg:
                print("\n⚠ Lỗi format, đang thử cách khác...")
                return self._download_fallback(url, output_path)
            else:
                raise Exception(f"Lỗi download: {error_msg}")

        # Tìm file đã download
        # yt-dlp có thể tạo file với tên khác
        downloaded_file = self._find_downloaded_file(output_path)

        if downloaded_file:
            return downloaded_file

        raise FileNotFoundError(f"Không tìm thấy file sau khi download: {output_path}")

    def _download_fallback(self, url: str, output_path: Path) -> str:
        """
        Fallback download với options đơn giản hơn
        """
        print("   Đang thử download với format đơn giản hơn...")

        ydl_opts = {
            'format': 'worst',  # Lấy quality thấp nhất nhưng chắc chắn có
            'outtmpl': str(output_path.with_suffix('')),
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self._progress_hook],
            'merge_output_format': 'mp4',
            'nocheckcertificate': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            downloaded_file = self._find_downloaded_file(output_path)

            if downloaded_file:
                print(f"✓ Download thành công (quality thấp)")
                return downloaded_file

        except Exception as e:
            print(f"⚠ Fallback cũng thất bại: {e}")

        # Fallback cuối cùng: thử format 18 (360p mp4)
        print("   Đang thử format 360p...")

        ydl_opts = {
            'format': '18',  # 360p mp4
            'outtmpl': str(output_path.with_suffix('')),
            'quiet': True,
            'progress_hooks': [self._progress_hook],
            'nocheckcertificate': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            downloaded_file = self._find_downloaded_file(output_path)

            if downloaded_file:
                print(f"✓ Download thành công (360p)")
                return downloaded_file

        except Exception as e:
            raise Exception(
                f"Không thể download video.\n"
                f"Lỗi: {e}\n"
                f"Vui lòng:\n"
                f"1. Update yt-dlp: pip install --upgrade yt-dlp\n"
                f"2. Hoặc download video thủ công rồi dùng --input"
            )

    def _find_downloaded_file(self, output_path: Path) -> Optional[str]:
        """
        Tìm file đã download (yt-dlp có thể đặt tên khác)
        """
        # Thử path gốc với .mp4
        if output_path.with_suffix('.mp4').exists():
            return str(output_path.with_suffix('.mp4'))

        # Thử path gốc
        if output_path.exists():
            return str(output_path)

        # Tìm file với pattern
        base_name = output_path.stem
        for file in self.output_dir.glob(f"{base_name}*"):
            if file.is_file() and file.suffix.lower() in ['.mp4', '.mkv', '.webm', '.avi']:
                return str(file)

        return None

    def _progress_hook(self, d):
        """Hook để hiển thị progress khi download"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f"\rDownloading: {percent} at {speed}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\n✓ Download hoàn tất!")

    def validate_local_file(self, file_path: str) -> str:
        """
        Validate file video local

        Args:
            file_path: Đường dẫn đến file video

        Returns:
            Đường dẫn tuyệt đối của file
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File không tồn tại: {file_path}")

        if not path.is_file():
            raise ValueError(f"Không phải file: {file_path}")

        # Kiểm tra extension
        valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
        if path.suffix.lower() not in valid_extensions:
            print(f"⚠ Cảnh báo: Extension không chuẩn ({path.suffix}), nhưng sẽ thử xử lý...")

        return str(path.absolute())
