#!/usr/bin/env python3

"""
YouTube Video Analyzer to Sora 2 Prompt Generator - ADVANCED VERSION 2.1
Phân tích video YouTube cực kỳ chi tiết và tạo prompts chuyên nghiệp cho Sora 2

Features:
- Không giới hạn số scenes
- Phân tích chi tiết nhân vật: chiều cao, cân nặng, màu da, tóc, trang phục, tỷ lệ cơ thể
- Phân tích chi tiết con vật: loài, kích thước, màu sắc, đặc điểm, tỷ lệ
- Scene detection tự động thông minh
- Audio transcription với Whisper
- Visual composition analysis
- Camera movement detection
- Multiple prompt variants
- Intelligent caching
"""

import os
import sys
import time
import subprocess
import cv2
import base64
import numpy as np
from pathlib import Path
import json
from openai import OpenAI
from datetime import datetime
import hashlib
from typing import List, Dict, Optional, Any
import shutil

# ========== CONFIGURATION ==========

class Config:
    """Cấu hình toàn cục"""
    # Scene detection
    SCENE_THRESHOLD = 30.0
    MIN_SCENE_LENGTH = 15
    FRAMES_PER_SCENE = 4  # Tăng từ 3 lên 4 để phân tích chi tiết hơn

    # Video download
    MAX_VIDEO_HEIGHT = 1080

    # API settings
    VISION_MODEL = "gpt-4o"
    TEXT_MODEL = "gpt-4o"
    WHISPER_MODEL = "whisper-1"
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    # Folders
    CACHE_DIR = "cache"
    OUTPUT_DIR = "output_results"
    TEMP_FRAMES_DIR = "temp_frames"

    # Limits - BỎ GIỚI HẠN!
    MAX_SCENES_TO_ANALYZE = 999  # Tăng từ 20 lên 999
    MAX_SCENE_SUMMARY_LENGTH = 300  # Tăng từ 200 lên 300


# ========== UTILITIES ==========

def load_env_file():
    """Load environment variables từ file .env"""
    env_file = Path('.env')
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        os.environ[key] = value
        except Exception as e:
            print(f"⚠ Lỗi đọc file .env: {e}")


def ensure_directories():
    """Tạo các thư mục cần thiết"""
    for dir_name in [Config.CACHE_DIR, Config.OUTPUT_DIR, Config.TEMP_FRAMES_DIR]:
        Path(dir_name).mkdir(exist_ok=True)


def cleanup_temp_files():
    """Xóa tất cả files tạm"""
    temp_files = ["temp_video.mp4", "temp_audio.m4a"]
    for f in temp_files:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass

    # Xóa temp frames
    if os.path.exists(Config.TEMP_FRAMES_DIR):
        try:
            shutil.rmtree(Config.TEMP_FRAMES_DIR)
            Path(Config.TEMP_FRAMES_DIR).mkdir(exist_ok=True)
        except:
            pass


def print_header(text: str):
    """In header đẹp"""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")


def print_section(text: str):
    """In section header"""
    print("\n" + "-"*70)
    print(text)
    print("-"*70)


def print_progress(message: str, step: Optional[int] = None, total: Optional[int] = None):
    """In progress message"""
    if step and total:
        print(f"[{step}/{total}] {message}")
    else:
        print(f"• {message}")


def print_success(message: str):
    """In success message"""
    print(f"✓ {message}")


def print_error(message: str):
    """In error message"""
    print(f"✗ {message}")


def print_warning(message: str):
    """In warning message"""
    print(f"⚠ {message}")


# ========== MAIN CLASS ==========

class YouTubeToSoraAnalyzer:
    """
    Advanced YouTube video analyzer cho Sora 2 prompt generation
    Version 2.1 - Phân tích chi tiết nhân vật và con vật
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Khởi tạo analyzer

        Args:
            api_key: OpenAI API key (optional, có thể load từ env)
        """
        # Load .env first
        load_env_file()

        # Setup API key
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key không tìm thấy!\n"
                "Vui lòng:\n"
                "1. Tạo file .env với: OPENAI_API_KEY=sk-your-key\n"
                "2. Hoặc set biến môi trường: export OPENAI_API_KEY=sk-your-key\n"
                "3. Hoặc truyền api_key vào constructor"
            )

        # Initialize OpenAI client
        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Không thể khởi tạo OpenAI client: {e}")

        # Setup directories
        ensure_directories()

        # State
        self.video_path: Optional[str] = None
        self.audio_path: Optional[str] = None
        self.youtube_url: Optional[str] = None
        self.video_title: str = ""
        self.video_metadata: Dict[str, Any] = {}
        self.scenes: List[Dict] = []
        self.frames: List[str] = []

    # ========== CACHE METHODS ==========

    def _get_cache_key(self, url: str) -> str:
        """Tạo cache key từ URL"""
        return hashlib.md5(url.encode()).hexdigest()

    def _save_cache(self, key: str, data: Dict):
        """Lưu data vào cache"""
        try:
            cache_file = Path(Config.CACHE_DIR) / f"{key}.json"
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print_warning(f"Không thể lưu cache: {e}")

    def _load_cache(self, key: str) -> Optional[Dict]:
        """Load data từ cache"""
        try:
            cache_file = Path(Config.CACHE_DIR) / f"{key}.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print_warning(f"Không thể đọc cache: {e}")
        return None

    # ========== VIDEO DOWNLOAD ==========

    def _get_video_metadata(self, youtube_url: str) -> Dict:
        """Lấy metadata từ YouTube"""
        print_progress("Đang lấy thông tin video...")

        try:
            result = subprocess.run(
                ["yt-dlp", "--dump-json", youtube_url],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                metadata = json.loads(result.stdout)
                self.video_title = metadata.get('title', 'Unknown')
                self.video_metadata = {
                    'title': metadata.get('title'),
                    'duration': metadata.get('duration', 0),
                    'description': (metadata.get('description') or '')[:500],
                    'uploader': metadata.get('uploader'),
                    'width': metadata.get('width'),
                    'height': metadata.get('height'),
                    'fps': metadata.get('fps'),
                }
                print_success(f"Video: {self.video_title}")
                print_success(f"Thời lượng: {self.video_metadata['duration']}s")
                return self.video_metadata
        except subprocess.TimeoutExpired:
            print_error("Timeout khi lấy metadata")
        except Exception as e:
            print_error(f"Lỗi lấy metadata: {e}")

        # Fallback
        self.video_title = f"Video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return {}

    def _download_video(self, youtube_url: str) -> bool:
        """Download video và audio"""
        print_progress("Đang tải video...")

        try:
            video_output = "temp_video.mp4"
            audio_output = "temp_audio.m4a"

            # Download video
            result = subprocess.run(
                [
                    "yt-dlp",
                    "-f", f"best[height<={Config.MAX_VIDEO_HEIGHT}][ext=mp4]",
                    "-o", video_output,
                    youtube_url
                ],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode != 0:
                print_error(f"Lỗi tải video: {result.stderr}")
                return False

            self.video_path = video_output
            print_success("Video đã tải xong")

            # Download audio (optional, for transcript)
            try:
                subprocess.run(
                    ["yt-dlp", "-f", "bestaudio[ext=m4a]", "-o", audio_output, youtube_url],
                    capture_output=True,
                    timeout=60
                )
                if os.path.exists(audio_output):
                    self.audio_path = audio_output
                    print_success("Audio đã tải xong")
            except:
                print_warning("Không thể tải audio (bỏ qua)")

            return True

        except subprocess.TimeoutExpired:
            print_error("Timeout khi tải video")
            return False
        except Exception as e:
            print_error(f"Lỗi tải video: {e}")
            return False

    # ========== SCENE DETECTION ==========

    def _detect_scenes(self) -> List[Dict]:
        """Phát hiện scenes tự động"""
        if not self.video_path or not os.path.exists(self.video_path):
            return []

        print_progress("Đang phát hiện scenes...")

        try:
            cap = cv2.VideoCapture(self.video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if total_frames == 0:
                print_error("Không thể đọc video")
                return []

            prev_frame = None
            scene_boundaries = [0]
            frame_idx = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Downsample
                small_frame = cv2.resize(frame, (320, 180))
                gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

                if prev_frame is not None:
                    diff = cv2.absdiff(gray, prev_frame)
                    mean_diff = np.mean(diff)

                    if mean_diff > Config.SCENE_THRESHOLD:
                        if frame_idx - scene_boundaries[-1] > Config.MIN_SCENE_LENGTH:
                            scene_boundaries.append(frame_idx)

                prev_frame = gray
                frame_idx += 1

                # Progress
                if frame_idx % 100 == 0:
                    progress = (frame_idx / total_frames) * 100
                    print(f"\r  Đang xử lý: {progress:.1f}%", end='', flush=True)

            print()  # Newline
            scene_boundaries.append(total_frames - 1)
            cap.release()

            # Create scene info
            scenes = []
            for i in range(len(scene_boundaries) - 1):
                start = scene_boundaries[i]
                end = scene_boundaries[i + 1]
                scenes.append({
                    'scene_id': i,
                    'start_frame': start,
                    'end_frame': end,
                    'start_time': start / fps,
                    'end_time': end / fps,
                    'duration': (end - start) / fps
                })

            # BỎ GIỚI HẠN - Phân tích tất cả scenes
            total_scenes = len(scenes)
            if total_scenes > Config.MAX_SCENES_TO_ANALYZE:
                print_warning(f"Video có {total_scenes} scenes - Sẽ phân tích TẤT CẢ (không giới hạn)")
                # Không cắt nữa!
            else:
                print_success(f"Đã phát hiện {total_scenes} scenes - Sẽ phân tích tất cả")

            self.scenes = scenes
            return scenes

        except Exception as e:
            print_error(f"Lỗi phát hiện scenes: {e}")
            return []

    def _extract_frames_from_scenes(self) -> List[str]:
        """Trích xuất key frames từ scenes"""
        if not self.scenes or not self.video_path:
            return []

        print_progress(f"Đang trích xuất {Config.FRAMES_PER_SCENE} frames từ mỗi scene...")

        try:
            cap = cv2.VideoCapture(self.video_path)
            all_frames = []

            for scene in self.scenes:
                scene_frames = []
                start = scene['start_frame']
                end = scene['end_frame']

                # Lấy frames đều
                positions = np.linspace(start, end, Config.FRAMES_PER_SCENE, dtype=int)

                for pos in positions:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
                    ret, frame = cap.read()

                    if ret:
                        frame_path = f"{Config.TEMP_FRAMES_DIR}/scene_{scene['scene_id']}_frame_{len(scene_frames)}.jpg"
                        cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                        scene_frames.append(frame_path)

                scene['frames'] = scene_frames
                all_frames.extend(scene_frames)

            cap.release()
            self.frames = all_frames
            print_success(f"Đã trích xuất {len(all_frames)} frames từ {len(self.scenes)} scenes")
            return all_frames

        except Exception as e:
            print_error(f"Lỗi trích xuất frames: {e}")
            return []

    # ========== AUDIO ANALYSIS ==========

    def _extract_transcript(self) -> Optional[Dict]:
        """Trích xuất transcript từ audio"""
        if not self.audio_path or not os.path.exists(self.audio_path):
            return None

        print_progress("Đang phân tích audio...")

        try:
            with open(self.audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=Config.WHISPER_MODEL,
                    file=audio_file,
                    response_format="verbose_json"
                )

            result = {
                'text': transcript.text,
                'language': getattr(transcript, 'language', 'unknown'),
                'duration': getattr(transcript, 'duration', 0),
            }

            print_success(f"Transcript: {len(result['text'])} ký tự")
            return result

        except Exception as e:
            print_warning(f"Không thể trích xuất transcript: {e}")
            return None

    # ========== VISUAL ANALYSIS ==========

    def _analyze_visual_composition(self, frame_path: str) -> Dict:
        """Phân tích màu sắc và composition"""
        try:
            img = cv2.imread(frame_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = img_rgb.reshape(-1, 3)

            avg_color = np.mean(pixels, axis=0)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            brightness = float(np.mean(gray))
            contrast = float(np.std(gray))

            # Classify mood
            r, g, b = avg_color
            if brightness < 85:
                mood = "dark, moody"
            elif brightness > 170:
                mood = "bright, airy"
            elif r > g and r > b:
                mood = "warm, energetic"
            elif b > r and b > g:
                mood = "cool, calm"
            else:
                mood = "balanced, natural"

            return {
                'brightness': brightness,
                'contrast': contrast,
                'color_mood': mood
            }
        except:
            return {}

    def _encode_image_base64(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8")

    # ========== AI ANALYSIS - CẢI TIẾN ==========

    def _call_vision_api_with_retry(self, messages: List[Dict], max_tokens: int = 2000) -> Optional[str]:
        """Gọi Vision API với retry logic"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=Config.VISION_MODEL,
                    max_tokens=max_tokens,
                    messages=messages
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt < Config.MAX_RETRIES - 1:
                    print_warning(f"API call failed (attempt {attempt + 1}/{Config.MAX_RETRIES}), retrying...")
                    time.sleep(Config.RETRY_DELAY * (attempt + 1))
                else:
                    print_error(f"API call failed after {Config.MAX_RETRIES} attempts: {e}")
                    return None
        return None

    def _analyze_scene(self, scene: Dict) -> Optional[Dict]:
        """Phân tích chi tiết một scene - CẢI TIẾN"""
        scene_id = scene['scene_id']
        frames = scene.get('frames', [])

        if not frames:
            return None

        print_progress(f"Đang phân tích scene {scene_id + 1}...", scene_id + 1, len(self.scenes))

        # PROMPT CẢI TIẾN - CHI TIẾT NHÂN VẬT VÀ CON VẬT
        content = [{
            "type": "text",
            "text": f"""Phân tích cực kỳ chi tiết scene này (thời lượng: {scene['duration']:.1f}s):

🎬 HÀNH ĐỘNG
- Gì đang xảy ra? Diễn biến chính?
- Tốc độ hành động (chậm/vừa/nhanh)?

👤 NHÂN VẬT (NẾU CÓ) - MÔ TẢ CỰC KỲ CHI TIẾT:
- Số lượng: Bao nhiêu người?
- Giới tính và tuổi ước tính (VD: nam 25-30 tuổi, nữ 40s)
- Chiều cao ước tính (VD: 170cm, tall ~185cm, short ~155cm)
- Thể hình: (slim/athletic/muscular/average/heavyset/petite) và cân nặng ước tính
- Màu da: (pale/fair/tan/olive/brown/dark brown/black) - mô tả chính xác
- Tóc:
  * Màu: (blonde/brown/black/red/gray/white/dyed)
  * Kiểu: (straight/wavy/curly/braided/ponytail/bun/short/long)
  * Độ dài: (buzz cut/short/shoulder-length/long/very long)
- Đặc điểm khuôn mặt: (angular/round/oval/square), mắt, mũi, miệng
- Tỷ lệ cơ thể: (proportions) - đầu:cơ thể, chân dài/ngắn
- Trang phục CHI TIẾT:
  * Loại: (casual/formal/sportswear/uniform/traditional)
  * Màu sắc chủ đạo và họa tiết
  * Form dáng: (fitted/loose/oversized/tight)
  * Phụ kiện: mũ/kính/đồng hồ/trang sức
- Tư thế và ngôn ngữ cơ thể
- Cảm xúc trên khuôn mặt

🐾 CON VẬT (NẾU CÓ) - MÔ TẢ CỰC KỲ CHI TIẾT:
- Loài: (chó/mèo/chim/etc.) và giống cụ thể nếu nhận ra
- Kích thước: (tiny/small/medium/large/giant) + ước tính chiều dài/cao
- Cân nặng ước tính: (VD: 5kg cat, 25kg dog, 500g bird)
- Màu sắc lông/vảy/lông vũ: mô tả chi tiết các màu và họa tiết
- Đặc điểm nổi bật: tai/đuôi/mắt/mỏ/móng vuốt
- Tỷ lệ cơ thể: đầu:thân, chân dài/ngắn, đuôi dài/ngắn
- Tư thế và hành động đang làm

🏞️ BỐI CẢNH
- Địa điểm: trong nhà/ngoài trời, môi trường gì?
- Không gian: rộng/hẹp, kiến trúc/thiên nhiên
- Vật thể xung quanh quan trọng

📷 CAMERA & KỸ THUẬT
- Góc quay: eye-level/high-angle/low-angle/bird's-eye/worm's-eye
- Di chuyển: static/pan/tilt/zoom/dolly/tracking/handheld/crane
- Shot type: wide/full/medium/close-up/extreme close-up
- Độ sâu trường ảnh: shallow/deep DOF

💡 ÁNH SÁNG & MÀU SẮC
- Nguồn sáng: natural/artificial/mixed, hướng ánh sáng
- Chất lượng: soft/hard/dramatic/flat
- Color grading: warm/cool/neutral/vibrant/desaturated
- Bầu không khí: bright/moody/mysterious/romantic

🎨 COMPOSITION
- Quy tắc: rule of thirds/golden ratio/symmetry/leading lines
- Cân bằng: balanced/asymmetrical
- Layers: foreground/middle/background elements
- Depth: perspective và độ sâu không gian

😊 CẢM XÚC & MOOD
- Tâm trạng tổng thể của scene
- Cảm giác mà scene gợi lên

Trả lời TIẾNG VIỆT, chi tiết, chính xác, dựa trên những gì nhìn thấy."""
        }]

        # Add frames
        for frame_path in frames:
            try:
                base64_img = self._encode_image_base64(frame_path)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_img}",
                        "detail": "high"
                    }
                })
            except:
                continue

        # Call API với max_tokens cao hơn
        analysis = self._call_vision_api_with_retry([{"role": "user", "content": content}], max_tokens=2500)

        if not analysis:
            return None

        # Visual composition
        visual = self._analyze_visual_composition(frames[0])

        return {
            'scene_id': scene_id,
            'analysis': analysis,
            'visual_composition': visual,
            'duration': scene['duration'],
            'timestamp': f"{scene['start_time']:.1f}s - {scene['end_time']:.1f}s"
        }

    def _analyze_overall(self, scene_analyses: List[Dict], transcript: Optional[Dict]) -> Optional[str]:
        """Phân tích tổng thể video - CẢI TIẾN"""
        print_progress("Đang tổng hợp phân tích tổng thể...")

        # Prepare scene summaries
        scene_text = "\n\n".join([
            f"SCENE {s['scene_id'] + 1} ({s['timestamp']}):\n{s['analysis']}"
            for s in scene_analyses if s
        ])

        # Transcript
        transcript_text = ""
        if transcript:
            transcript_text = f"\n\nTRANSCRIPT:\n{transcript.get('text', '')}"

        # Metadata
        metadata_text = ""
        if self.video_metadata:
            metadata_text = f"\nThời lượng: {self.video_metadata.get('duration', 0)}s"

        prompt = f"""Dựa trên phân tích chi tiết từng scene và transcript, viết tổng hợp phân tích video:

VIDEO METADATA:{metadata_text}

PHÂN TÍCH TỪNG SCENE:
{scene_text}
{transcript_text}

Hãy viết phân tích tổng thể bao gồm:

1. TÓM TẮT NỘI DUNG
- Cốt truyện chính, diễn biến
- Thông điệp/chủ đề

2. NHÂN VẬT CHI TIẾT (nếu có)
- Tổng hợp tất cả nhân vật xuất hiện
- Mô tả ngoại hình, trang phục, đặc điểm của từng người
- Tỷ lệ cơ thể, màu sắc, phong cách
- Vai trò và hành động

3. CON VẬT CHI TIẾT (nếu có)
- Tổng hợp tất cả con vật
- Loài, kích thước, màu sắc, đặc điểm
- Tỷ lệ cơ thể, hành vi

4. PHONG CÁCH HÌNH ẢNH
- Visual style tổng thể
- Màu sắc chủ đạo
- Lighting approach
- Composition patterns

5. KỸ THUẬT QUAY
- Camera movements chính
- Shot types sử dụng
- Transitions giữa scenes
- Tempo và rhythm

6. KHÔNG KHÍ & CẢM XÚC
- Mood tổng thể
- Tone (dramatic/comedic/serious/etc.)
- Emotional arc

7. THỂ LOẠI & PHONG CÁCH
- Documentary/Narrative/Music Video/Commercial/Tutorial/etc.
- Reference style (cinematic/documentary/social media/etc.)

8. ĐẶC ĐIỂM NỔI BẬT
- Điểm đặc biệt, unique elements
- Techniques đáng chú ý
- Visual motifs

Trả lời chi tiết, có cấu trúc, TIẾNG VIỆT."""

        return self._call_vision_api_with_retry(
            [{"role": "user", "content": prompt}],
            max_tokens=3000
        )

    def _generate_prompts(self, overall_analysis: str, scene_analyses: List[Dict]) -> Optional[str]:
        """Tạo Sora prompts - CẢI TIẾN"""
        print_progress("Đang tạo Sora 2 prompts với mô tả chi tiết...")

        # Scene summaries - lấy nhiều scenes hơn
        scene_text = "\n".join([
            f"Scene {s['scene_id'] + 1}: {s['analysis'][:400]}..."
            for s in scene_analyses[:10] if s  # Tăng từ 5 lên 10 scenes
        ])

        prompt = f"""Dựa trên phân tích chi tiết video, tạo 3 PROMPT cho Sora 2:

PHÂN TÍCH TỔNG THỂ:
{overall_analysis}

CÁC SCENE CHI TIẾT:
{scene_text}

Tạo 3 prompts:

1. **SHORT PROMPT** (60-80 words): Súc tích nhưng có detail quan trọng

2. **DETAILED PROMPT** (150-200 words):
   - Mô tả CHÍNH XÁC nhân vật (chiều cao, body type, màu da, tóc, quần áo, tỷ lệ)
   - Mô tả CHÍNH XÁC con vật (loài, size, màu sắc, proportions)
   - Camera movement và angles cụ thể
   - Lighting setup chi tiết
   - Environment và atmosphere
   - Action và movement

3. **CINEMATIC PROMPT** (120-160 words):
   - Nghệ thuật, metaphor
   - Film references nếu phù hợp
   - Emotional tone
   - Artistic techniques
   - Chi tiết visual composition

YÊU CẦU QUAN TRỌNG:
✅ TẤT CẢ BẰNG TIẾNG ANH
✅ Mô tả nhân vật/con vật PHẢI cực kỳ chi tiết: height, build, skin tone, hair (color/style/length), clothing (color/style/fit), proportions
✅ Camera: cụ thể movement type (dolly/crane/steadicam/handheld)
✅ Lighting: cụ thể (soft key light, rim light, practical lights, etc.)
✅ Rõ ràng, sinh động, có thể visualize được
✅ Không giải thích, CHỈ viết prompts

Format:
=== SHORT PROMPT ===
[prompt here]

=== DETAILED PROMPT ===
[prompt here]

=== CINEMATIC PROMPT ===
[prompt here]"""

        return self._call_vision_api_with_retry(
            [{"role": "user", "content": prompt}],
            max_tokens=2000
        )

    # ========== EXPORT ==========

    def _save_results(self, overall: str, scenes: List[Dict], transcript: Optional[Dict], prompts: str) -> str:
        """Lưu kết quả ra files"""
        try:
            # Safe filename
            safe_title = "".join(c for c in self.video_title if c.isalnum() or c in (' ', '_', '-'))[:50]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{safe_title}_{timestamp}"

            # ========== TXT FILE ==========
            txt_path = f"{Config.OUTPUT_DIR}/{filename}.txt"

            scene_details = "\n\n".join([
                f"""{'='*60}
SCENE {s['scene_id'] + 1} | {s['timestamp']} | {s['duration']:.1f}s
{'='*60}

{s['analysis']}

VISUAL METRICS:
- Brightness: {s.get('visual_composition', {}).get('brightness', 0):.1f}
- Contrast: {s.get('visual_composition', {}).get('contrast', 0):.1f}
- Color Mood: {s.get('visual_composition', {}).get('color_mood', 'N/A')}
"""
                for s in scenes if s
            ])

            transcript_section = ""
            if transcript:
                transcript_section = f"""
{'='*60}
TRANSCRIPT
{'='*60}
Language: {transcript.get('language', 'unknown')}

{transcript.get('text', '')}
"""

            txt_content = f"""{'='*70}
YOUTUBE TO SORA 2 - DETAILED ANALYSIS REPORT v2.1
{'='*70}

VIDEO: {self.video_title}
URL: {self.youtube_url}
DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {self.video_metadata.get('duration', 0)}s
Total Scenes Analyzed: {len(scenes)}

{'='*70}
OVERALL ANALYSIS
{'='*70}

{overall}

{'='*70}
SCENE-BY-SCENE ANALYSIS ({len(scenes)} scenes)
{'='*70}

{scene_details}
{transcript_section}

{'='*70}
SORA 2 PROMPTS (DETAILED CHARACTER & ANIMAL DESCRIPTIONS)
{'='*70}

{prompts}

{'='*70}
Generated by YouTube to Sora 2 Analyzer v2.1
Features: Unlimited scenes, detailed character/animal analysis
{'='*70}
"""

            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(txt_content)

            print_success(f"Đã lưu TXT: {txt_path}")

            # ========== JSON FILE ==========
            json_path = f"{Config.OUTPUT_DIR}/{filename}.json"
            json_data = {
                'video_info': {
                    'title': self.video_title,
                    'url': self.youtube_url,
                    'metadata': self.video_metadata,
                    'date': datetime.now().isoformat(),
                    'total_scenes': len(scenes)
                },
                'overall_analysis': overall,
                'scenes': scenes,
                'transcript': transcript,
                'sora_prompts': prompts,
                'version': '2.1',
                'features': ['unlimited_scenes', 'detailed_character_analysis', 'detailed_animal_analysis']
            }

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            print_success(f"Đã lưu JSON: {json_path}")

            # ========== MARKDOWN FILE ==========
            md_path = f"{Config.OUTPUT_DIR}/{filename}.md"
            md_content = f"""# YouTube to Sora 2 - Analysis Report

**Version:** 2.1 (Detailed Character & Animal Analysis)
**Video:** {self.video_title}
**URL:** {self.youtube_url}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Duration:** {self.video_metadata.get('duration', 0)}s
**Total Scenes:** {len(scenes)}

---

## 📊 Overall Analysis

{overall}

---

## 🎬 Scene-by-Scene Breakdown

"""
            for s in scenes:
                if s:
                    md_content += f"""### Scene {s['scene_id'] + 1} ({s['timestamp']}, {s['duration']:.1f}s)

{s['analysis']}

**Visual Metrics:**
- Brightness: {s.get('visual_composition', {}).get('brightness', 0):.1f}
- Contrast: {s.get('visual_composition', {}).get('contrast', 0):.1f}
- Color Mood: {s.get('visual_composition', {}).get('color_mood', 'N/A')}

---

"""

            if transcript:
                md_content += f"""## 🎤 Transcript

**Language:** {transcript.get('language', 'unknown')}

{transcript.get('text', '')}

---

"""

            md_content += f"""## 🎨 Sora 2 Prompts

{prompts}

---

*Generated by YouTube to Sora 2 Analyzer v2.1*
*Features: Unlimited scenes analysis, detailed character/animal descriptions, body proportions, color details*
"""

            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)

            print_success(f"Đã lưu Markdown: {md_path}")

            return txt_path

        except Exception as e:
            print_error(f"Lỗi lưu file: {e}")
            return ""

    # ========== MAIN PROCESS ==========

    def analyze(self, youtube_url: str, use_cache: bool = True, analyze_audio: bool = True) -> Optional[Dict]:
        """
        Phân tích video YouTube và tạo Sora prompts

        Args:
            youtube_url: URL của video YouTube
            use_cache: Sử dụng cache nếu có
            analyze_audio: Phân tích audio/transcript

        Returns:
            Dict chứa kết quả phân tích hoặc None nếu thất bại
        """
        self.youtube_url = youtube_url

        print_header("YOUTUBE TO SORA 2 - ADVANCED ANALYZER v2.1")
        print("✨ Features: Unlimited scenes, detailed character & animal analysis")

        # Check cache
        cache_key = self._get_cache_key(youtube_url)
        if use_cache:
            cached = self._load_cache(cache_key)
            if cached:
                print_success("Tìm thấy kết quả trong cache!")
                self.video_title = cached.get('video_info', {}).get('title', '')
                print(f"Video: {self.video_title}\n")

                print_section("PHÂN TÍCH TỔNG THỂ (từ cache)")
                print(cached.get('overall_analysis', ''))

                print_section("SORA 2 PROMPTS (từ cache)")
                print(cached.get('sora_prompts', ''))

                return cached

        # Step 1: Get metadata
        self._get_video_metadata(youtube_url)

        # Step 2: Download
        if not self._download_video(youtube_url):
            return None

        # Step 3: Scene detection
        if not self._detect_scenes():
            cleanup_temp_files()
            return None

        # Step 4: Extract frames
        if not self._extract_frames_from_scenes():
            cleanup_temp_files()
            return None

        # Step 5: Transcript (optional)
        transcript = None
        if analyze_audio:
            transcript = self._extract_transcript()

        # Step 6: Analyze scenes
        print_section(f"PHÂN TÍCH CHI TIẾT {len(self.scenes)} SCENES")
        scene_analyses = []
        for scene in self.scenes:
            result = self._analyze_scene(scene)
            if result:
                scene_analyses.append(result)
            # Small delay để tránh rate limit
            time.sleep(0.5)

        if not scene_analyses:
            print_error("Không thể phân tích scenes")
            cleanup_temp_files()
            return None

        print_success(f"Đã phân tích xong {len(scene_analyses)} scenes!")

        # Step 7: Overall analysis
        print_section("PHÂN TÍCH TỔNG THỂ")
        overall = self._analyze_overall(scene_analyses, transcript)

        if overall:
            print(overall)
        else:
            cleanup_temp_files()
            return None

        # Step 8: Generate prompts
        print_section("TẠO SORA 2 PROMPTS")
        prompts = self._generate_prompts(overall, scene_analyses)

        if prompts:
            print(prompts)
        else:
            cleanup_temp_files()
            return None

        # Step 9: Save results
        print_section("LƯU KẾT QUẢ")
        self._save_results(overall, scene_analyses, transcript, prompts)

        # Save cache
        if use_cache:
            cache_data = {
                'video_info': {
                    'title': self.video_title,
                    'url': self.youtube_url,
                    'metadata': self.video_metadata,
                    'total_scenes': len(scene_analyses)
                },
                'overall_analysis': overall,
                'scene_analyses': scene_analyses,
                'transcript': transcript,
                'sora_prompts': prompts,
                'version': '2.1'
            }
            self._save_cache(cache_key, cache_data)
            print_success("Đã lưu vào cache")

        # Cleanup
        cleanup_temp_files()

        print_header("✓ HOÀN TẤT!")
        print(f"📁 Kết quả đã lưu trong folder: {Config.OUTPUT_DIR}/")
        print(f"📊 Đã phân tích {len(scene_analyses)} scenes với mô tả chi tiết nhân vật & con vật\n")

        return {
            'overall_analysis': overall,
            'scene_analyses': scene_analyses,
            'transcript': transcript,
            'sora_prompts': prompts
        }


# ========== CLI ==========

def main():
    """Main CLI interface"""
    print_header("YOUTUBE TO SORA 2 - ADVANCED ANALYZER v2.1")
    print("✨ Không giới hạn scenes")
    print("✨ Phân tích chi tiết nhân vật: chiều cao, cân nặng, màu da, tóc, trang phục")
    print("✨ Phân tích chi tiết con vật: loài, kích thước, màu sắc, tỷ lệ cơ thể\n")

    # Input URL
    youtube_url = input("Nhập YouTube URL: ").strip()
    if not youtube_url:
        print_error("URL không hợp lệ")
        return

    # Check API key
    load_env_file()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        api_key = input("Nhập OpenAI API Key: ").strip()
        if not api_key:
            print_error("Cần OpenAI API Key")
            print("\nCách lấy API key:")
            print("1. Vào https://platform.openai.com/api-keys")
            print("2. Tạo key mới")
            print("3. Lưu vào file .env hoặc nhập trực tiếp")
            return

    # Options
    print("\n--- TÙY CHỌN ---")
    use_cache = input("Sử dụng cache? (y/n, mặc định: y): ").strip().lower() != 'n'
    analyze_audio = input("Phân tích audio? (y/n, mặc định: y): ").strip().lower() != 'n'

    # Process
    try:
        analyzer = YouTubeToSoraAnalyzer(api_key=api_key)
        result = analyzer.analyze(
            youtube_url=youtube_url,
            use_cache=use_cache,
            analyze_audio=analyze_audio
        )

        if result:
            print_success("Phân tích thành công!")
            print(f"\n📊 Thống kê:")
            print(f"  - Tổng scenes: {len(result['scene_analyses'])}")
            print(f"  - Transcript: {'Có' if result['transcript'] else 'Không'}")
        else:
            print_error("Có lỗi xảy ra")

    except KeyboardInterrupt:
        print("\n\n⚠ Đã dừng bởi người dùng")
        cleanup_temp_files()
    except Exception as e:
        print_error(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()
        cleanup_temp_files()


if __name__ == "__main__":
    main()
