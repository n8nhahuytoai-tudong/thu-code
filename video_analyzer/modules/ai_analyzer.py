"""
Module phân tích nội dung cảnh bằng AI (Claude Vision API)
"""

import anthropic
import base64
import os
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm
import time


class AIAnalyzer:
    """Phân tích nội dung video bằng AI"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Khởi tạo AI Analyzer

        Args:
            api_key: Anthropic API key (nếu không cung cấp, sẽ lấy từ env ANTHROPIC_API_KEY)
            model: Model Claude sử dụng
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Cần có ANTHROPIC_API_KEY. "
                "Vui lòng set environment variable hoặc truyền vào constructor"
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model

    def analyze_scene(
        self,
        scene_data: Dict,
        language: str = "vi",
        detail_level: str = "detailed"
    ) -> Dict:
        """
        Phân tích một cảnh dựa trên frames

        Args:
            scene_data: Dict chứa thông tin scene và đường dẫn frames
            language: Ngôn ngữ mô tả ("vi" hoặc "en")
            detail_level: Mức độ chi tiết ("brief", "detailed", "very_detailed")

        Returns:
            scene_data với thêm trường 'description'
        """
        frames = scene_data.get('frames', {})

        if not frames:
            scene_data['description'] = "Không có frame để phân tích"
            return scene_data

        # Tạo prompt dựa trên detail_level
        prompt = self._create_prompt(scene_data, language, detail_level)

        # Chuẩn bị images cho API
        image_contents = []

        for frame_type in ['first', 'middle', 'last']:
            if frame_type in frames:
                image_path = frames[frame_type]
                image_data = self._encode_image(image_path)

                image_contents.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data,
                    },
                })

        # Gọi Claude API
        try:
            message_content = image_contents + [{"type": "text", "text": prompt}]

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": message_content
                    }
                ]
            )

            description = message.content[0].text
            scene_data['description'] = description.strip()

        except Exception as e:
            print(f"⚠ Lỗi khi phân tích scene {scene_data['scene_number']}: {e}")
            scene_data['description'] = f"Lỗi phân tích: {str(e)}"

        return scene_data

    def analyze_all_scenes(
        self,
        scenes: List[Dict],
        language: str = "vi",
        detail_level: str = "detailed",
        delay: float = 0.5
    ) -> List[Dict]:
        """
        Phân tích tất cả các cảnh

        Args:
            scenes: List các scene với frames
            language: Ngôn ngữ mô tả
            detail_level: Mức độ chi tiết
            delay: Delay giữa các API call (để tránh rate limit)

        Returns:
            List scenes với descriptions
        """
        print(f"\n🤖 Đang phân tích {len(scenes)} cảnh bằng AI...")

        results = []

        for scene in tqdm(scenes, desc="Analyzing scenes"):
            analyzed_scene = self.analyze_scene(scene, language, detail_level)
            results.append(analyzed_scene)

            # Delay để tránh rate limit
            if delay > 0:
                time.sleep(delay)

        print("✓ Hoàn tất phân tích AI")

        return results

    def _create_prompt(self, scene_data: Dict, language: str, detail_level: str) -> str:
        """Tạo prompt cho AI dựa trên yêu cầu"""

        scene_num = scene_data['scene_number']
        duration = scene_data.get('duration', 0)

        if language == "vi":
            base_prompt = f"""Đây là cảnh số {scene_num} trong video (thời lượng: {duration:.1f}s).

Hãy phân tích và mô tả nội dung của cảnh này một cách chi tiết.
"""

            if detail_level == "brief":
                base_prompt += "\nMô tả ngắn gọn (1-2 câu) nội dung chính của cảnh."

            elif detail_level == "detailed":
                base_prompt += """
Mô tả chi tiết theo các khía cạnh sau:
1. **Bối cảnh/Môi trường**: Cảnh diễn ra ở đâu? (trong nhà, ngoài trời, địa điểm cụ thể, thời gian trong ngày)
2. **Nhân vật/Đối tượng**: Có ai/cái gì trong cảnh? Họ đang làm gì?
3. **Hành động chính**: Diễn biến chính của cảnh (nếu có)
4. **Chi tiết đáng chú ý**: Các yếu tố quan trọng khác (màu sắc, ánh sáng, cảm xúc, v.v.)
"""

            elif detail_level == "very_detailed":
                base_prompt += """
Phân tích CỰC KỲ CHI TIẾT cảnh này:

1. **Bối cảnh & Môi trường**:
   - Địa điểm, không gian
   - Thời gian (ngày/đêm, mùa nào)
   - Điều kiện thời tiết, ánh sáng

2. **Nhân vật & Đối tượng**:
   - Số lượng người
   - Ngoại hình, trang phục
   - Vị trí, tư thế
   - Biểu cảm, cảm xúc

3. **Hành động & Diễn biến**:
   - Hoạt động chính
   - Tương tác giữa các nhân vật
   - Chuyển động, di chuyển

4. **Kỹ thuật quay & Thị giác**:
   - Góc quay, composition
   - Màu sắc chủ đạo
   - Ánh sáng, bóng tối
   - Các hiệu ứng đặc biệt (nếu có)

5. **Âm thanh có thể đoán được**:
   - Âm thanh môi trường
   - Lời thoại (nếu nhìn thấy)
   - Âm nhạc (nếu có dấu hiệu)

6. **Ý nghĩa & Ngữ cảnh**:
   - Mục đích của cảnh
   - Thông điệp/ý nghĩa
   - Mối liên hệ với cảnh trước/sau (nếu đoán được)
"""

        else:  # English
            base_prompt = f"""This is scene number {scene_num} in the video (duration: {duration:.1f}s).

Please analyze and describe the content of this scene in detail.
"""

            if detail_level == "brief":
                base_prompt += "\nProvide a brief description (1-2 sentences) of the main content."

            elif detail_level == "detailed":
                base_prompt += """
Describe in detail:
1. **Setting/Environment**: Where does it take place?
2. **Characters/Objects**: Who/what is in the scene? What are they doing?
3. **Main Action**: Key events happening
4. **Notable Details**: Other important elements (colors, lighting, emotions, etc.)
"""

            elif detail_level == "very_detailed":
                base_prompt += """
Provide EXTREMELY DETAILED analysis:

1. **Setting & Environment**
2. **Characters & Objects**
3. **Actions & Events**
4. **Cinematography & Visual Elements**
5. **Potential Audio**
6. **Meaning & Context**
"""

        return base_prompt

    def _encode_image(self, image_path: str) -> str:
        """
        Encode ảnh thành base64

        Args:
            image_path: Đường dẫn file ảnh

        Returns:
            Base64 encoded string
        """
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

    def analyze_with_custom_prompt(
        self,
        image_paths: List[str],
        custom_prompt: str
    ) -> str:
        """
        Phân tích với prompt tùy chỉnh

        Args:
            image_paths: List đường dẫn ảnh
            custom_prompt: Prompt tùy chỉnh

        Returns:
            Kết quả phân tích
        """
        image_contents = []

        for img_path in image_paths:
            image_data = self._encode_image(img_path)
            image_contents.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data,
                },
            })

        message_content = image_contents + [{"type": "text", "text": custom_prompt}]

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": message_content
                }
            ]
        )

        return message.content[0].text.strip()


if __name__ == "__main__":
    # Test
    try:
        analyzer = AIAnalyzer()

        # Test với một scene
        scene_data = {
            'scene_number': 1,
            'duration': 5.2,
            'frames': {
                'first': 'path/to/first.jpg',
                'last': 'path/to/last.jpg'
            }
        }

        result = analyzer.analyze_scene(scene_data, language="vi", detail_level="detailed")
        print("Description:", result['description'])

    except Exception as e:
        print(f"Error: {e}")
