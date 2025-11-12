"""
Module phân tích nội dung cảnh bằng AI (OpenAI GPT-4 Vision API)
"""

import base64
import os
import time
from typing import Dict, List, Optional

from tqdm import tqdm


class OpenAIAnalyzer:
    """Phân tích nội dung video bằng AI using OpenAI GPT-4 Vision"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Khởi tạo OpenAI Analyzer

        Args:
            api_key: OpenAI API key (nếu None, lấy từ env OPENAI_API_KEY)
            model: Model OpenAI sử dụng (default: gpt-4o, gpt-4o-mini, gpt-4-turbo)

        Raises:
            ValueError: Nếu không có API key hoặc không thể khởi tạo client
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Cần có OPENAI_API_KEY.\n"
                "Vui lòng:\n"
                "1. Tạo file .env với: OPENAI_API_KEY=your_key\n"
                "2. Hoặc truyền api_key vào constructor\n"
                "3. Hoặc chạy với --no-ai"
            )

        self.model = model
        self.client = self._initialize_client()

    def _initialize_client(self):
        """
        Khởi tạo OpenAI client

        Returns:
            OpenAI client instance

        Raises:
            ValueError: Nếu không thể khởi tạo client
        """
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            print(f"✓ Đã kết nối OpenAI API (model: {self.model})")
            return client
        except ImportError:
            raise ValueError(
                "Không tìm thấy thư viện openai.\n"
                "Vui lòng cài đặt: pip install openai"
            )
        except Exception as e:
            raise ValueError(f"Không thể khởi tạo OpenAI client: {e}")

    def analyze_scenes(
        self,
        scenes: List[Dict],
        detail_level: str = "normal"
    ) -> List[Dict]:
        """
        Phân tích tất cả các cảnh

        Args:
            scenes: Danh sách các scene với frames
            detail_level: Mức độ chi tiết (brief, normal, detailed, comprehensive)

        Returns:
            Danh sách scenes đã được thêm description
        """
        print(f"\n[AI] Đang phân tích {len(scenes)} cảnh bằng OpenAI GPT-4 Vision...")

        # Tạo prompt template dựa trên detail level
        prompt_template = self._get_prompt_template(detail_level)

        analyzed_scenes = []

        for scene in tqdm(scenes, desc="Phân tích AI"):
            try:
                description = self._analyze_single_scene(scene, prompt_template)
                scene['description'] = description
                analyzed_scenes.append(scene)

                # Rate limiting: tránh quá nhiều requests/phút
                time.sleep(0.5)

            except Exception as e:
                print(f"⚠ Lỗi phân tích cảnh {scene['scene_number']}: {e}")
                scene['description'] = f"Không thể phân tích (lỗi: {str(e)})"
                analyzed_scenes.append(scene)

        return analyzed_scenes

    def _analyze_single_scene(self, scene: Dict, prompt_template: str) -> str:
        """
        Phân tích một cảnh đơn

        Args:
            scene: Thông tin cảnh với frames
            prompt_template: Template prompt

        Returns:
            Mô tả cảnh
        """
        # Lấy frames (ưu tiên first, middle, last)
        frames = scene.get('frames', {})
        frame_paths = []

        for key in ['first', 'middle', 'last']:
            if key in frames and os.path.exists(frames[key]):
                frame_paths.append(frames[key])

        if not frame_paths:
            return "Không có frame để phân tích"

        # Encode images to base64
        encoded_images = []
        for frame_path in frame_paths:
            try:
                with open(frame_path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                    encoded_images.append(image_data)
            except Exception as e:
                print(f"⚠ Không thể đọc frame {frame_path}: {e}")

        if not encoded_images:
            return "Không thể đọc frames"

        # Tạo prompt với thông tin cảnh
        duration = scene.get('duration', 0)
        scene_number = scene.get('scene_number', 0)

        prompt = prompt_template.format(
            scene_number=scene_number,
            duration=f"{duration:.1f}",
            num_frames=len(encoded_images)
        )

        # Tạo messages cho OpenAI API
        content = [
            {
                "type": "text",
                "text": prompt
            }
        ]

        # Thêm images
        for img_data in encoded_images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_data}"
                }
            })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=500
            )

            description = response.choices[0].message.content.strip()
            return description

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def _get_prompt_template(self, detail_level: str) -> str:
        """
        Lấy prompt template theo mức độ chi tiết

        Args:
            detail_level: brief, normal, detailed, comprehensive

        Returns:
            Prompt template string
        """
        prompts = {
            'brief': (
                "Mô tả ngắn gọn cảnh {scene_number} (thời lượng {duration}s) "
                "dựa trên {num_frames} frame này. Chỉ nêu nội dung chính trong 1-2 câu."
            ),
            'normal': (
                "Phân tích cảnh {scene_number} (thời lượng {duration}s) dựa trên {num_frames} frame:\n"
                "- Nội dung chính đang diễn ra\n"
                "- Đối tượng/người xuất hiện\n"
                "- Bối cảnh, môi trường\n"
                "Viết 2-3 câu ngắn gọn."
            ),
            'detailed': (
                "Phân tích CHI TIẾT cảnh {scene_number} (thời lượng {duration}s) dựa trên {num_frames} frame:\n"
                "1. Mô tả nội dung chính đang diễn ra\n"
                "2. Các đối tượng/nhân vật xuất hiện (trang phục, hành động)\n"
                "3. Bối cảnh, môi trường, ánh sáng\n"
                "4. Góc quay, chuyển động camera (nếu có)\n"
                "5. Điểm đặc biệt/nổi bật\n"
                "Viết 4-5 câu chi tiết."
            ),
            'comprehensive': (
                "Phân tích TOÀN DIỆN và RẤT CHI TIẾT cảnh {scene_number} (thời lượng {duration}s):\n\n"
                "1. NỘI DUNG:\n"
                "   - Diễn biến chính trong cảnh\n"
                "   - Hành động của các nhân vật/đối tượng\n\n"
                "2. HÌNH ẢNH:\n"
                "   - Đối tượng xuất hiện (mô tả chi tiết)\n"
                "   - Trang phục, màu sắc\n"
                "   - Bối cảnh, không gian\n\n"
                "3. KỸ THUẬT:\n"
                "   - Ánh sáng, màu sắc tổng thể\n"
                "   - Góc quay, composition\n"
                "   - Chuyển động camera\n\n"
                "4. CẢM XÚC/TONE:\n"
                "   - Không khí, cảm giác\n"
                "   - Message/ý nghĩa (nếu có)\n\n"
                "Viết mô tả đầy đủ, chi tiết nhất có thể."
            )
        }

        return prompts.get(detail_level, prompts['normal'])
