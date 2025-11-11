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

        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': str(output_path),
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }

        print(f"Đang tải video từ: {url}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # yt-dlp có thể thêm extension, tìm file thực tế
        if output_path.exists():
            return str(output_path)

        # Tìm file với pattern
        for file in self.output_dir.glob(f"{output_path.stem}*"):
            if file.is_file():
                return str(file)

        raise FileNotFoundError(f"Không tìm thấy file sau khi download: {output_path}")

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
