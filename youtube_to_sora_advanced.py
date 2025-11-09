#!/usr/bin/env python3
"""
YouTube to Sora 2 - Advanced Video Analyzer
Phân tích video YouTube chi tiết và tạo prompts cho Sora 2

Version: 2.1
Author: Claude AI
License: MIT
"""

import os
import sys
import json
import time
import hashlib
import shutil
import subprocess
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

import cv2
import numpy as np
from openai import OpenAI


# ========================================
# CONFIGURATION
# ========================================

class Config:
    """Cấu hình chung cho analyzer"""

    # Scene detection
    SCENE_THRESHOLD = 30.0
    MIN_SCENE_LENGTH = 15
    FRAMES_PER_SCENE = 3
    MAX_SCENES = 20

    # Video settings
    MAX_VIDEO_HEIGHT = 1080
    VIDEO_TIMEOUT = 300

    # API settings
    MODEL_VISION = "gpt-4o"
    MODEL_TEXT = "gpt-4o"
    MODEL_WHISPER = "whisper-1"
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    # Directories
    DIR_CACHE = "cache"
    DIR_OUTPUT = "output_results"
    DIR_TEMP_FRAMES = "temp_frames"

    # Files
    FILE_TEMP_VIDEO = "temp_video.mp4"
    FILE_TEMP_AUDIO = "temp_audio.m4a"


# ========================================
# UTILITIES
# ========================================

def load_env_file() -> None:
    """Load .env file nếu tồn tại"""
    env_path = Path('.env')
    if not env_path.exists():
        return

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue

                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ[key] = value
    except Exception as e:
        print(f"⚠ Không thể đọc .env: {e}")


def setup_directories() -> None:
    """Tạo các thư mục cần thiết"""
    for dir_name in [Config.DIR_CACHE, Config.DIR_OUTPUT, Config.DIR_TEMP_FRAMES]:
        Path(dir_name).mkdir(exist_ok=True)


def cleanup_temp_files() -> None:
    """Xóa tất cả temp files"""
    # Xóa video/audio files
    for file in [Config.FILE_TEMP_VIDEO, Config.FILE_TEMP_AUDIO]:
        if os.path.exists(file):
            try:
                os.remove(file)
            except:
                pass

    # Xóa frames
    if os.path.exists(Config.DIR_TEMP_FRAMES):
        try:
            shutil.rmtree(Config.DIR_TEMP_FRAMES)
            Path(Config.DIR_TEMP_FRAMES).mkdir(exist_ok=True)
        except:
            pass


def print_header(text: str) -> None:
    """In header"""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")


def print_section(text: str) -> None:
    """In section"""
    print("\n" + "-"*70)
    print(text)
    print("-"*70)


def print_step(message: str, step: Optional[int] = None, total: Optional[int] = None) -> None:
    """In bước tiến trình"""
    if step and total:
        print(f"[{step}/{total}] {message}")
    else:
        print(f"• {message}")


def print_ok(message: str) -> None:
    """In thành công"""
    print(f"✓ {message}")


def print_err(message: str) -> None:
    """In lỗi"""
    print(f"✗ {message}")


def print_warn(message: str) -> None:
    """In cảnh báo"""
    print(f"⚠ {message}")


# ========================================
# MAIN ANALYZER CLASS
# ========================================

class SoraAnalyzer:
    """YouTube to Sora 2 Video Analyzer"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Khởi tạo analyzer

        Args:
            api_key: OpenAI API key (optional)
        """
        # Load environment
        load_env_file()

        # Setup API key
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        final_key = os.getenv("OPENAI_API_KEY")
        if not final_key:
            raise ValueError(
                "❌ Không tìm thấy OpenAI API key!\n\n"
                "Cách khắc phục:\n"
                "1. Tạo file .env với nội dung: OPENAI_API_KEY=sk-your-key\n"
                "2. Hoặc: set OPENAI_API_KEY=sk-your-key (Windows)\n"
                "3. Hoặc: export OPENAI_API_KEY=sk-your-key (Linux/Mac)\n"
            )

        # Initialize OpenAI client
        try:
            self.client = OpenAI(api_key=final_key)
        except Exception as e:
            raise ValueError(f"❌ Không thể khởi tạo OpenAI: {e}")

        # Setup
        setup_directories()

        # State
        self.url: str = ""
        self.title: str = ""
        self.metadata: Dict = {}
        self.scenes: List[Dict] = []

    # ========== CACHE ==========

    def _cache_key(self, url: str) -> str:
        """Tạo cache key"""
        return hashlib.md5(url.encode()).hexdigest()

    def _cache_save(self, key: str, data: Dict) -> None:
        """Lưu cache"""
        try:
            path = Path(Config.DIR_CACHE) / f"{key}.json"
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print_warn(f"Không lưu được cache: {e}")

    def _cache_load(self, key: str) -> Optional[Dict]:
        """Load cache"""
        try:
            path = Path(Config.DIR_CACHE) / f"{key}.json"
            if not path.exists():
                return None

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # VALIDATE CACHE - quan trọng!
            if not isinstance(data, dict):
                return None

            # Phải có đủ keys
            required = ['video_info', 'overall_analysis', 'sora_prompts']
            if not all(k in data for k in required):
                return None

            # Phải có giá trị, không được None hoặc rỗng
            overall = data.get('overall_analysis')
            prompts = data.get('sora_prompts')

            if not overall or not prompts:
                return None

            if overall == "None" or prompts == "None":
                return None

            return data

        except Exception as e:
            print_warn(f"Không đọc được cache: {e}")
            return None

    # ========== VIDEO DOWNLOAD ==========

    def _get_metadata(self, url: str) -> Dict:
        """Lấy metadata từ YouTube"""
        print_step("Đang lấy thông tin video...")

        try:
            result = subprocess.run(
                ["yt-dlp", "--dump-json", url],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                meta = json.loads(result.stdout)
                self.title = meta.get('title', 'Unknown')
                self.metadata = {
                    'title': meta.get('title'),
                    'duration': meta.get('duration', 0),
                    'uploader': meta.get('uploader'),
                    'width': meta.get('width'),
                    'height': meta.get('height'),
                    'fps': meta.get('fps'),
                }
                print_ok(f"Video: {self.title}")
                return self.metadata
        except Exception as e:
            print_err(f"Lỗi lấy metadata: {e}")

        # Fallback
        self.title = f"Video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return {}

    def _download(self, url: str) -> bool:
        """Download video và audio"""
        print_step("Đang tải video...")

        try:
            # Download video
            result = subprocess.run(
                [
                    "yt-dlp",
                    "-f", f"best[height<={Config.MAX_VIDEO_HEIGHT}][ext=mp4]",
                    "-o", Config.FILE_TEMP_VIDEO,
                    url
                ],
                capture_output=True,
                text=True,
                timeout=Config.VIDEO_TIMEOUT
            )

            if result.returncode != 0:
                print_err(f"Lỗi tải video: {result.stderr[:200]}")
                return False

            print_ok("Video đã tải xong")

            # Download audio (for transcript)
            try:
                subprocess.run(
                    ["yt-dlp", "-f", "bestaudio[ext=m4a]", "-o", Config.FILE_TEMP_AUDIO, url],
                    capture_output=True,
                    timeout=60
                )
                if os.path.exists(Config.FILE_TEMP_AUDIO):
                    print_ok("Audio đã tải xong")
            except:
                print_warn("Không tải được audio (bỏ qua)")

            return True

        except subprocess.TimeoutExpired:
            print_err("Timeout khi tải video")
            return False
        except Exception as e:
            print_err(f"Lỗi: {e}")
            return False

    # ========== SCENE DETECTION ==========

    def _detect_scenes(self) -> bool:
        """Phát hiện scenes"""
        if not os.path.exists(Config.FILE_TEMP_VIDEO):
            return False

        print_step("Đang phát hiện scenes...")

        try:
            cap = cv2.VideoCapture(Config.FILE_TEMP_VIDEO)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if total == 0:
                print_err("Không đọc được video")
                return False

            prev = None
            boundaries = [0]
            idx = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                small = cv2.resize(frame, (320, 180))
                gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

                if prev is not None:
                    diff = cv2.absdiff(gray, prev)
                    mean_diff = np.mean(diff)

                    if mean_diff > Config.SCENE_THRESHOLD:
                        if idx - boundaries[-1] > Config.MIN_SCENE_LENGTH:
                            boundaries.append(idx)

                prev = gray
                idx += 1

                if idx % 100 == 0:
                    pct = (idx / total) * 100
                    print(f"\r  Đang xử lý: {pct:.1f}%", end='', flush=True)

            print()
            boundaries.append(total - 1)
            cap.release()

            # Tạo scene list
            scenes = []
            for i in range(len(boundaries) - 1):
                start = boundaries[i]
                end = boundaries[i + 1]
                scenes.append({
                    'id': i,
                    'start_frame': start,
                    'end_frame': end,
                    'start_time': start / fps,
                    'end_time': end / fps,
                    'duration': (end - start) / fps,
                    'frames': []
                })

            # Giới hạn scenes
            if len(scenes) > Config.MAX_SCENES:
                print_warn(f"Video có {len(scenes)} scenes, chỉ phân tích {Config.MAX_SCENES} đầu")
                scenes = scenes[:Config.MAX_SCENES]

            self.scenes = scenes
            print_ok(f"Đã phát hiện {len(scenes)} scenes")
            return True

        except Exception as e:
            print_err(f"Lỗi: {e}")
            return False

    def _extract_frames(self) -> bool:
        """Trích xuất frames từ scenes"""
        if not self.scenes:
            return False

        print_step("Đang trích xuất frames...")

        try:
            cap = cv2.VideoCapture(Config.FILE_TEMP_VIDEO)

            for scene in self.scenes:
                positions = np.linspace(
                    scene['start_frame'],
                    scene['end_frame'],
                    Config.FRAMES_PER_SCENE,
                    dtype=int
                )

                for pos in positions:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
                    ret, frame = cap.read()

                    if ret:
                        path = f"{Config.DIR_TEMP_FRAMES}/scene_{scene['id']}_frame_{len(scene['frames'])}.jpg"
                        cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                        scene['frames'].append(path)

            cap.release()
            total = sum(len(s['frames']) for s in self.scenes)
            print_ok(f"Đã trích xuất {total} frames")
            return True

        except Exception as e:
            print_err(f"Lỗi: {e}")
            return False

    # ========== AUDIO ==========

    def _extract_transcript(self) -> Optional[str]:
        """Trích xuất transcript"""
        if not os.path.exists(Config.FILE_TEMP_AUDIO):
            return None

        print_step("Đang phân tích audio...")

        try:
            with open(Config.FILE_TEMP_AUDIO, "rb") as f:
                result = self.client.audio.transcriptions.create(
                    model=Config.MODEL_WHISPER,
                    file=f,
                    response_format="text"
                )

            text = str(result).strip()
            if text:
                print_ok(f"Transcript: {len(text)} ký tự")
                return text

        except Exception as e:
            print_warn(f"Không trích xuất được transcript: {e}")

        return None

    # ========== AI ANALYSIS ==========

    def _call_api(self, messages: List[Dict], max_tokens: int = 1500) -> Optional[str]:
        """Gọi API với retry"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=Config.MODEL_VISION,
                    max_tokens=max_tokens,
                    messages=messages
                )
                return response.choices[0].message.content

            except Exception as e:
                if attempt < Config.MAX_RETRIES - 1:
                    delay = Config.RETRY_DELAY * (attempt + 1)
                    print_warn(f"API lỗi (lần {attempt+1}/{Config.MAX_RETRIES}), thử lại sau {delay}s...")
                    time.sleep(delay)
                else:
                    print_err(f"API lỗi sau {Config.MAX_RETRIES} lần: {e}")
                    return None

        return None

    def _encode_image(self, path: str) -> str:
        """Encode image to base64"""
        with open(path, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8")

    def _analyze_scene(self, scene: Dict) -> Optional[str]:
        """Phân tích 1 scene"""
        if not scene['frames']:
            return None

        sid = scene['id']
        print_step(f"Phân tích scene {sid+1}...", sid+1, len(self.scenes))

        content = [{
            "type": "text",
            "text": f"""Phân tích scene này ({scene['duration']:.1f}s):

1. HÀNH ĐỘNG: Gì đang xảy ra?
2. NHÂN VẬT: Ai/cái gì?
3. CẢM XÚC: Tâm trạng?
4. BỐI CẢNH: Địa điểm?
5. CAMERA: Di chuyển? (static/pan/zoom/tracking)
6. ÁNH SÁNG: Loại ánh sáng?
7. MÀU SẮC: Tông màu chủ đạo?

Trả lời ngắn gọn, tiếng Việt."""
        }]

        # Add images
        for frame in scene['frames']:
            try:
                b64 = self._encode_image(frame)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64}",
                        "detail": "high"
                    }
                })
            except:
                continue

        return self._call_api([{"role": "user", "content": content}])

    def _analyze_overall(self, scene_texts: List[str], transcript: Optional[str]) -> Optional[str]:
        """Phân tích tổng thể"""
        print_step("Tổng hợp phân tích...")

        scenes_summary = "\n\n".join([
            f"SCENE {i+1}:\n{text}"
            for i, text in enumerate(scene_texts)
        ])

        transcript_part = ""
        if transcript:
            transcript_part = f"\n\nTRANSCRIPT:\n{transcript[:1000]}"

        prompt = f"""Dựa trên phân tích scenes, viết tổng hợp:

{scenes_summary}
{transcript_part}

Viết phân tích gồm:
1. TÓM TẮT: Nội dung chính
2. HÌNH ẢNH: Visual style, màu sắc, lighting
3. CAMERA: Techniques, movements
4. KHÔNG KHÍ: Mood tổng thể
5. THỂ LOẠI: Documentary/Narrative/etc.

Tiếng Việt, chi tiết."""

        return self._call_api([{"role": "user", "content": prompt}], max_tokens=2000)

    def _generate_prompts(self, overall: str, scene_texts: List[str]) -> Optional[str]:
        """Tạo Sora prompts"""
        print_step("Tạo Sora prompts...")

        scenes_brief = "\n".join([
            f"Scene {i+1}: {text[:150]}..."
            for i, text in enumerate(scene_texts[:5])
        ])

        prompt = f"""Tạo 3 PROMPT cho Sora 2:

TỔNG THỂ:
{overall[:800]}

SCENES:
{scenes_brief}

Tạo 3 prompts (TIẾNG ANH):

1. SHORT (50-70 từ): Súc tích
2. DETAILED (120-150 từ): Đầy đủ
3. CREATIVE (100-130 từ): Nghệ thuật

Format:
=== SHORT PROMPT ===
[prompt]

=== DETAILED PROMPT ===
[prompt]

=== CREATIVE PROMPT ===
[prompt]"""

        return self._call_api([{"role": "user", "content": prompt}], max_tokens=1500)

    # ========== EXPORT ==========

    def _save_results(self, overall: str, scenes: List[str], transcript: Optional[str], prompts: str) -> str:
        """Lưu kết quả"""
        try:
            safe_title = "".join(c for c in self.title if c.isalnum() or c in (' ', '_', '-'))[:50]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{safe_title}_{timestamp}"

            # TXT
            txt_path = f"{Config.DIR_OUTPUT}/{filename}.txt"

            scenes_text = "\n\n".join([
                f"{'='*60}\nSCENE {i+1}\n{'='*60}\n\n{text}"
                for i, text in enumerate(scenes)
            ])

            transcript_text = ""
            if transcript:
                transcript_text = f"\n\n{'='*60}\nTRANSCRIPT\n{'='*60}\n\n{transcript}"

            content = f"""{'='*70}
YOUTUBE TO SORA 2 - ANALYSIS REPORT
{'='*70}

VIDEO: {self.title}
URL: {self.url}
DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*70}
PHÂN TÍCH TỔNG THỂ
{'='*70}

{overall}

{'='*70}
PHÂN TÍCH SCENES
{'='*70}

{scenes_text}
{transcript_text}

{'='*70}
SORA 2 PROMPTS
{'='*70}

{prompts}

{'='*70}
"""

            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print_ok(f"Đã lưu: {txt_path}")

            # JSON
            json_path = f"{Config.DIR_OUTPUT}/{filename}.json"
            json_data = {
                'video_info': {
                    'title': self.title,
                    'url': self.url,
                    'metadata': self.metadata,
                    'date': datetime.now().isoformat()
                },
                'overall_analysis': overall,
                'scene_analyses': scenes,
                'transcript': transcript,
                'sora_prompts': prompts
            }

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            print_ok(f"Đã lưu: {json_path}")

            return txt_path

        except Exception as e:
            print_err(f"Lỗi lưu file: {e}")
            return ""

    # ========== MAIN ==========

    def analyze(self, url: str, use_cache: bool = True, analyze_audio: bool = True) -> Optional[Dict]:
        """
        Phân tích video

        Args:
            url: YouTube URL
            use_cache: Dùng cache?
            analyze_audio: Phân tích audio?

        Returns:
            Dict kết quả hoặc None nếu lỗi
        """
        self.url = url

        print_header("YOUTUBE TO SORA 2 - ANALYZER")

        # Check cache
        cache_key = self._cache_key(url)
        if use_cache:
            cached = self._cache_load(cache_key)
            if cached:
                print_ok("Tìm thấy cache hợp lệ!")
                self.title = cached['video_info']['title']
                print(f"Video: {self.title}\n")

                print_section("PHÂN TÍCH TỔNG THỂ")
                print(cached['overall_analysis'])

                print_section("SORA 2 PROMPTS")
                print(cached['sora_prompts'])

                return cached

        # Download
        self._get_metadata(url)
        if not self._download(url):
            cleanup_temp_files()
            return None

        # Scenes
        if not self._detect_scenes():
            cleanup_temp_files()
            return None

        if not self._extract_frames():
            cleanup_temp_files()
            return None

        # Transcript
        transcript = None
        if analyze_audio:
            transcript = self._extract_transcript()

        # Analyze scenes
        print_section("PHÂN TÍCH SCENES")
        scene_texts = []
        for scene in self.scenes:
            text = self._analyze_scene(scene)
            if text:
                scene_texts.append(text)

        if not scene_texts:
            print_err("Không phân tích được scenes")
            cleanup_temp_files()
            return None

        # Overall
        print_section("TỔNG HỢP")
        overall = self._analyze_overall(scene_texts, transcript)
        if overall:
            print(overall)
        else:
            cleanup_temp_files()
            return None

        # Prompts
        print_section("TẠO PROMPTS")
        prompts = self._generate_prompts(overall, scene_texts)
        if prompts:
            print(prompts)
        else:
            cleanup_temp_files()
            return None

        # Save
        print_section("LƯU KẾT QUẢ")
        self._save_results(overall, scene_texts, transcript, prompts)

        # Cache
        if use_cache:
            cache_data = {
                'video_info': {
                    'title': self.title,
                    'url': self.url,
                    'metadata': self.metadata
                },
                'overall_analysis': overall,
                'scene_analyses': scene_texts,
                'transcript': transcript,
                'sora_prompts': prompts
            }
            self._cache_save(cache_key, cache_data)
            print_ok("Đã lưu cache")

        # Cleanup
        cleanup_temp_files()

        print_header("✓ HOÀN TẤT!")
        print(f"Kết quả: {Config.DIR_OUTPUT}/\n")

        return {
            'overall_analysis': overall,
            'scene_analyses': scene_texts,
            'transcript': transcript,
            'sora_prompts': prompts
        }


# ========================================
# CLI
# ========================================

def main():
    """CLI interface"""
    print_header("YOUTUBE TO SORA 2 - ANALYZER")

    # URL
    url = input("YouTube URL: ").strip()
    if not url:
        print_err("URL không hợp lệ")
        return

    # API key
    load_env_file()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        api_key = input("OpenAI API Key: ").strip()
        if not api_key:
            print_err("Cần API key")
            print("\nLấy tại: https://platform.openai.com/api-keys")
            return

    # Options
    print("\n--- TÙY CHỌN ---")
    use_cache = input("Dùng cache? (y/n, mặc định y): ").strip().lower() != 'n'
    analyze_audio = input("Phân tích audio? (y/n, mặc định y): ").strip().lower() != 'n'

    # Run
    try:
        analyzer = SoraAnalyzer(api_key=api_key)
        result = analyzer.analyze(url, use_cache=use_cache, analyze_audio=analyze_audio)

        if result:
            print_ok("Thành công!")
        else:
            print_err("Có lỗi xảy ra")

    except KeyboardInterrupt:
        print("\n\n⚠ Đã hủy")
    except Exception as e:
        print_err(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
