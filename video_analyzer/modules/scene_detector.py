"""
Module phát hiện các cảnh trong video
Sử dụng PySceneDetect để tự động phát hiện thay đổi cảnh
"""

import cv2
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector, ThresholdDetector, AdaptiveDetector
from typing import List, Tuple, Dict
from pathlib import Path


class SceneDetector:
    """Phát hiện các cảnh trong video"""

    def __init__(self, threshold: float = 27.0, min_scene_len: int = 15):
        """
        Khởi tạo Scene Detector

        Args:
            threshold: Ngưỡng để phát hiện thay đổi cảnh (27.0 là mặc định, càng thấp càng nhạy)
            min_scene_len: Độ dài tối thiểu của một cảnh (số frame)
        """
        self.threshold = threshold
        self.min_scene_len = min_scene_len

    def detect_scenes(self, video_path: str, method: str = "content") -> List[Dict]:
        """
        Phát hiện các cảnh trong video

        Args:
            video_path: Đường dẫn đến file video
            method: Phương pháp detect ("content", "threshold", "adaptive")

        Returns:
            List các scene với thông tin start_time, end_time, start_frame, end_frame
        """
        print(f"\n🎬 Đang phát hiện cảnh trong video: {Path(video_path).name}")
        print(f"   Phương pháp: {method}, Threshold: {self.threshold}")

        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()

        # Chọn detector
        if method == "content":
            detector = ContentDetector(threshold=self.threshold, min_scene_len=self.min_scene_len)
        elif method == "threshold":
            detector = ThresholdDetector(threshold=self.threshold, min_scene_len=self.min_scene_len)
        elif method == "adaptive":
            detector = AdaptiveDetector(min_scene_len=self.min_scene_len)
        else:
            raise ValueError(f"Method không hợp lệ: {method}")

        scene_manager.add_detector(detector)

        # Start video manager và detect scenes
        video_manager.set_downscale_factor()
        video_manager.start()

        # Detect scenes
        scene_manager.detect_scenes(frame_source=video_manager)

        # Get scene list
        scene_list = scene_manager.get_scene_list()
        video_fps = video_manager.get_framerate()
        video_manager.release()

        # Convert to readable format
        scenes = []
        for i, scene in enumerate(scene_list, 1):
            start_frame = scene[0].get_frames()
            end_frame = scene[1].get_frames()
            start_time = scene[0].get_seconds()
            end_time = scene[1].get_seconds()

            scenes.append({
                'scene_number': i,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'start_time': start_time,
                'end_time': end_time,
                'duration': end_time - start_time,
                'num_frames': end_frame - start_frame
            })

        print(f"✓ Đã phát hiện {len(scenes)} cảnh")

        # Nếu không detect được cảnh nào, coi toàn bộ video là 1 cảnh
        if len(scenes) == 0:
            print("⚠ Không phát hiện được thay đổi cảnh, coi toàn bộ video là 1 cảnh")
            scenes = self._create_single_scene(video_path, video_fps)

        return scenes

    def _create_single_scene(self, video_path: str, fps: float) -> List[Dict]:
        """
        Tạo 1 scene duy nhất cho toàn bộ video nếu không detect được

        Args:
            video_path: Đường dẫn video
            fps: Frame rate của video

        Returns:
            List chứa 1 scene duy nhất
        """
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        cap.release()

        return [{
            'scene_number': 1,
            'start_frame': 0,
            'end_frame': total_frames,
            'start_time': 0.0,
            'end_time': duration,
            'duration': duration,
            'num_frames': total_frames
        }]

    def get_video_info(self, video_path: str) -> Dict:
        """
        Lấy thông tin về video

        Args:
            video_path: Đường dẫn video

        Returns:
            Dict chứa thông tin video
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Không thể mở video: {video_path}")

        info = {
            'path': video_path,
            'filename': Path(video_path).name,
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        }

        cap.release()

        return info

    def format_time(self, seconds: float) -> str:
        """
        Format thời gian từ seconds sang HH:MM:SS

        Args:
            seconds: Số giây

        Returns:
            Chuỗi thời gian định dạng HH:MM:SS
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


if __name__ == "__main__":
    # Test
    detector = SceneDetector(threshold=27.0)

    # Test với video
    try:
        video_path = "test.mp4"
        info = detector.get_video_info(video_path)
        print("Video Info:", info)

        scenes = detector.detect_scenes(video_path)
        for scene in scenes:
            print(f"Scene {scene['scene_number']}: "
                  f"{detector.format_time(scene['start_time'])} - "
                  f"{detector.format_time(scene['end_time'])}")
    except Exception as e:
        print(f"Error: {e}")
