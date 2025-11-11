"""
Module để extract frames từ video
"""

import cv2
import os
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm


class FrameExtractor:
    """Extract frames từ video cho mỗi scene"""

    def __init__(self, output_dir: str = "./output/frames"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_scene_frames(
        self,
        video_path: str,
        scenes: List[Dict],
        extract_first: bool = True,
        extract_last: bool = True,
        extract_middle: bool = False
    ) -> List[Dict]:
        """
        Extract frames cho mỗi scene

        Args:
            video_path: Đường dẫn video
            scenes: List các scene từ SceneDetector
            extract_first: Extract frame đầu tiên
            extract_last: Extract frame cuối cùng
            extract_middle: Extract frame giữa

        Returns:
            List scenes với thông tin về frames đã extract
        """
        print(f"\n📸 Đang extract frames từ {len(scenes)} cảnh...")

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Không thể mở video: {video_path}")

        video_name = Path(video_path).stem

        # Create output directory cho video này
        video_output_dir = self.output_dir / video_name
        video_output_dir.mkdir(parents=True, exist_ok=True)

        results = []

        for scene in tqdm(scenes, desc="Extracting frames"):
            scene_num = scene['scene_number']
            start_frame = scene['start_frame']
            end_frame = scene['end_frame']

            scene_data = scene.copy()
            scene_data['frames'] = {}

            # Extract first frame
            if extract_first:
                first_frame_path = self._extract_frame(
                    cap, start_frame, video_output_dir,
                    f"scene_{scene_num:03d}_first.jpg"
                )
                scene_data['frames']['first'] = first_frame_path

            # Extract middle frame
            if extract_middle:
                middle_frame = (start_frame + end_frame) // 2
                middle_frame_path = self._extract_frame(
                    cap, middle_frame, video_output_dir,
                    f"scene_{scene_num:03d}_middle.jpg"
                )
                scene_data['frames']['middle'] = middle_frame_path

            # Extract last frame
            if extract_last:
                # Lấy frame trước frame cuối một chút để tránh transition
                last_frame = max(start_frame, end_frame - 1)
                last_frame_path = self._extract_frame(
                    cap, last_frame, video_output_dir,
                    f"scene_{scene_num:03d}_last.jpg"
                )
                scene_data['frames']['last'] = last_frame_path

            results.append(scene_data)

        cap.release()
        print(f"✓ Đã extract frames vào thư mục: {video_output_dir}")

        return results

    def _extract_frame(
        self,
        cap: cv2.VideoCapture,
        frame_number: int,
        output_dir: Path,
        filename: str
    ) -> str:
        """
        Extract một frame cụ thể từ video

        Args:
            cap: VideoCapture object
            frame_number: Số thứ tự frame cần extract
            output_dir: Thư mục output
            filename: Tên file output

        Returns:
            Đường dẫn đến file ảnh đã lưu
        """
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if not ret:
            raise ValueError(f"Không thể đọc frame {frame_number}")

        output_path = output_dir / filename
        cv2.imwrite(str(output_path), frame)

        return str(output_path)

    def extract_frames_at_interval(
        self,
        video_path: str,
        interval_seconds: float = 1.0,
        max_frames: Optional[int] = None
    ) -> List[str]:
        """
        Extract frames theo khoảng thời gian nhất định
        (Hữu ích cho video dài)

        Args:
            video_path: Đường dẫn video
            interval_seconds: Khoảng thời gian giữa các frame (giây)
            max_frames: Số lượng frame tối đa cần extract

        Returns:
            List đường dẫn đến các frame đã extract
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Không thể mở video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_interval = int(interval_seconds * fps)

        video_name = Path(video_path).stem
        video_output_dir = self.output_dir / video_name / "interval"
        video_output_dir.mkdir(parents=True, exist_ok=True)

        frame_paths = []
        frame_count = 0

        print(f"\n📸 Extracting frames every {interval_seconds}s...")

        for frame_num in tqdm(range(0, total_frames, frame_interval)):
            if max_frames and frame_count >= max_frames:
                break

            try:
                frame_path = self._extract_frame(
                    cap, frame_num, video_output_dir,
                    f"frame_{frame_count:05d}.jpg"
                )
                frame_paths.append(frame_path)
                frame_count += 1
            except Exception as e:
                print(f"⚠ Lỗi khi extract frame {frame_num}: {e}")
                continue

        cap.release()
        print(f"✓ Đã extract {len(frame_paths)} frames")

        return frame_paths

    def create_thumbnail_grid(
        self,
        image_paths: List[str],
        output_path: str,
        grid_cols: int = 4,
        thumbnail_size: tuple = (320, 180)
    ):
        """
        Tạo lưới ảnh thumbnail từ nhiều ảnh
        (Để preview nhanh tất cả scenes)

        Args:
            image_paths: List đường dẫn ảnh
            output_path: Đường dẫn file output
            grid_cols: Số cột trong lưới
            thumbnail_size: Kích thước mỗi thumbnail (width, height)
        """
        import numpy as np

        if not image_paths:
            print("⚠ Không có ảnh để tạo thumbnail grid")
            return

        # Tính số hàng
        grid_rows = (len(image_paths) + grid_cols - 1) // grid_cols

        # Tạo canvas trống
        canvas_width = thumbnail_size[0] * grid_cols
        canvas_height = thumbnail_size[1] * grid_rows
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

        for idx, img_path in enumerate(image_paths):
            img = cv2.imread(img_path)
            if img is None:
                continue

            # Resize
            img_resized = cv2.resize(img, thumbnail_size)

            # Tính vị trí
            row = idx // grid_cols
            col = idx % grid_cols

            y_start = row * thumbnail_size[1]
            y_end = y_start + thumbnail_size[1]
            x_start = col * thumbnail_size[0]
            x_end = x_start + thumbnail_size[0]

            canvas[y_start:y_end, x_start:x_end] = img_resized

        cv2.imwrite(output_path, canvas)
        print(f"✓ Đã tạo thumbnail grid: {output_path}")


if __name__ == "__main__":
    # Test
    extractor = FrameExtractor()

    # Test extract frames
    try:
        video_path = "test.mp4"
        scenes = [
            {'scene_number': 1, 'start_frame': 0, 'end_frame': 100},
            {'scene_number': 2, 'start_frame': 100, 'end_frame': 200},
        ]
        results = extractor.extract_scene_frames(video_path, scenes)
        print("Extracted frames:", results)
    except Exception as e:
        print(f"Error: {e}")
