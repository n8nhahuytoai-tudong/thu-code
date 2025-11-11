"""
Module để extract frames từ video
"""

import cv2
from pathlib import Path
from typing import List, Dict
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
        """Extract một frame cụ thể từ video"""
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if not ret:
            raise ValueError(f"Không thể đọc frame {frame_number}")

        output_path = output_dir / filename
        cv2.imwrite(str(output_path), frame)

        return str(output_path)
