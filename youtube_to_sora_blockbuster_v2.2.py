#!/usr/bin/env python3

"""
YouTube Video Analyzer to Sora 2 Prompt Generator - BLOCKBUSTER VERSION 2.2
Phân tích video theo tiêu chuẩn PHIM BOM TẤN HOLLYWOOD

Features:
- Cinematic analysis theo chuẩn Hollywood
- Technical specs: lens, aperture, focal length, aspect ratio
- Production value assessment
- VFX & CGI detection
- Color grading analysis
- Storytelling structure (3-act, pacing)
- Genre-specific analysis
- Professional lighting setups
- Sound design analysis
- Chi tiết nhân vật & con vật
- Không giới hạn scenes
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
    FRAMES_PER_SCENE = 4

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
    OUTPUT_DIR = "output_blockbuster"
    TEMP_FRAMES_DIR = "temp_frames"

    # Limits
    MAX_SCENES_TO_ANALYZE = 999
    MAX_SCENE_SUMMARY_LENGTH = 400


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


def print_section(text: str):
    print("\n" + "-"*70)
    print(text)
    print("-"*70)


def print_progress(message: str, step: Optional[int] = None, total: Optional[int] = None):
    if step and total:
        print(f"[{step}/{total}] {message}")
    else:
        print(f"• {message}")


def print_success(message: str):
    print(f"✓ {message}")


def print_error(message: str):
    print(f"✗ {message}")


def print_warning(message: str):
    print(f"⚠ {message}")


# ========== MAIN CLASS ==========

class YouTubeToSoraBlockbusterAnalyzer:
    """
    BLOCKBUSTER Version 2.2 - Hollywood Standard Analysis
    """

    def __init__(self, api_key: Optional[str] = None):
        load_env_file()

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

        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Không thể khởi tạo OpenAI client: {e}")

        ensure_directories()

        self.video_path: Optional[str] = None
        self.audio_path: Optional[str] = None
        self.youtube_url: Optional[str] = None
        self.video_title: str = ""
        self.video_metadata: Dict[str, Any] = {}
        self.scenes: List[Dict] = []
        self.frames: List[str] = []

    # ========== CACHE METHODS ==========

    def _get_cache_key(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()

    def _save_cache(self, key: str, data: Dict):
        try:
            cache_file = Path(Config.CACHE_DIR) / f"{key}.json"
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print_warning(f"Không thể lưu cache: {e}")

    def _load_cache(self, key: str) -> Optional[Dict]:
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
                print_success(f"Thời lượng: {self.video_metadata['duration']}s, FPS: {self.video_metadata.get('fps', 'N/A')}")
                return self.video_metadata
        except subprocess.TimeoutExpired:
            print_error("Timeout khi lấy metadata")
        except Exception as e:
            print_error(f"Lỗi lấy metadata: {e}")

        self.video_title = f"Video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return {}

    def _download_video(self, youtube_url: str) -> bool:
        print_progress("Đang tải video...")

        try:
            video_output = "temp_video.mp4"
            audio_output = "temp_audio.m4a"

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

            total_scenes = len(scenes)
            if total_scenes > Config.MAX_SCENES_TO_ANALYZE:
                print_warning(f"Video có {total_scenes} scenes - Sẽ phân tích TẤT CẢ")
            else:
                print_success(f"Đã phát hiện {total_scenes} scenes")

            self.scenes = scenes
            return scenes

        except Exception as e:
            print_error(f"Lỗi phát hiện scenes: {e}")
            return []

    def _extract_frames_from_scenes(self) -> List[str]:
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
        try:
            img = cv2.imread(frame_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = img_rgb.reshape(-1, 3)

            avg_color = np.mean(pixels, axis=0)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            brightness = float(np.mean(gray))
            contrast = float(np.std(gray))

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
        with open(image_path, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8")

    # ========== AI ANALYSIS - BLOCKBUSTER STANDARD ==========

    def _call_vision_api_with_retry(self, messages: List[Dict], max_tokens: int = 3000) -> Optional[str]:
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

    def _analyze_scene_blockbuster(self, scene: Dict) -> Optional[Dict]:
        """Phân tích scene theo tiêu chuẩn HOLLYWOOD BLOCKBUSTER"""
        scene_id = scene['scene_id']
        frames = scene.get('frames', [])

        if not frames:
            return None

        print_progress(f"Đang phân tích scene {scene_id + 1} (Blockbuster Standard)...", scene_id + 1, len(self.scenes))

        content = [{
            "type": "text",
            "text": f"""Phân tích scene này theo TIÊU CHUẨN PHIM BOM TẤN HOLLYWOOD (thời lượng: {scene['duration']:.1f}s):

🎬 HÀNH ĐỘNG & CỐT TRUYỆN
- Diễn biến: Gì đang xảy ra? Conflict/tension?
- Pacing: Slow/medium/fast? Dramatic beats?
- Story purpose: Setup/confrontation/resolution/transition?

👥 NHÂN VẬT (NẾU CÓ) - MÔ TẢ HOLLYWOOD-LEVEL:
- Số lượng và vai trò (protagonist/antagonist/supporting)
- PHYSICAL DETAILS:
  * Gender & Age: (VD: male 30s, female mid-20s)
  * Height: (VD: tall ~185cm, average ~170cm, petite ~160cm)
  * Build & Weight: (athletic 75kg, slim 55kg, muscular 90kg, etc.)
  * Skin tone: (pale ivory, fair, tan, olive, bronze, brown, deep brown, ebony)
  * Hair details:
    - Color: (platinum blonde/golden blonde/light brown/chestnut/dark brown/black/auburn/gray/silver/white)
    - Style: (slicked back/messy/wavy/curly/straight/braided/dreadlocks)
    - Length: (buzz cut/short/medium/shoulder-length/long/very long)
  * Facial features: (angular/soft/chiseled/round), jawline, cheekbones, eyes (color/shape), nose, lips
  * Body proportions: head-to-body ratio (1:7, 1:8), leg length, torso, shoulders
- COSTUME DESIGN:
  * Style era: (contemporary/period/futuristic/fantasy)
  * Outfit type: (casual/formal/tactical/uniform/costume)
  * Colors: dominant colors và accent colors
  * Material/texture: (leather/silk/cotton/metal/synthetic)
  * Fit: (tailored/fitted/loose/oversized/tight)
  * Accessories: jewelry/watches/glasses/hats/weapons/gadgets
  * Condition: pristine/worn/damaged/weathered
- Performance:
  * Body language: posture, gestures, movement quality
  * Facial expression: emotion, intensity
  * Eye line và blocking

🐾 CON VẬT/CREATURES (NẾU CÓ):
- Species: (dog/cat/horse/bird/fantasy creature/alien)
- Breed/Type: specific breed nếu nhận ra
- Size dimensions:
  * Height: (VD: 30cm small dog, 70cm large dog, 160cm horse at shoulder)
  * Length: body length, tail length
  * Weight estimate: (VD: 3kg cat, 35kg dog, 500kg horse)
- Physical characteristics:
  * Coat/fur/scales/feathers: color(s), pattern (solid/spotted/striped/mottled)
  * Texture: (fluffy/sleek/rough/smooth/shiny)
  * Features: ears (pointed/floppy), tail (bushy/thin), eyes, teeth/claws
  * Body proportions: head:body:legs ratio
- Movement & behavior: gait, speed, actions

📷 CINEMATOGRAPHY - TECHNICAL SPECS:
- Camera angle: (eye-level/high-angle/low-angle/dutch-angle/overhead/worm's-eye)
- Camera movement:
  * Type: (static/pan/tilt/dolly/tracking/crane/steadicam/handheld/gimbal)
  * Speed: smooth/fast/whip pan
  * Motivation: motivated by character/unmotivated
- Shot type & framing:
  * Size: (extreme wide/wide/full/medium/close-up/extreme close-up/insert)
  * Composition: rule of thirds/golden ratio/centered/symmetrical/asymmetrical
  * Headroom & lead room
- Lens characteristics:
  * Focal length: (wide 18-35mm/normal 50mm/portrait 85mm/telephoto 100-200mm)
  * Depth of field: shallow (f/1.4-2.8)/medium/deep (f/8-16)
  * Lens distortion: minimal/perspective distortion/fisheye
- Focus:
  * Type: sharp throughout/rack focus/selective focus
  * Subject isolation: foreground/middle/background

💡 LIGHTING - HOLLYWOOD SETUP:
- Lighting scheme:
  * Setup: 3-point (key/fill/back)/naturalistic/high-key/low-key/chiaroscuro
  * Key light: position (front/side/back), intensity (soft/hard), color temp
  * Fill ratio: high contrast/balanced/flat
  * Practical lights: visible sources (lamps/windows/screens/fire)
- Light quality:
  * Hard light: sharp shadows, defined edges
  * Soft light: diffused, wrapped, gentle shadows
  * Direction: top/side/Rembrandt/butterfly/split
- Color temperature:
  * Kelvin range: warm (2700-3500K)/neutral (4000-5000K)/cool (5500-7000K)
  * Gels/filters: warming/cooling/color accents
- Atmosphere:
  * Haze/fog/smoke for volumetric lighting
  * God rays/light shafts
  * Ambient occlusion

🎨 COLOR GRADING:
- Color palette: (warm/cool/complementary/analogous/monochromatic)
- LUT style: (naturalistic/cinematic/teal-orange/bleach bypass/cross-processed)
- Saturation: vibrant/desaturated/selective color
- Contrast: high/normal/low/lifted blacks
- Mood: bright/moody/noir/romantic/horror/fantasy

🏞️ PRODUCTION DESIGN:
- Location: (practical location/studio set/green screen/hybrid)
- Environment: (urban/rural/interior/exterior/natural/constructed)
- Set dressing: props, furniture, details
- Architecture: style, period, scale
- Depth layers: foreground/mid/background elements

✨ VFX & POST-PRODUCTION:
- CGI elements: (none/minimal/moderate/heavy)
- Compositing: green screen replacement, matte paintings
- Particle effects: smoke/dust/sparks/magic
- Digital enhancement: sky replacement, cleanup, beauty
- Motion graphics/HUD elements

🎭 GENRE CONVENTIONS:
- Genre indicators: (action/drama/sci-fi/horror/comedy/romance/thriller)
- Tropes: specific genre conventions visible
- Tone: serious/lighthearted/dark/epic/intimate

🎵 VISUAL RHYTHM:
- Cutting pattern: fast/moderate/slow
- Motion within frame: static/dynamic/chaotic
- Visual tempo matching story beats

📐 ASPECT RATIO & FRAMING:
- Estimated ratio: (16:9/2.39:1 anamorphic/1.85:1/IMAX)
- Frame usage: letterboxed/full frame
- Safe areas: compositional boundaries

😊 EMOTIONAL IMPACT:
- Mood: overall feeling of the scene
- Atmosphere: tension/calm/excitement/dread
- Audience engagement: passive/immersive/intense

🎬 BLOCKBUSTER QUALITY SCORE:
- Production value: (low-budget/indie/mid-budget/studio/blockbuster) - đánh giá từ 1-10
- Technical execution: camera work, lighting, composition quality
- Cinematic polish: color grade, VFX, overall finish

Trả lời CỰC KỲ CHI TIẾT, TIẾNG VIỆT, dựa trên visual evidence. Nếu không chắc chắn về technical detail, hãy ước tính dựa trên visual cues."""
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

        analysis = self._call_vision_api_with_retry([{"role": "user", "content": content}], max_tokens=3500)

        if not analysis:
            return None

        visual = self._analyze_visual_composition(frames[0])

        return {
            'scene_id': scene_id,
            'analysis': analysis,
            'visual_composition': visual,
            'duration': scene['duration'],
            'timestamp': f"{scene['start_time']:.1f}s - {scene['end_time']:.1f}s"
        }

    def _analyze_overall_blockbuster(self, scene_analyses: List[Dict], transcript: Optional[Dict]) -> Optional[str]:
        """Phân tích tổng thể theo chuẩn BLOCKBUSTER"""
        print_progress("Đang tổng hợp phân tích BLOCKBUSTER tổng thể...")

        scene_text = "\n\n".join([
            f"SCENE {s['scene_id'] + 1} ({s['timestamp']}):\n{s['analysis']}"
            for s in scene_analyses if s
        ])

        transcript_text = ""
        if transcript:
            transcript_text = f"\n\nTRANSCRIPT:\n{transcript.get('text', '')}"

        metadata_text = f"\nThời lượng: {self.video_metadata.get('duration', 0)}s, FPS: {self.video_metadata.get('fps', 'N/A')}, Resolution: {self.video_metadata.get('width', 0)}x{self.video_metadata.get('height', 0)}"

        prompt = f"""Dựa trên phân tích chi tiết từng scene, viết PHÂN TÍCH TỔNG THỂ theo TIÊU CHUẨN HOLLYWOOD BLOCKBUSTER:

VIDEO METADATA:{metadata_text}

PHÂN TÍCH TỪNG SCENE:
{scene_text}
{transcript_text}

Hãy viết phân tích CHUYÊN NGHIỆP bao gồm:

1. STORY STRUCTURE & NARRATIVE
- Cốt truyện tổng quát
- Three-act structure (nếu áp dụng): Setup/Confrontation/Resolution
- Character arcs và development
- Dramatic tension và conflict
- Story beats và turning points
- Pacing analysis: rhythm, tempo changes

2. CHARACTERS IN-DEPTH (nếu có)
- Tổng hợp TẤT CẢ nhân vật xuất hiện
- MÔ TẢ CHI TIẾT từng nhân vật:
  * Physical: height, build, weight, skin tone, hair (color/style/length)
  * Costume design: style, colors, materials, era, symbolism
  * Performance: body language, expressions, character traits
  * Role: protagonist/antagonist/supporting/ensemble
- Character relationships và dynamics

3. CREATURES/ANIMALS (nếu có)
- Tổng hợp chi tiết: species, size, weight, colors, proportions
- Role in story
- Visual design quality

4. CINEMATOGRAPHY ANALYSIS
- Camera language: predominant movements và angles
- Shot vocabulary: most used shot types
- Lens choices: estimated focal lengths pattern
- Focus techniques: rack focus, selective, deep
- Coverage style: single cam/multi-cam, master shots/coverage
- Reference films: visual style tương tự phim nào?

5. LIGHTING DESIGN
- Overall lighting approach: naturalistic/stylized/high-key/low-key
- Key setups used: 3-point/practical/motivated
- Light quality patterns: hard/soft balance
- Color temperature palette: warm/cool/mixed
- Mood lighting: how lighting supports story
- Time of day representation

6. COLOR GRADING & VISUAL STYLE
- Color palette analysis: dominant colors, contrasts
- Grading style: LUT characteristics, references
- Saturation approach: vibrant/muted/selective
- Contrast ratio: high/medium/low, lifted blacks?
- Visual consistency: unified look or varied?
- Mood through color: emotional color coding

7. PRODUCTION DESIGN
- Locations: types, variety, authenticity
- Set design: quality, detail level, period accuracy
- Props & dressing: attention to detail
- World-building: consistency, believability
- Scale: intimate/epic/varied

8. VFX & POST-PRODUCTION
- CGI usage: none/minimal/moderate/heavy, quality level
- Compositing quality: seamless/visible/rough
- Effects types: practical/digital/hybrid
- Post enhancement: cleanup, beauty, sky replacement
- Technical polish: professional/amateur/mixed

9. TECHNICAL QUALITY ASSESSMENT
- Camera work: (1-10) - stability, movement quality, framing
- Lighting: (1-10) - setup complexity, mood creation, technical execution
- Color grading: (1-10) - consistency, artistic vision, technical skill
- VFX quality: (1-10) - realism, integration, artistry
- Production value: (1-10) - overall budget impression

10. GENRE & STYLE
- Primary genre: Action/Drama/Sci-fi/Horror/Comedy/Romance/Thriller/Documentary/etc.
- Subgenres and blends
- Genre conventions: how well executed?
- Tone: serious/dark/light/epic/intimate/gritty/polished
- Visual references: similar films/directors/styles

11. OVERALL PRODUCTION VALUE
- Budget level assessment: (low/indie/mid-budget/studio/blockbuster AAA)
- Technical execution: professional/semi-pro/amateur
- Cinematic quality: (1-10)
- Hollywood comparison: comparable to what tier?
- Strengths: best aspects
- Weaknesses: areas for improvement

12. SORA 2 GENERATION INSIGHTS
- Complexity level: easy/medium/hard to recreate
- Key challenges for AI generation
- Elements that need emphasis in prompts
- Technical specs to specify

Trả lời CỰC KỲ CHI TIẾT, có CẤU TRÚC, TIẾNG VIỆT, như một film critic chuyên nghiệp."""

        return self._call_vision_api_with_retry(
            [{"role": "user", "content": prompt}],
            max_tokens=4000
        )

    def _generate_blockbuster_prompts(self, overall_analysis: str, scene_analyses: List[Dict]) -> Optional[str]:
        """Tạo Sora prompts - BLOCKBUSTER LEVEL"""
        print_progress("Đang tạo Sora 2 BLOCKBUSTER prompts...")

        scene_text = "\n".join([
            f"Scene {s['scene_id'] + 1}: {s['analysis'][:500]}..."
            for s in scene_analyses[:10] if s
        ])

        prompt = f"""Dựa trên phân tích BLOCKBUSTER-level, tạo 3 PROMPT CHUYÊN NGHIỆP cho Sora 2:

PHÂN TÍCH TỔNG THỂ:
{overall_analysis}

CÁC SCENE CHI TIẾT:
{scene_text}

Tạo 3 prompts với HOLLYWOOD BLOCKBUSTER STANDARDS:

1. **CONCISE BLOCKBUSTER PROMPT** (70-90 words):
   - Core action và story beat
   - Key character details (height, build, skin, hair, costume colors)
   - Primary camera move và shot type
   - Lighting mood và color palette
   - Production value indicators
   - Súc tích nhưng PACKED with specific details

2. **DETAILED TECHNICAL PROMPT** (180-250 words):
   - CHARACTERS: Full physical description (height estimate, body type, exact skin tone, hair color/style/length, facial features, costume details with colors/materials/fit, accessories, body proportions)
   - CREATURES/ANIMALS: Species, size/weight, colors/patterns, proportions, behavior
   - CINEMATOGRAPHY: Specific camera move (dolly in/crane up/steadicam tracking), shot size, lens (35mm/50mm/85mm), aperture (f/2.8/f/5.6), focus technique
   - LIGHTING: Setup type (3-point/Rembrandt/natural), key light position, fill ratio, color temp (3200K/5600K), quality (hard/soft), practicals
   - COLOR GRADING: LUT style (teal-orange/bleach bypass/naturalistic), saturation level, contrast approach, mood
   - PRODUCTION DESIGN: Location specifics, set dressing, props, depth layers
   - VFX: CGI elements if any, compositing, effects
   - ASPECT RATIO: 2.39:1/16:9/1.85:1
   - GENRE & TONE: Specific genre, mood, atmosphere
   - PACING: Action speed, dramatic beat

3. **CINEMATIC MASTERPIECE PROMPT** (150-200 words):
   - Artistic vision và emotional core
   - Visual metaphors và symbolism
   - Film references: "in the style of [Director/Film]"
   - Cinematographic artistry
   - Character essence beyond physical
   - Lighting as storytelling
   - Color psychology
   - Compositional beauty
   - Genre elevation
   - Emotional journey
   - Cinematic poetry

CRITICAL REQUIREMENTS:
✅ ALL IN ENGLISH (professional film industry terminology)
✅ CHARACTERS: Must include height (cm/ft), build (athletic/slim/muscular), skin tone (ivory/tan/olive/bronze/brown/ebony), hair (blonde/brunette/black/red + straight/wavy/curly + short/long), costume (colors, style, fit, materials)
✅ ANIMALS: Must include species, size (height/length/weight), coat color/pattern, proportions
✅ CAMERA: Specific movement type (not just "moving"), lens focal length, aperture if relevant
✅ LIGHTING: Specific setup (not just "good lighting"), color temperature, quality, direction
✅ COLOR: Specific grading style, palette, mood through color
✅ PRODUCTION VALUE: Indicators of blockbuster quality
✅ Use PRECISE technical film terminology
✅ Vivid, specific, visualizable
✅ NO explanations, ONLY prompts

Format:
=== CONCISE BLOCKBUSTER PROMPT ===
[prompt here]

=== DETAILED TECHNICAL PROMPT ===
[prompt here]

=== CINEMATIC MASTERPIECE PROMPT ===
[prompt here]"""

        return self._call_vision_api_with_retry(
            [{"role": "user", "content": prompt}],
            max_tokens=2500
        )

    # ========== EXPORT ==========

    def _save_results(self, overall: str, scenes: List[Dict], transcript: Optional[Dict], prompts: str) -> str:
        """Lưu kết quả ra files"""
        try:
            safe_title = "".join(c for c in self.video_title if c.isalnum() or c in (' ', '_', '-'))[:50]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{safe_title}_BLOCKBUSTER_{timestamp}"

            # ========== TXT FILE ==========
            txt_path = f"{Config.OUTPUT_DIR}/{filename}.txt"

            scene_details = "\n\n".join([
                f"""{'='*70}
SCENE {s['scene_id'] + 1} | {s['timestamp']} | {s['duration']:.1f}s
{'='*70}

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
{'='*70}
TRANSCRIPT & DIALOGUE
{'='*70}
Language: {transcript.get('language', 'unknown')}

{transcript.get('text', '')}
"""

            txt_content = f"""{'='*70}
YOUTUBE TO SORA 2 - BLOCKBUSTER ANALYSIS REPORT v2.2
HOLLYWOOD PRODUCTION STANDARDS
{'='*70}

VIDEO: {self.video_title}
URL: {self.youtube_url}
DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {self.video_metadata.get('duration', 0)}s
FPS: {self.video_metadata.get('fps', 'N/A')}
Resolution: {self.video_metadata.get('width', 0)}x{self.video_metadata.get('height', 0)}
Total Scenes Analyzed: {len(scenes)}

{'='*70}
BLOCKBUSTER-LEVEL OVERALL ANALYSIS
{'='*70}

{overall}

{'='*70}
SCENE-BY-SCENE BREAKDOWN ({len(scenes)} scenes)
HOLLYWOOD TECHNICAL STANDARDS
{'='*70}

{scene_details}
{transcript_section}

{'='*70}
SORA 2 PROMPTS - BLOCKBUSTER QUALITY
{'='*70}

{prompts}

{'='*70}
Generated by YouTube to Sora 2 Blockbuster Analyzer v2.2
Features: Hollywood standards, unlimited scenes, detailed technical analysis
Cinematography • Lighting • Color Grading • Production Design • VFX
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
                'blockbuster_analysis': overall,
                'scenes': scenes,
                'transcript': transcript,
                'sora_prompts': prompts,
                'version': '2.2-BLOCKBUSTER',
                'analysis_standards': [
                    'hollywood_cinematography',
                    'professional_lighting',
                    'color_grading_analysis',
                    'production_design',
                    'vfx_assessment',
                    'character_physical_details',
                    'animal_detailed_specs',
                    'technical_camera_specs',
                    'genre_conventions',
                    'quality_scoring'
                ]
            }

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            print_success(f"Đã lưu JSON: {json_path}")

            # ========== MARKDOWN FILE ==========
            md_path = f"{Config.OUTPUT_DIR}/{filename}.md"
            md_content = f"""# 🎬 YouTube to Sora 2 - BLOCKBUSTER Analysis

**Version:** 2.2 - Hollywood Production Standards
**Video:** {self.video_title}
**URL:** {self.youtube_url}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Duration:** {self.video_metadata.get('duration', 0)}s
**Resolution:** {self.video_metadata.get('width', 0)}x{self.video_metadata.get('height', 0)} @ {self.video_metadata.get('fps', 'N/A')} FPS
**Total Scenes:** {len(scenes)}

---

## 🎯 Blockbuster-Level Overall Analysis

{overall}

---

## 🎬 Scene-by-Scene Technical Breakdown

"""
            for s in scenes:
                if s:
                    md_content += f"""### Scene {s['scene_id'] + 1} • {s['timestamp']} • {s['duration']:.1f}s

{s['analysis']}

**Visual Metrics:**
- Brightness: {s.get('visual_composition', {}).get('brightness', 0):.1f}
- Contrast: {s.get('visual_composition', {}).get('contrast', 0):.1f}
- Color Mood: {s.get('visual_composition', {}).get('color_mood', 'N/A')}

---

"""

            if transcript:
                md_content += f"""## 🎤 Transcript & Dialogue

**Language:** {transcript.get('language', 'unknown')}

{transcript.get('text', '')}

---

"""

            md_content += f"""## 🎨 Sora 2 Blockbuster Prompts

{prompts}

---

## 📊 Analysis Standards Applied

- ✅ Hollywood Cinematography Analysis
- ✅ Professional Lighting Setups
- ✅ Color Grading & LUT Identification
- ✅ Production Design Assessment
- ✅ VFX & CGI Quality Evaluation
- ✅ Character Physical Specifications
- ✅ Animal/Creature Detailed Specs
- ✅ Technical Camera Specifications
- ✅ Lens & Aperture Estimates
- ✅ Genre Conventions Analysis
- ✅ Quality Scoring (1-10 scale)
- ✅ Blockbuster Value Assessment

---

*Generated by YouTube to Sora 2 Blockbuster Analyzer v2.2*
*Hollywood Production Standards • Unlimited Scenes • Technical Precision*
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
        Phân tích video YouTube theo tiêu chuẩn BLOCKBUSTER
        """
        self.youtube_url = youtube_url

        print_header("YOUTUBE TO SORA 2 - BLOCKBUSTER ANALYZER v2.2")
        print("🎬 Hollywood Production Standards")
        print("🎯 Unlimited scenes • Technical precision • Industry terminology\n")

        cache_key = self._get_cache_key(youtube_url)
        if use_cache:
            cached = self._load_cache(cache_key)
            if cached:
                print_success("Tìm thấy kết quả trong cache!")
                self.video_title = cached.get('video_info', {}).get('title', '')
                print(f"Video: {self.video_title}\n")

                print_section("BLOCKBUSTER ANALYSIS (từ cache)")
                print(cached.get('blockbuster_analysis', ''))

                print_section("SORA 2 PROMPTS (từ cache)")
                print(cached.get('sora_prompts', ''))

                return cached

        self._get_video_metadata(youtube_url)

        if not self._download_video(youtube_url):
            return None

        if not self._detect_scenes():
            cleanup_temp_files()
            return None

        if not self._extract_frames_from_scenes():
            cleanup_temp_files()
            return None

        transcript = None
        if analyze_audio:
            transcript = self._extract_transcript()

        print_section(f"PHÂN TÍCH BLOCKBUSTER-LEVEL: {len(self.scenes)} SCENES")
        scene_analyses = []
        for scene in self.scenes:
            result = self._analyze_scene_blockbuster(scene)
            if result:
                scene_analyses.append(result)
            time.sleep(0.5)

        if not scene_analyses:
            print_error("Không thể phân tích scenes")
            cleanup_temp_files()
            return None

        print_success(f"Đã phân tích xong {len(scene_analyses)} scenes theo chuẩn Hollywood!")

        print_section("PHÂN TÍCH TỔNG THỂ - BLOCKBUSTER")
        overall = self._analyze_overall_blockbuster(scene_analyses, transcript)

        if overall:
            print(overall)
        else:
            cleanup_temp_files()
            return None

        print_section("TẠO SORA 2 BLOCKBUSTER PROMPTS")
        prompts = self._generate_blockbuster_prompts(overall, scene_analyses)

        if prompts:
            print(prompts)
        else:
            cleanup_temp_files()
            return None

        print_section("LƯU KẾT QUẢ")
        self._save_results(overall, scene_analyses, transcript, prompts)

        if use_cache:
            cache_data = {
                'video_info': {
                    'title': self.video_title,
                    'url': self.youtube_url,
                    'metadata': self.video_metadata,
                    'total_scenes': len(scene_analyses)
                },
                'blockbuster_analysis': overall,
                'scene_analyses': scene_analyses,
                'transcript': transcript,
                'sora_prompts': prompts,
                'version': '2.2-BLOCKBUSTER'
            }
            self._save_cache(cache_key, cache_data)
            print_success("Đã lưu vào cache")

        cleanup_temp_files()

        print_header("✓ HOÀN TẤT - BLOCKBUSTER QUALITY!")
        print(f"📁 Kết quả đã lưu trong folder: {Config.OUTPUT_DIR}/")
        print(f"🎬 Đã phân tích {len(scene_analyses)} scenes theo tiêu chuẩn Hollywood")
        print(f"📊 Bao gồm: Cinematography • Lighting • Color Grading • Production Design • VFX\n")

        return {
            'blockbuster_analysis': overall,
            'scene_analyses': scene_analyses,
            'transcript': transcript,
            'sora_prompts': prompts
        }


# ========== CLI ==========

def main():
    """Main CLI interface"""
    print_header("YOUTUBE TO SORA 2 - BLOCKBUSTER ANALYZER v2.2")
    print("🎬 Phân tích theo tiêu chuẩn HOLLYWOOD BLOCKBUSTER")
    print("✨ Cinematography • Lighting • Color Grading • Production Design • VFX")
    print("✨ Character physical specs • Animal details • Technical camera specs")
    print("✨ Genre analysis • Quality scoring • Unlimited scenes\n")

    youtube_url = input("Nhập YouTube URL: ").strip()
    if not youtube_url:
        print_error("URL không hợp lệ")
        return

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

    print("\n--- TÙY CHỌN ---")
    use_cache = input("Sử dụng cache? (y/n, mặc định: y): ").strip().lower() != 'n'
    analyze_audio = input("Phân tích audio? (y/n, mặc định: y): ").strip().lower() != 'n'

    try:
        analyzer = YouTubeToSoraBlockbusterAnalyzer(api_key=api_key)
        result = analyzer.analyze(
            youtube_url=youtube_url,
            use_cache=use_cache,
            analyze_audio=analyze_audio
        )

        if result:
            print_success("Phân tích BLOCKBUSTER thành công!")
            print(f"\n📊 Thống kê:")
            print(f"  - Tổng scenes: {len(result['scene_analyses'])}")
            print(f"  - Transcript: {'Có' if result['transcript'] else 'Không'}")
            print(f"  - Chuẩn: Hollywood Blockbuster")
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
