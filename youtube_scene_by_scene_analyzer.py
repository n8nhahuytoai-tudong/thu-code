#!/usr/bin/env python3
"""
YouTube Scene-by-Scene Analyzer - Per-Scene Prompt Generator
Phân tích từng cảnh riêng biệt và tạo prompt chi tiết cho mỗi cảnh

Features:
- Xuất ảnh đầu + ảnh cuối cho mỗi cảnh
- Tạo prompt cinema chi tiết riêng cho MỖI cảnh
- Export organized by scenes
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
from typing import List, Dict, Optional
import shutil

# ========== CONFIGURATION ==========

class Config:
    """Cấu hình"""
    SCENE_THRESHOLD = 30.0
    MIN_SCENE_LENGTH = 15
    MAX_VIDEO_HEIGHT = 1080

    VISION_MODEL = "gpt-4o"
    WHISPER_MODEL = "whisper-1"
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    CACHE_DIR = "cache"
    OUTPUT_DIR = "output_scenes"
    TEMP_FRAMES_DIR = "temp_frames"

    MAX_SCENES_TO_ANALYZE = 999

# ========== UTILITIES ==========

def load_env_file():
    """Load .env file"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key, value = key.strip(), value.strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key] = value

def ensure_directories():
    """Tạo thư mục"""
    for d in [Config.CACHE_DIR, Config.OUTPUT_DIR, Config.TEMP_FRAMES_DIR]:
        Path(d).mkdir(exist_ok=True)

def cleanup_temp():
    """Xóa temp files"""
    for f in ["temp_video.mp4", "temp_audio.m4a"]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass
    if os.path.exists(Config.TEMP_FRAMES_DIR):
        try:
            shutil.rmtree(Config.TEMP_FRAMES_DIR)
            Path(Config.TEMP_FRAMES_DIR).mkdir(exist_ok=True)
        except:
            pass

def print_header(text: str):
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")

def print_progress(msg: str, step: int = None, total: int = None):
    if step and total:
        print(f"[{step}/{total}] {msg}")
    else:
        print(f"• {msg}")

def print_success(msg: str):
    print(f"✓ {msg}")

def print_error(msg: str):
    print(f"✗ {msg}")

# ========== MAIN ANALYZER ==========

class SceneBySceneAnalyzer:
    """Phân tích từng cảnh riêng biệt"""

    SCENE_PROMPT_TEMPLATE = """Phân tích scene này ({duration:.1f}s) và tạo MỘT PROMPT DUY NHẤT cho Sora 2 theo TIÊU CHUẨN HOLLYWOOD CINEMA.

Bạn đang xem 2 frames: FRAME ĐẦU và FRAME CUỐI của scene này.

Tạo prompt TIẾNG ANH, chi tiết, 150-200 words, bao gồm:

📹 CAMERA & COMPOSITION:
- Shot type & size (wide/medium/close-up/etc)
- Camera movement (static/pan/tilt/dolly/tracking/crane/steadicam/handheld)
- Camera angle (eye-level/high/low/dutch/overhead)
- Lens focal length estimate (18mm/35mm/50mm/85mm/100mm+)
- Aperture & DOF (shallow f/1.4-2.8 / deep f/8-16)
- Composition (rule of thirds/centered/symmetrical)
- Aspect ratio (16:9/2.39:1/1.85:1)

👥 CHARACTERS (nếu có):
- Physical: gender, age estimate, height (~cm), build (slim/athletic/muscular/heavy), weight estimate
- Skin tone: ivory/fair/tan/olive/bronze/brown/deep brown/ebony
- Hair: color (blonde/brown/black/red/gray), style (straight/wavy/curly/braided), length (short/medium/long)
- Facial features: angular/soft/chiseled/round, jawline, eyes, nose
- Costume: style, colors, materials, fit, accessories
- Action/performance: what they're doing, body language, expression

🐾 ANIMALS/CREATURES (nếu có):
- Species, breed, size (height/length/weight), coat color & pattern, features, movement

💡 LIGHTING:
- Setup type (3-point/natural/high-key/low-key/Rembrandt/butterfly)
- Key light position & quality (hard/soft)
- Fill ratio (high contrast/balanced)
- Color temperature (warm 3200K/neutral/cool 5600K)
- Practicals (visible light sources)
- Atmosphere (haze/fog/volumetric)

🎨 COLOR GRADING:
- Palette (warm/cool/complementary/monochromatic)
- LUT style (naturalistic/teal-orange/bleach bypass/noir)
- Saturation level (vibrant/muted/desaturated)
- Contrast & blacks (crushed/lifted/normal)

🏞️ ENVIRONMENT & PRODUCTION:
- Location type (interior/exterior/urban/nature)
- Set design & props
- Time of day & weather
- VFX elements (CGI/practical/none)

🎭 ACTION & STORY:
- What's happening in the scene
- Movement & pacing (slow/medium/fast)
- Emotional tone & mood
- Genre indicators

🎬 STYLE REFERENCE:
- Comparable to which film/director style
- Production value level (indie/studio/blockbuster)

CRITICAL REQUIREMENTS:
✅ Write in ENGLISH only
✅ Use professional cinema terminology
✅ Be SPECIFIC with numbers (heights in cm, focal lengths in mm, color temps in K)
✅ Describe visual evidence you see, not assumptions
✅ Create ONE continuous paragraph prompt (not bullet points)
✅ Focus on recreatable technical details for Sora 2
✅ 150-200 words total

Format your response as:
PROMPT: [your single-paragraph detailed prompt here]"""

    def __init__(self, api_key: Optional[str] = None):
        load_env_file()

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found!")

        self.client = OpenAI(api_key=api_key)
        ensure_directories()

        self.video_path: Optional[str] = None
        self.youtube_url: Optional[str] = None
        self.video_title: str = ""
        self.video_metadata: Dict = {}
        self.scenes: List[Dict] = []

    # ========== VIDEO DOWNLOAD ==========

    def _get_metadata(self, url: str) -> Dict:
        print_progress("Đang lấy metadata...")
        try:
            result = subprocess.run(
                ["yt-dlp", "--dump-json", url],
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
                    'width': metadata.get('width'),
                    'height': metadata.get('height'),
                    'fps': metadata.get('fps'),
                }
                print_success(f"Video: {self.video_title}")
                return self.video_metadata
        except Exception as e:
            print_error(f"Lỗi metadata: {e}")

        self.video_title = f"Video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return {}

    def _download_video(self, url: str) -> bool:
        print_progress("Đang tải video...")
        try:
            result = subprocess.run(
                [
                    "yt-dlp",
                    "-f", f"best[height<={Config.MAX_VIDEO_HEIGHT}][ext=mp4]",
                    "-o", "temp_video.mp4",
                    url
                ],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode != 0:
                print_error(f"Lỗi tải video: {result.stderr}")
                return False

            self.video_path = "temp_video.mp4"
            print_success("Video đã tải xong")
            return True
        except Exception as e:
            print_error(f"Lỗi: {e}")
            return False

    # ========== SCENE DETECTION ==========

    def _detect_scenes(self) -> List[Dict]:
        if not self.video_path or not os.path.exists(self.video_path):
            return []

        print_progress("Đang phát hiện scenes...")

        try:
            cap = cv2.VideoCapture(self.video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if total_frames == 0:
                print_error("Không đọc được video")
                return []

            prev_frame = None
            scene_boundaries = [0]
            frame_idx = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                small = cv2.resize(frame, (320, 180))
                gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

                if prev_frame is not None:
                    diff = cv2.absdiff(gray, prev_frame)
                    mean_diff = np.mean(diff)

                    if mean_diff > Config.SCENE_THRESHOLD:
                        if frame_idx - scene_boundaries[-1] > Config.MIN_SCENE_LENGTH:
                            scene_boundaries.append(frame_idx)

                prev_frame = gray
                frame_idx += 1

                if frame_idx % 100 == 0:
                    progress = (frame_idx / total_frames) * 100
                    print(f"\r  Đang xử lý: {progress:.1f}%", end='', flush=True)

            print()
            scene_boundaries.append(total_frames - 1)
            cap.release()

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

            print_success(f"Đã phát hiện {len(scenes)} scenes")
            self.scenes = scenes
            return scenes

        except Exception as e:
            print_error(f"Lỗi phát hiện scenes: {e}")
            return []

    # ========== EXTRACT FIRST & LAST FRAMES ==========

    def _extract_first_last_frames(self) -> bool:
        """Trích xuất frame đầu và frame cuối của mỗi scene"""
        if not self.scenes or not self.video_path:
            return False

        print_progress(f"Đang trích xuất frame ĐẦU + CUỐI từ {len(self.scenes)} scenes...")

        try:
            cap = cv2.VideoCapture(self.video_path)

            for scene in self.scenes:
                scene_id = scene['scene_id']
                start_frame = scene['start_frame']
                end_frame = scene['end_frame']

                # Frame ĐẦU
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                ret, frame = cap.read()
                if ret:
                    first_path = f"{Config.TEMP_FRAMES_DIR}/scene_{scene_id:04d}_FIRST.jpg"
                    cv2.imwrite(first_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                    scene['frame_first'] = first_path

                # Frame CUỐI
                cap.set(cv2.CAP_PROP_POS_FRAMES, end_frame)
                ret, frame = cap.read()
                if ret:
                    last_path = f"{Config.TEMP_FRAMES_DIR}/scene_{scene_id:04d}_LAST.jpg"
                    cv2.imwrite(last_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                    scene['frame_last'] = last_path

            cap.release()
            print_success(f"Đã trích xuất {len(self.scenes) * 2} frames (đầu + cuối)")
            return True

        except Exception as e:
            print_error(f"Lỗi trích xuất frames: {e}")
            return False

    # ========== AI ANALYSIS ==========

    def _encode_image_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8")

    def _call_vision_api(self, messages: List[Dict], max_tokens: int = 500) -> Optional[str]:
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
                    print(f"  Retry {attempt + 1}...", end='', flush=True)
                    time.sleep(Config.RETRY_DELAY * (attempt + 1))
                else:
                    print_error(f"API failed: {e}")
                    return None
        return None

    def _analyze_scene_and_generate_prompt(self, scene: Dict) -> Optional[Dict]:
        """Phân tích scene và tạo prompt riêng cho scene đó"""
        scene_id = scene['scene_id']
        frame_first = scene.get('frame_first')
        frame_last = scene.get('frame_last')

        if not frame_first or not frame_last:
            return None

        print_progress(f"Analyzing scene {scene_id + 1}...", scene_id + 1, len(self.scenes))

        # Build content
        content = [{
            "type": "text",
            "text": self.SCENE_PROMPT_TEMPLATE.format(duration=scene['duration'])
        }]

        # Add FIRST frame
        try:
            base64_first = self._encode_image_base64(frame_first)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_first}",
                    "detail": "high"
                }
            })
        except:
            pass

        # Add LAST frame
        try:
            base64_last = self._encode_image_base64(frame_last)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_last}",
                    "detail": "high"
                }
            })
        except:
            pass

        # Call API
        prompt = self._call_vision_api(
            messages=[{"role": "user", "content": content}],
            max_tokens=500
        )

        if not prompt:
            return None

        # Extract prompt text (remove "PROMPT:" prefix if exists)
        prompt_text = prompt.strip()
        if prompt_text.startswith("PROMPT:"):
            prompt_text = prompt_text[7:].strip()

        scene['sora_prompt'] = prompt_text

        return scene

    # ========== EXPORT ==========

    def _export_results(self) -> str:
        """Export scenes với ảnh đầu + cuối + prompt"""
        print_progress("Đang export kết quả...")

        try:
            safe_title = "".join(c for c in self.video_title if c.isalnum() or c in (' ', '_', '-'))[:50]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_folder = Path(Config.OUTPUT_DIR) / f"{safe_title}_{timestamp}"
            output_folder.mkdir(exist_ok=True, parents=True)

            # Copy images và tạo prompt files cho từng scene
            for scene in self.scenes:
                scene_id = scene['scene_id']
                scene_folder = output_folder / f"scene_{scene_id:04d}"
                scene_folder.mkdir(exist_ok=True)

                # Copy frame đầu
                if 'frame_first' in scene and os.path.exists(scene['frame_first']):
                    shutil.copy(
                        scene['frame_first'],
                        scene_folder / f"FIRST_frame.jpg"
                    )

                # Copy frame cuối
                if 'frame_last' in scene and os.path.exists(scene['frame_last']):
                    shutil.copy(
                        scene['frame_last'],
                        scene_folder / f"LAST_frame.jpg"
                    )

                # Save prompt
                if 'sora_prompt' in scene:
                    prompt_file = scene_folder / "sora_prompt.txt"
                    with open(prompt_file, 'w', encoding='utf-8') as f:
                        f.write(f"Scene {scene_id + 1}\n")
                        f.write(f"Duration: {scene['duration']:.1f}s\n")
                        f.write(f"Time: {scene['start_time']:.1f}s - {scene['end_time']:.1f}s\n")
                        f.write(f"\n{'='*70}\n")
                        f.write(f"SORA 2 PROMPT:\n")
                        f.write(f"{'='*70}\n\n")
                        f.write(scene['sora_prompt'])

            # Tạo summary file
            summary_file = output_folder / "00_SUMMARY.txt"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"{'='*70}\n")
                f.write(f"YOUTUBE SCENE-BY-SCENE ANALYSIS\n")
                f.write(f"{'='*70}\n\n")
                f.write(f"Video: {self.video_title}\n")
                f.write(f"URL: {self.youtube_url}\n")
                f.write(f"Total Scenes: {len(self.scenes)}\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"{'='*70}\n")
                f.write(f"SCENE LIST\n")
                f.write(f"{'='*70}\n\n")

                for scene in self.scenes:
                    f.write(f"Scene {scene['scene_id'] + 1}:\n")
                    f.write(f"  - Duration: {scene['duration']:.1f}s\n")
                    f.write(f"  - Time: {scene['start_time']:.1f}s - {scene['end_time']:.1f}s\n")
                    f.write(f"  - Folder: scene_{scene['scene_id']:04d}/\n")
                    if 'sora_prompt' in scene:
                        f.write(f"  - Prompt: {scene['sora_prompt'][:100]}...\n")
                    f.write(f"\n")

            # JSON export
            json_file = output_folder / "scenes_data.json"
            json_data = {
                'video_info': {
                    'title': self.video_title,
                    'url': self.youtube_url,
                    'metadata': self.video_metadata,
                    'total_scenes': len(self.scenes)
                },
                'scenes': [
                    {
                        'scene_id': s['scene_id'],
                        'start_time': s['start_time'],
                        'end_time': s['end_time'],
                        'duration': s['duration'],
                        'sora_prompt': s.get('sora_prompt', ''),
                        'frame_first': f"scene_{s['scene_id']:04d}/FIRST_frame.jpg",
                        'frame_last': f"scene_{s['scene_id']:04d}/LAST_frame.jpg"
                    }
                    for s in self.scenes
                ],
                'export_date': datetime.now().isoformat()
            }

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            print_success(f"Đã export vào: {output_folder}/")
            print_success(f"  - {len(self.scenes)} scene folders (mỗi folder có: FIRST_frame.jpg + LAST_frame.jpg + sora_prompt.txt)")
            print_success(f"  - 00_SUMMARY.txt (tổng quan)")
            print_success(f"  - scenes_data.json (dữ liệu JSON)")

            return str(output_folder)

        except Exception as e:
            print_error(f"Lỗi export: {e}")
            return ""

    # ========== MAIN PROCESS ==========

    def analyze(self, youtube_url: str) -> Optional[str]:
        """Phân tích video và tạo prompt cho từng scene"""
        self.youtube_url = youtube_url

        print_header("YOUTUBE SCENE-BY-SCENE ANALYZER")
        print("📹 Xuất ảnh đầu + ảnh cuối cho mỗi cảnh")
        print("🎬 Tạo prompt cinema chi tiết cho MỖI cảnh\n")

        # Get metadata
        self._get_metadata(youtube_url)

        # Download video
        if not self._download_video(youtube_url):
            return None

        # Detect scenes
        if not self._detect_scenes():
            cleanup_temp()
            return None

        # Extract first & last frames
        if not self._extract_first_last_frames():
            cleanup_temp()
            return None

        # Analyze each scene and generate prompts
        print_header(f"ANALYZING {len(self.scenes)} SCENES")

        for scene in self.scenes:
            result = self._analyze_scene_and_generate_prompt(scene)
            if result:
                print_success(f"Scene {scene['scene_id'] + 1} ✓")
            time.sleep(0.5)

        # Export results
        print_header("EXPORTING RESULTS")
        output_path = self._export_results()

        # Cleanup
        cleanup_temp()

        if output_path:
            print_header("✓ HOÀN TẤT!")
            print(f"📁 Kết quả: {output_path}/")
            print(f"📊 Tổng: {len(self.scenes)} scenes")
            print(f"🎬 Mỗi scene có: 2 ảnh (đầu+cuối) + 1 prompt chi tiết\n")

        return output_path

# ========== CLI ==========

def main():
    print_header("YOUTUBE SCENE-BY-SCENE ANALYZER")
    print("🎬 Phân tích từng cảnh và tạo prompt riêng\n")

    url = input("Nhập YouTube URL: ").strip()
    if not url:
        print_error("URL không hợp lệ")
        return

    load_env_file()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        api_key = input("Nhập OpenAI API Key: ").strip()

    if not api_key:
        print_error("Cần OpenAI API Key")
        return

    try:
        analyzer = SceneBySceneAnalyzer(api_key=api_key)
        result = analyzer.analyze(youtube_url=url)

        if result:
            print_success("✓ Phân tích thành công!")
        else:
            print_error("Có lỗi xảy ra")

    except KeyboardInterrupt:
        print("\n\n⚠ Đã dừng")
        cleanup_temp()
    except Exception as e:
        print_error(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()
        cleanup_temp()

if __name__ == "__main__":
    main()
