"""
Module phân tích nội dung cảnh bằng AI (Claude Vision API)
Compatible with multiple anthropic library versions
"""

import base64
import os
import time
from typing import Dict, List, Optional

from tqdm import tqdm


class AIAnalyzer:
    """Phân tích nội dung video bằng AI using Claude Vision"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Khởi tạo AI Analyzer

        Args:
            api_key: Anthropic API key (nếu None, lấy từ env ANTHROPIC_API_KEY)
            model: Model Claude sử dụng (default: claude-3-5-sonnet-20241022)

        Raises:
            ValueError: Nếu không có API key hoặc không thể khởi tạo client
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Cần có ANTHROPIC_API_KEY.\n"
                "Vui lòng:\n"
                "1. Tạo file .env với: ANTHROPIC_API_KEY=your_key\n"
                "2. Hoặc truyền api_key vào constructor\n"
                "3. Hoặc chạy với --no-ai"
            )

        self.model = model
        self.client = self._initialize_client()

    def _initialize_client(self):
        """
        Khởi tạo Anthropic client với hỗ trợ nhiều version

        Returns:
            Anthropic client instance

        Raises:
            ValueError: Nếu không thể khởi tạo client
        """
        try:
            import anthropic
        except ImportError:
            raise ValueError(
                "Chưa cài đặt anthropic library.\n"
                "Vui lòng chạy: pip install anthropic"
            )

        # Thử các cách khởi tạo khác nhau cho các version khác nhau

        # Method 1: Modern API (anthropic >= 0.18.0)
        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            # Test client
            return client
        except TypeError as e:
            if 'proxies' in str(e) or 'unexpected keyword' in str(e):
                pass  # Try next method
            else:
                raise

        # Method 2: Older API (anthropic < 0.18.0)
        try:
            client = anthropic.Client(self.api_key)
            return client
        except Exception:
            pass

        # Method 3: Alternative initialization
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            return client
        except Exception:
            pass

        # If all methods fail
        raise ValueError(
            "Không thể khởi tạo Anthropic client.\n"
            "Vui lòng:\n"
            "1. Update library: pip install --upgrade anthropic\n"
            "2. Hoặc cài version cụ thể: pip install anthropic==0.39.0\n"
            "3. Hoặc chạy với --no-ai để bỏ qua AI analysis"
        )

    def analyze_scene(
        self,
        scene_data: Dict,
        language: str = "vi",
        detail_level: str = "detailed"
    ) -> Dict:
        """
        Phân tích một cảnh dựa trên frames

        Args:
            scene_data: Dict chứa thông tin scene và frames
                {
                    'scene_number': int,
                    'duration': float,
                    'frames': {
                        'first': str (path),
                        'middle': str (path),
                        'last': str (path)
                    }
                }
            language: Ngôn ngữ mô tả ("vi" hoặc "en")
            detail_level: Mức độ chi tiết ("brief", "detailed", "very_detailed")

        Returns:
            scene_data với thêm trường 'description'
        """
        frames = scene_data.get('frames', {})

        if not frames:
            scene_data['description'] = "Không có frame để phân tích"
            return scene_data

        # Tạo prompt
        prompt = self._create_prompt(scene_data, language, detail_level)

        # Chuẩn bị images cho API
        image_contents = []

        for frame_type in ['first', 'middle', 'last']:
            if frame_type in frames:
                try:
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
                except Exception as e:
                    print(f"⚠ Không thể load frame {frame_type}: {e}")

        if not image_contents:
            scene_data['description'] = "Không thể load frames để phân tích"
            return scene_data

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
            error_msg = str(e)
            print(f"⚠ Lỗi khi phân tích scene {scene_data['scene_number']}: {error_msg}")

            # Cung cấp thông tin lỗi hữu ích
            if "rate_limit" in error_msg.lower():
                scene_data['description'] = "Lỗi: Vượt quá giới hạn API (rate limit)"
            elif "api_key" in error_msg.lower():
                scene_data['description'] = "Lỗi: API key không hợp lệ"
            elif "quota" in error_msg.lower():
                scene_data['description'] = "Lỗi: Hết quota API"
            else:
                scene_data['description'] = f"Lỗi phân tích: {error_msg[:100]}"

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
            language: Ngôn ngữ mô tả ("vi" hoặc "en")
            detail_level: Mức độ chi tiết ("brief", "detailed", "very_detailed")
            delay: Delay giữa các API call (seconds) để tránh rate limit

        Returns:
            List scenes với descriptions
        """
        if not scenes:
            print("⚠ Không có cảnh nào để phân tích")
            return []

        print(f"\n🤖 Đang phân tích {len(scenes)} cảnh bằng AI...")
        print(f"   Mức độ: {detail_level}, Ngôn ngữ: {language}")

        results = []

        for scene in tqdm(scenes, desc="Analyzing scenes"):
            analyzed_scene = self.analyze_scene(scene, language, detail_level)
            results.append(analyzed_scene)

            # Delay để tránh rate limit
            if delay > 0 and scene != scenes[-1]:  # Không delay ở scene cuối
                time.sleep(delay)

        # Đếm số cảnh thành công
        success_count = sum(
            1 for s in results
            if s.get('description') and not s['description'].startswith('Lỗi')
        )

        print(f"✓ Hoàn tất phân tích AI: {success_count}/{len(scenes)} cảnh thành công")

        return results

    def _create_prompt(self, scene_data: Dict, language: str, detail_level: str) -> str:
        """
        Tạo prompt cho AI dựa trên yêu cầu

        Args:
            scene_data: Thông tin scene
            language: Ngôn ngữ ("vi" hoặc "en")
            detail_level: Mức độ chi tiết

        Returns:
            Prompt string
        """
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
1. **Bối cảnh/Môi trường**: Cảnh diễn ra ở đâu? (trong nhà, ngoài trời, địa điểm cụ thể)
2. **Nhân vật/Đối tượng**: Có ai/cái gì trong cảnh? Họ đang làm gì?
3. **Hành động chính**: Diễn biến chính của cảnh (nếu có)
4. **Chi tiết đáng chú ý**: Các yếu tố quan trọng khác (màu sắc, ánh sáng, cảm xúc)
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

        Raises:
            FileNotFoundError: Nếu file không tồn tại
            Exception: Nếu không thể đọc file
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Frame không tồn tại: {image_path}")

        try:
            with open(image_path, "rb") as image_file:
                return base64.standard_b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            raise Exception(f"Không thể đọc frame {image_path}: {e}")

    def analyze_with_custom_prompt(
        self,
        image_paths: List[str],
        custom_prompt: str,
        max_tokens: int = 2048
    ) -> str:
        """
        Phân tích với prompt tùy chỉnh (advanced usage)

        Args:
            image_paths: List đường dẫn ảnh
            custom_prompt: Prompt tùy chỉnh
            max_tokens: Số tokens tối đa cho response

        Returns:
            Kết quả phân tích

        Raises:
            Exception: Nếu có lỗi khi gọi API
        """
        image_contents = []

        for img_path in image_paths:
            try:
                image_data = self._encode_image(img_path)
                image_contents.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data,
                    },
                })
            except Exception as e:
                print(f"⚠ Không thể load ảnh {img_path}: {e}")

        if not image_contents:
            raise ValueError("Không có ảnh hợp lệ nào để phân tích")

        message_content = image_contents + [{"type": "text", "text": custom_prompt}]

        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": message_content
                }
            ]
        )

        return message.content[0].text.strip()


# Module level helper function
def check_api_key() -> bool:
    """
    Kiểm tra xem có API key không

    Returns:
        True nếu có API key, False nếu không
    """
    return bool(os.getenv("ANTHROPIC_API_KEY"))


if __name__ == "__main__":
    # Test code
    print("Testing AIAnalyzer...")

    if not check_api_key():
        print("❌ Không tìm thấy ANTHROPIC_API_KEY")
        print("   Vui lòng set environment variable hoặc tạo file .env")
    else:
        try:
            analyzer = AIAnalyzer()
            print(f"✓ Khởi tạo AIAnalyzer thành công")
            print(f"  Model: {analyzer.model}")
        except Exception as e:
            print(f"❌ Lỗi khi khởi tạo: {e}")
