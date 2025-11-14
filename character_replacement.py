"""
Character Replacement in Video
Thay thế nhân vật trong video sử dụng AI

Module này cung cấp chức năng thay thế nhân vật/đối tượng trong video
bằng cách sử dụng các kỹ thuật AI và xử lý ảnh.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List
import json
from datetime import datetime


class CharacterReplacer:
    """Class để thay thế nhân vật trong video"""

    def __init__(self, video_path: str):
        """
        Khởi tạo CharacterReplacer

        Args:
            video_path: Đường dẫn đến file video đầu vào
        """
        self.video_path = Path(video_path)
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file không tồn tại: {video_path}")

        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            raise ValueError(f"Không thể mở video: {video_path}")

        # Lấy thông tin video
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.total_frames / self.fps if self.fps > 0 else 0

        # Khởi tạo các detector
        self._init_detectors()

    def _init_detectors(self):
        """Khởi tạo các detector cho face và body"""
        try:
            # Face detector (Haar Cascade)
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )

            # Body detector (Haar Cascade)
            self.body_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_fullbody.xml'
            )

            print("✓ Đã khởi tạo face và body detectors")
        except Exception as e:
            print(f"⚠ Cảnh báo: Không thể khởi tạo detectors: {e}")

    def get_video_info(self) -> dict:
        """Lấy thông tin video"""
        return {
            "filename": self.video_path.name,
            "path": str(self.video_path),
            "resolution": f"{self.width}x{self.height}",
            "fps": self.fps,
            "total_frames": self.total_frames,
            "duration_seconds": self.duration
        }

    def detect_characters(self, frame: np.ndarray) -> List[dict]:
        """
        Phát hiện nhân vật trong frame

        Args:
            frame: Frame ảnh từ video

        Returns:
            List các dictionary chứa thông tin nhân vật phát hiện được
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        characters = []

        # Phát hiện khuôn mặt
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for idx, (x, y, w, h) in enumerate(faces):
            characters.append({
                "type": "face",
                "id": idx,
                "bbox": {"x": int(x), "y": int(y), "w": int(w), "h": int(h)},
                "center": {"x": int(x + w/2), "y": int(y + h/2)}
            })

        # Phát hiện body
        bodies = self.body_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 100)
        )

        for idx, (x, y, w, h) in enumerate(bodies):
            # Kiểm tra nếu body không trùng với face đã detect
            overlap = False
            for char in characters:
                if char["type"] == "face":
                    fx, fy, fw, fh = char["bbox"]["x"], char["bbox"]["y"], char["bbox"]["w"], char["bbox"]["h"]
                    if self._is_overlapping((x, y, w, h), (fx, fy, fw, fh)):
                        overlap = True
                        break

            if not overlap:
                characters.append({
                    "type": "body",
                    "id": idx,
                    "bbox": {"x": int(x), "y": int(y), "w": int(w), "h": int(h)},
                    "center": {"x": int(x + w/2), "y": int(y + h/2)}
                })

        return characters

    def _is_overlapping(self, box1: Tuple, box2: Tuple, threshold: float = 0.3) -> bool:
        """Kiểm tra 2 bounding box có overlap không"""
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2

        # Tính intersection
        x_left = max(x1, x2)
        y_top = max(y1, y2)
        x_right = min(x1 + w1, x2 + w2)
        y_bottom = min(y1 + h1, y2 + h2)

        if x_right < x_left or y_bottom < y_top:
            return False

        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        box1_area = w1 * h1
        box2_area = w2 * h2

        iou = intersection_area / float(box1_area + box2_area - intersection_area)
        return iou > threshold

    def replace_character_blur(
        self,
        frame: np.ndarray,
        character: dict,
        blur_strength: int = 51
    ) -> np.ndarray:
        """
        Thay thế nhân vật bằng cách blur vùng đó

        Args:
            frame: Frame gốc
            character: Thông tin nhân vật cần thay thế
            blur_strength: Độ mạnh của blur (số lẻ)

        Returns:
            Frame đã được xử lý
        """
        result = frame.copy()
        bbox = character["bbox"]
        x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]

        # Blur vùng nhân vật
        roi = result[y:y+h, x:x+w]
        blurred = cv2.GaussianBlur(roi, (blur_strength, blur_strength), 0)
        result[y:y+h, x:x+w] = blurred

        return result

    def replace_character_pixelate(
        self,
        frame: np.ndarray,
        character: dict,
        pixel_size: int = 20
    ) -> np.ndarray:
        """
        Thay thế nhân vật bằng pixelation/mosaic

        Args:
            frame: Frame gốc
            character: Thông tin nhân vật cần thay thế
            pixel_size: Kích thước pixel (càng lớn càng mờ)

        Returns:
            Frame đã được xử lý
        """
        result = frame.copy()
        bbox = character["bbox"]
        x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]

        # Pixelate vùng nhân vật
        roi = result[y:y+h, x:x+w]

        # Giảm kích thước
        temp = cv2.resize(roi, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
        # Tăng lại kích thước
        pixelated = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

        result[y:y+h, x:x+w] = pixelated

        return result

    def replace_character_color(
        self,
        frame: np.ndarray,
        character: dict,
        color: Tuple[int, int, int] = (0, 0, 0)
    ) -> np.ndarray:
        """
        Thay thế nhân vật bằng màu đồng nhất

        Args:
            frame: Frame gốc
            character: Thông tin nhân vật cần thay thế
            color: Màu thay thế (B, G, R)

        Returns:
            Frame đã được xử lý
        """
        result = frame.copy()
        bbox = character["bbox"]
        x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]

        # Tạo silhouette
        cv2.rectangle(result, (x, y), (x+w, y+h), color, -1)

        return result

    def replace_character_image(
        self,
        frame: np.ndarray,
        character: dict,
        replacement_image_path: str
    ) -> np.ndarray:
        """
        Thay thế nhân vật bằng ảnh khác

        Args:
            frame: Frame gốc
            character: Thông tin nhân vật cần thay thế
            replacement_image_path: Đường dẫn đến ảnh thay thế

        Returns:
            Frame đã được xử lý
        """
        result = frame.copy()
        bbox = character["bbox"]
        x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]

        # Đọc ảnh thay thế
        replacement = cv2.imread(replacement_image_path)
        if replacement is None:
            print(f"⚠ Không thể đọc ảnh: {replacement_image_path}")
            return result

        # Resize ảnh thay thế để khớp với kích thước nhân vật
        replacement_resized = cv2.resize(replacement, (w, h))

        # Thay thế vùng nhân vật
        result[y:y+h, x:x+w] = replacement_resized

        return result

    def process_video(
        self,
        output_path: str,
        replacement_method: str = "blur",
        replacement_image: Optional[str] = None,
        character_filter: Optional[str] = None,
        show_bboxes: bool = False,
        frame_skip: int = 1
    ) -> dict:
        """
        Xử lý video và thay thế nhân vật

        Args:
            output_path: Đường dẫn lưu video đầu ra
            replacement_method: Phương pháp thay thế ("blur", "pixelate", "color", "image")
            replacement_image: Đường dẫn ảnh thay thế (nếu method="image")
            character_filter: Lọc loại nhân vật ("face", "body", None=all)
            show_bboxes: Hiển thị bounding boxes
            frame_skip: Bỏ qua n frames (tăng tốc độ xử lý)

        Returns:
            Dictionary chứa thống kê xử lý
        """
        # Khởi tạo video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        if not out.isOpened():
            raise ValueError(f"Không thể tạo video output: {output_path}")

        stats = {
            "start_time": datetime.now().isoformat(),
            "input_video": str(self.video_path),
            "output_video": output_path,
            "method": replacement_method,
            "frames_processed": 0,
            "characters_replaced": 0,
            "processing_errors": 0
        }

        print(f"\n🎬 Bắt đầu xử lý video...")
        print(f"   Input: {self.video_path.name}")
        print(f"   Output: {output_path}")
        print(f"   Method: {replacement_method}")
        print(f"   Total frames: {self.total_frames}")

        frame_count = 0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset về frame đầu

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_count += 1

            # Skip frames nếu cần
            if frame_count % (frame_skip + 1) != 0:
                out.write(frame)
                continue

            try:
                # Phát hiện nhân vật
                characters = self.detect_characters(frame)

                # Lọc theo loại nhân vật nếu cần
                if character_filter:
                    characters = [c for c in characters if c["type"] == character_filter]

                # Thay thế từng nhân vật
                processed_frame = frame.copy()
                for char in characters:
                    if replacement_method == "blur":
                        processed_frame = self.replace_character_blur(processed_frame, char)
                    elif replacement_method == "pixelate":
                        processed_frame = self.replace_character_pixelate(processed_frame, char)
                    elif replacement_method == "color":
                        processed_frame = self.replace_character_color(processed_frame, char)
                    elif replacement_method == "image" and replacement_image:
                        processed_frame = self.replace_character_image(processed_frame, char, replacement_image)

                    stats["characters_replaced"] += 1

                    # Vẽ bounding box nếu cần
                    if show_bboxes:
                        bbox = char["bbox"]
                        cv2.rectangle(
                            processed_frame,
                            (bbox["x"], bbox["y"]),
                            (bbox["x"] + bbox["w"], bbox["y"] + bbox["h"]),
                            (0, 255, 0), 2
                        )
                        cv2.putText(
                            processed_frame,
                            char["type"],
                            (bbox["x"], bbox["y"] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2
                        )

                out.write(processed_frame)
                stats["frames_processed"] += 1

                # Hiển thị tiến trình
                if frame_count % 30 == 0:
                    progress = (frame_count / self.total_frames) * 100
                    print(f"   Progress: {progress:.1f}% ({frame_count}/{self.total_frames})")

            except Exception as e:
                print(f"⚠ Lỗi xử lý frame {frame_count}: {e}")
                stats["processing_errors"] += 1
                out.write(frame)  # Ghi frame gốc nếu có lỗi

        # Cleanup
        out.release()

        stats["end_time"] = datetime.now().isoformat()
        print(f"\n✓ Hoàn thành!")
        print(f"   Frames processed: {stats['frames_processed']}")
        print(f"   Characters replaced: {stats['characters_replaced']}")
        print(f"   Errors: {stats['processing_errors']}")

        return stats

    def extract_characters_info(self, output_json: str, frame_step: int = 30) -> dict:
        """
        Trích xuất thông tin nhân vật từ video

        Args:
            output_json: Đường dẫn file JSON lưu kết quả
            frame_step: Bước nhảy giữa các frame

        Returns:
            Dictionary chứa thông tin nhân vật
        """
        info = {
            "video_info": self.get_video_info(),
            "frame_step": frame_step,
            "characters_timeline": []
        }

        print(f"\n🔍 Trích xuất thông tin nhân vật...")

        frame_count = 0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if frame_count % frame_step == 0:
                characters = self.detect_characters(frame)

                info["characters_timeline"].append({
                    "frame_number": frame_count,
                    "timestamp_seconds": frame_count / self.fps,
                    "characters_detected": len(characters),
                    "characters": characters
                })

                if frame_count % (frame_step * 10) == 0:
                    progress = (frame_count / self.total_frames) * 100
                    print(f"   Progress: {progress:.1f}%")

            frame_count += 1

        # Lưu vào file JSON
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

        print(f"✓ Đã lưu thông tin vào: {output_json}")

        return info

    def __del__(self):
        """Cleanup khi object bị destroy"""
        if hasattr(self, 'cap'):
            self.cap.release()


def main():
    """Demo function"""
    import argparse

    parser = argparse.ArgumentParser(description='Thay thế nhân vật trong video')
    parser.add_argument('input', help='Đường dẫn video đầu vào')
    parser.add_argument('-o', '--output', help='Đường dẫn video đầu ra', default='output.mp4')
    parser.add_argument('-m', '--method',
                       choices=['blur', 'pixelate', 'color', 'image', 'info'],
                       default='blur',
                       help='Phương pháp thay thế')
    parser.add_argument('-i', '--image', help='Đường dẫn ảnh thay thế (cho method=image)')
    parser.add_argument('-f', '--filter', choices=['face', 'body'],
                       help='Lọc loại nhân vật')
    parser.add_argument('-b', '--bbox', action='store_true',
                       help='Hiển thị bounding boxes')
    parser.add_argument('-s', '--skip', type=int, default=0,
                       help='Bỏ qua n frames để tăng tốc')

    args = parser.parse_args()

    try:
        replacer = CharacterReplacer(args.input)

        if args.method == 'info':
            # Chỉ trích xuất thông tin
            output_json = args.output.replace('.mp4', '.json')
            replacer.extract_characters_info(output_json)
        else:
            # Xử lý video
            stats = replacer.process_video(
                output_path=args.output,
                replacement_method=args.method,
                replacement_image=args.image,
                character_filter=args.filter,
                show_bboxes=args.bbox,
                frame_skip=args.skip
            )

            # Lưu stats
            stats_file = args.output.replace('.mp4', '_stats.json')
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            print(f"✓ Đã lưu thống kê vào: {stats_file}")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
