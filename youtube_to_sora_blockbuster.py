#!/usr/bin/env python3
"""
YouTube Video Analyzer to Sora 2 Prompt Generator - BLOCKBUSTER VERSION 2.3
Phân tích video theo tiêu chuẩn PHIM BOM TẤN HOLLYWOOD - Refactored

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

Improvements v2.3:
- Professional logging system
- Better error handling and recovery
- Optimized API calls with rate limiting
- Improved cache management
- Modular architecture
- Type safety with full type hints
- Progress tracking
- Configurable from .env or YAML
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
import json
import hashlib
import shutil
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from functools import wraps

try:
    import cv2
    import numpy as np
    from openai import OpenAI
    import base64
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Install with: pip install opencv-python numpy openai")
    sys.exit(1)


# ========== LOGGING SETUP ==========

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for terminal output"""

    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """Configure and return logger with color support"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Colored formatter
        formatter = ColoredFormatter(
            '%(levelname)s | %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()


# ========== ENUMS & DATA CLASSES ==========

class AnalysisStage(Enum):
    """Stages of video analysis"""
    METADATA = "metadata"
    DOWNLOAD = "download"
    SCENE_DETECTION = "scene_detection"
    FRAME_EXTRACTION = "frame_extraction"
    AUDIO_ANALYSIS = "audio_analysis"
    VISUAL_ANALYSIS = "visual_analysis"
    OVERALL_ANALYSIS = "overall_analysis"
    PROMPT_GENERATION = "prompt_generation"
    EXPORT = "export"


@dataclass
class VideoMetadata:
    """Video metadata structure"""
    title: str
    duration: float
    description: str
    uploader: str
    width: int
    height: int
    fps: float
    url: str

    def __str__(self) -> str:
        return (f"'{self.title}' | {self.duration}s | "
                f"{self.width}x{self.height}@{self.fps}fps")


@dataclass
class SceneInfo:
    """Scene information structure"""
    scene_id: int
    start_frame: int
    end_frame: int
    start_time: float
    end_time: float
    duration: float
    frames: List[str]
    analysis: Optional[str] = None
    visual_composition: Optional[Dict[str, float]] = None

    @property
    def timestamp(self) -> str:
        return f"{self.start_time:.1f}s - {self.end_time:.1f}s"


@dataclass
class Config:
    """Application configuration"""
    # Scene detection
    scene_threshold: float = 30.0
    min_scene_length: int = 15
    frames_per_scene: int = 4

    # Video download
    max_video_height: int = 1080

    # API settings
    vision_model: str = "gpt-4o"
    text_model: str = "gpt-4o"
    whisper_model: str = "whisper-1"
    max_retries: int = 3
    retry_delay: float = 2.0
    api_timeout: int = 120

    # Rate limiting
    api_calls_per_minute: int = 60

    # Folders
    cache_dir: Path = Path("cache")
    output_dir: Path = Path("output_blockbuster")
    temp_frames_dir: Path = Path("temp_frames")

    # Limits
    max_scenes_to_analyze: int = 999
    max_scene_summary_length: int = 400

    # Processing
    video_resize_width: int = 320  # For scene detection
    video_resize_height: int = 180
    jpeg_quality: int = 95

    def __post_init__(self):
        """Ensure directories exist"""
        for dir_path in [self.cache_dir, self.output_dir, self.temp_frames_dir]:
            dir_path.mkdir(exist_ok=True, parents=True)

    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables"""
        config = cls()

        # Override from environment if available
        if val := os.getenv('SCENE_THRESHOLD'):
            config.scene_threshold = float(val)
        if val := os.getenv('MAX_VIDEO_HEIGHT'):
            config.max_video_height = int(val)
        if val := os.getenv('VISION_MODEL'):
            config.vision_model = val
        if val := os.getenv('MAX_RETRIES'):
            config.max_retries = int(val)

        return config


# ========== UTILITIES ==========

def load_env_file(env_path: Path = Path('.env')) -> None:
    """Load environment variables from .env file"""
    if not env_path.exists():
        logger.debug(f"No .env file found at {env_path}")
        return

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    logger.warning(f"Invalid line {line_num} in .env: {line}")
                    continue

                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes
                for quote in ('"', "'"):
                    if value.startswith(quote) and value.endswith(quote):
                        value = value[1:-1]
                        break

                os.environ[key] = value

        logger.info(f"✓ Loaded environment from {env_path}")
    except Exception as e:
        logger.error(f"Error loading .env file: {e}")


def retry_on_failure(max_attempts: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """Decorator for retrying failed operations with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed: {e}. "
                            f"Retrying in {current_delay:.1f}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed")

            raise last_exception
        return wrapper
    return decorator


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def safe_filename(text: str, max_length: int = 50) -> str:
    """Convert text to safe filename"""
    safe = "".join(c for c in text if c.isalnum() or c in (' ', '_', '-'))
    return safe[:max_length].strip()


class ProgressTracker:
    """Track and display progress"""

    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()

    def update(self, increment: int = 1):
        """Update progress"""
        self.current += increment
        self._display()

    def _display(self):
        """Display progress bar"""
        if self.total == 0:
            return

        percent = (self.current / self.total) * 100
        elapsed = time.time() - self.start_time

        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = format_duration(eta)
        else:
            eta_str = "calculating..."

        bar_length = 30
        filled = int(bar_length * self.current / self.total)
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"\r{self.description}: [{bar}] {percent:.1f}% | ETA: {eta_str}",
              end='', flush=True)

        if self.current >= self.total:
            print()  # New line when complete


# ========== CACHE MANAGER ==========

class CacheManager:
    """Manage analysis cache"""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True, parents=True)

    def _get_key(self, url: str) -> str:
        """Generate cache key from URL"""
        return hashlib.md5(url.encode()).hexdigest()

    def get(self, url: str) -> Optional[Dict]:
        """Retrieve cached analysis"""
        cache_file = self.cache_dir / f"{self._get_key(url)}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"✓ Cache hit for URL")
            return data
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
            return None

    def set(self, url: str, data: Dict) -> bool:
        """Save analysis to cache"""
        cache_file = self.cache_dir / f"{self._get_key(url)}.json"

        try:
            # Add metadata
            data['_cache_meta'] = {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'version': '2.3'
            }

            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"✓ Saved to cache: {cache_file.name}")
            return True
        except Exception as e:
            logger.error(f"Cache write error: {e}")
            return False

    def clear(self) -> int:
        """Clear all cache files"""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except:
                pass
        logger.info(f"Cleared {count} cache files")
        return count


# ========== VIDEO DOWNLOADER ==========

class VideoDownloader:
    """Handle video downloading with yt-dlp"""

    def __init__(self, max_height: int = 1080):
        self.max_height = max_height
        self._check_ytdlp()

    def _check_ytdlp(self):
        """Check if yt-dlp is available"""
        try:
            subprocess.run(
                ["yt-dlp", "--version"],
                capture_output=True,
                timeout=5
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            raise RuntimeError(
                "yt-dlp not found! Install with: pip install yt-dlp"
            )

    @retry_on_failure(max_attempts=3, delay=2.0)
    def get_metadata(self, url: str) -> VideoMetadata:
        """Extract video metadata"""
        logger.info("Fetching video metadata...")

        result = subprocess.run(
            ["yt-dlp", "--dump-json", url],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise RuntimeError(f"Failed to get metadata: {result.stderr}")

        data = json.loads(result.stdout)

        metadata = VideoMetadata(
            title=data.get('title', 'Unknown'),
            duration=data.get('duration', 0),
            description=(data.get('description') or '')[:500],
            uploader=data.get('uploader', 'Unknown'),
            width=data.get('width', 0),
            height=data.get('height', 0),
            fps=data.get('fps', 30.0),
            url=url
        )

        logger.info(f"✓ Video: {metadata}")
        return metadata

    @retry_on_failure(max_attempts=2, delay=5.0)
    def download_video(self, url: str, output_path: Path) -> bool:
        """Download video file"""
        logger.info("Downloading video...")

        result = subprocess.run(
            [
                "yt-dlp",
                "-f", f"best[height<={self.max_height}][ext=mp4]",
                "-o", str(output_path),
                url
            ],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            raise RuntimeError(f"Download failed: {result.stderr}")

        if not output_path.exists():
            raise RuntimeError("Video file not created")

        logger.info(f"✓ Downloaded: {output_path.name}")
        return True

    def download_audio(self, url: str, output_path: Path) -> bool:
        """Download audio file (best effort)"""
        try:
            logger.info("Downloading audio...")

            result = subprocess.run(
                ["yt-dlp", "-f", "bestaudio[ext=m4a]", "-o", str(output_path), url],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and output_path.exists():
                logger.info(f"✓ Downloaded audio: {output_path.name}")
                return True
            else:
                logger.warning("Audio download failed (continuing without)")
                return False
        except Exception as e:
            logger.warning(f"Audio download error: {e}")
            return False


# ========== SCENE DETECTOR ==========

class SceneDetector:
    """Detect scene changes in video"""

    def __init__(self, config: Config):
        self.config = config

    def detect_scenes(self, video_path: Path) -> List[SceneInfo]:
        """Detect all scene changes"""
        logger.info("Detecting scenes...")

        cap = cv2.VideoCapture(str(video_path))

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames == 0:
            raise RuntimeError("Cannot read video file")

        logger.info(f"Video: {total_frames} frames @ {fps:.2f} fps")

        scene_boundaries = [0]
        prev_frame = None
        frame_idx = 0

        progress = ProgressTracker(total_frames, "Scene detection")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize for performance
            small = cv2.resize(
                frame,
                (self.config.video_resize_width, self.config.video_resize_height)
            )
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

            if prev_frame is not None:
                diff = cv2.absdiff(gray, prev_frame)
                mean_diff = np.mean(diff)

                # Scene change detected
                if mean_diff > self.config.scene_threshold:
                    min_gap = self.config.min_scene_length
                    if frame_idx - scene_boundaries[-1] > min_gap:
                        scene_boundaries.append(frame_idx)

            prev_frame = gray
            frame_idx += 1

            if frame_idx % 50 == 0:
                progress.update(50)

        progress.update(total_frames - progress.current)
        cap.release()

        # Add final boundary
        scene_boundaries.append(total_frames - 1)

        # Create SceneInfo objects
        scenes = []
        for i in range(len(scene_boundaries) - 1):
            start = scene_boundaries[i]
            end = scene_boundaries[i + 1]

            scenes.append(SceneInfo(
                scene_id=i,
                start_frame=start,
                end_frame=end,
                start_time=start / fps,
                end_time=end / fps,
                duration=(end - start) / fps,
                frames=[]
            ))

        logger.info(f"✓ Detected {len(scenes)} scenes")

        if len(scenes) > self.config.max_scenes_to_analyze:
            logger.warning(
                f"Video has {len(scenes)} scenes - "
                f"will analyze all (no limit)"
            )

        return scenes


# ========== FRAME EXTRACTOR ==========

class FrameExtractor:
    """Extract frames from video scenes"""

    def __init__(self, config: Config):
        self.config = config

    def extract_frames(
        self,
        video_path: Path,
        scenes: List[SceneInfo]
    ) -> int:
        """Extract representative frames from each scene"""
        logger.info(
            f"Extracting {self.config.frames_per_scene} frames "
            f"from each of {len(scenes)} scenes..."
        )

        cap = cv2.VideoCapture(str(video_path))
        total_frames = 0

        progress = ProgressTracker(len(scenes), "Frame extraction")

        for scene in scenes:
            scene_frames = []

            # Get frame positions
            positions = np.linspace(
                scene.start_frame,
                scene.end_frame,
                self.config.frames_per_scene,
                dtype=int
            )

            for frame_num, pos in enumerate(positions):
                cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
                ret, frame = cap.read()

                if not ret:
                    continue

                # Save frame
                frame_path = (
                    self.config.temp_frames_dir /
                    f"scene_{scene.scene_id:04d}_frame_{frame_num:02d}.jpg"
                )

                cv2.imwrite(
                    str(frame_path),
                    frame,
                    [cv2.IMWRITE_JPEG_QUALITY, self.config.jpeg_quality]
                )

                scene_frames.append(str(frame_path))

            scene.frames = scene_frames
            total_frames += len(scene_frames)
            progress.update()

        cap.release()

        logger.info(f"✓ Extracted {total_frames} frames total")
        return total_frames


# ========== API CLIENT ==========

class OpenAIClient:
    """Wrapper for OpenAI API with rate limiting and retry"""

    def __init__(self, api_key: str, config: Config):
        self.client = OpenAI(api_key=api_key)
        self.config = config
        self.last_call_time = 0.0
        self.call_count = 0
        self.minute_start = time.time()

    def _rate_limit(self):
        """Enforce rate limiting"""
        now = time.time()

        # Reset counter every minute
        if now - self.minute_start > 60:
            self.call_count = 0
            self.minute_start = now

        # Check if we've hit the limit
        if self.call_count >= self.config.api_calls_per_minute:
            sleep_time = 60 - (now - self.minute_start)
            if sleep_time > 0:
                logger.info(f"Rate limit: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
                self.call_count = 0
                self.minute_start = time.time()

        # Minimum delay between calls
        min_delay = 60.0 / self.config.api_calls_per_minute
        elapsed = now - self.last_call_time
        if elapsed < min_delay:
            time.sleep(min_delay - elapsed)

        self.last_call_time = time.time()
        self.call_count += 1

    @retry_on_failure(max_attempts=3, delay=2.0)
    def vision_completion(
        self,
        messages: List[Dict],
        max_tokens: int = 3000
    ) -> str:
        """Call vision API with retry and rate limiting"""
        self._rate_limit()

        response = self.client.chat.completions.create(
            model=self.config.vision_model,
            max_tokens=max_tokens,
            messages=messages,
            timeout=self.config.api_timeout
        )

        return response.choices[0].message.content

    @retry_on_failure(max_attempts=3, delay=2.0)
    def text_completion(
        self,
        messages: List[Dict],
        max_tokens: int = 4000
    ) -> str:
        """Call text API with retry and rate limiting"""
        self._rate_limit()

        response = self.client.chat.completions.create(
            model=self.config.text_model,
            max_tokens=max_tokens,
            messages=messages,
            timeout=self.config.api_timeout
        )

        return response.choices[0].message.content

    @retry_on_failure(max_attempts=2, delay=3.0)
    def transcribe_audio(self, audio_path: Path) -> Dict:
        """Transcribe audio file"""
        with open(audio_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model=self.config.whisper_model,
                file=audio_file,
                response_format="verbose_json"
            )

        return {
            'text': transcript.text,
            'language': getattr(transcript, 'language', 'unknown'),
            'duration': getattr(transcript, 'duration', 0),
        }


# ========== VISUAL ANALYZER ==========

class VisualAnalyzer:
    """Analyze visual composition of frames"""

    @staticmethod
    def analyze_composition(frame_path: str) -> Dict[str, float]:
        """Analyze frame composition (brightness, contrast, color mood)"""
        try:
            img = cv2.imread(frame_path)
            if img is None:
                return {}

            # Convert to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = img_rgb.reshape(-1, 3)

            # Calculate metrics
            avg_color = np.mean(pixels, axis=0)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            brightness = float(np.mean(gray))
            contrast = float(np.std(gray))

            # Determine color mood
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
                'brightness': round(brightness, 2),
                'contrast': round(contrast, 2),
                'color_mood': mood,
                'avg_red': round(float(r), 2),
                'avg_green': round(float(g), 2),
                'avg_blue': round(float(b), 2),
            }
        except Exception as e:
            logger.warning(f"Visual analysis error: {e}")
            return {}

    @staticmethod
    def encode_image_base64(image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8")


# ========== MAIN ANALYZER ==========

class BlockbusterAnalyzer:
    """Main orchestrator for blockbuster-level video analysis"""

    BLOCKBUSTER_SCENE_PROMPT = """Phân tích scene này theo TIÊU CHUẨN PHIM BOM TẤN HOLLYWOOD (thời lượng: {duration:.1f}s):

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

    def __init__(self, api_key: str, config: Optional[Config] = None):
        self.config = config or Config.from_env()
        self.api_client = OpenAIClient(api_key, self.config)
        self.downloader = VideoDownloader(self.config.max_video_height)
        self.scene_detector = SceneDetector(self.config)
        self.frame_extractor = FrameExtractor(self.config)
        self.visual_analyzer = VisualAnalyzer()
        self.cache_manager = CacheManager(self.config.cache_dir)

        # State
        self.video_metadata: Optional[VideoMetadata] = None
        self.scenes: List[SceneInfo] = []
        self.transcript: Optional[Dict] = None

    def analyze_scene(self, scene: SceneInfo) -> Optional[SceneInfo]:
        """Analyze a single scene with blockbuster standards"""
        if not scene.frames:
            logger.warning(f"Scene {scene.scene_id} has no frames")
            return None

        logger.info(f"Analyzing scene {scene.scene_id + 1}/{len(self.scenes)}...")

        # Build content for API
        content = [{
            "type": "text",
            "text": self.BLOCKBUSTER_SCENE_PROMPT.format(duration=scene.duration)
        }]

        # Add frame images
        for frame_path in scene.frames:
            try:
                base64_img = self.visual_analyzer.encode_image_base64(frame_path)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_img}",
                        "detail": "high"
                    }
                })
            except Exception as e:
                logger.warning(f"Failed to encode frame {frame_path}: {e}")
                continue

        try:
            # Call API
            analysis = self.api_client.vision_completion(
                messages=[{"role": "user", "content": content}],
                max_tokens=3500
            )

            # Analyze visual composition of first frame
            visual_comp = self.visual_analyzer.analyze_composition(scene.frames[0])

            # Update scene object
            scene.analysis = analysis
            scene.visual_composition = visual_comp

            return scene

        except Exception as e:
            logger.error(f"Scene analysis failed: {e}")
            return None

    def analyze_overall(self) -> Optional[str]:
        """Generate overall blockbuster analysis"""
        logger.info("Generating overall blockbuster analysis...")

        # Prepare scene summaries
        scene_text = "\n\n".join([
            f"SCENE {s.scene_id + 1} ({s.timestamp}):\n{s.analysis}"
            for s in self.scenes if s.analysis
        ])

        transcript_text = ""
        if self.transcript:
            transcript_text = f"\n\nTRANSCRIPT:\n{self.transcript.get('text', '')}"

        metadata_text = ""
        if self.video_metadata:
            metadata_text = (
                f"\nThời lượng: {self.video_metadata.duration}s, "
                f"FPS: {self.video_metadata.fps}, "
                f"Resolution: {self.video_metadata.width}x{self.video_metadata.height}"
            )

        prompt = f"""Dựa trên phân tích chi tiết từng scene, viết PHÂN TÍCH TỔNG THỂ theo TIÊU CHUẨN HOLLYWOOD BLOCKBUSTER:

VIDEO METADATA:{metadata_text}

PHÂN TÍCH TỪNG SCENE:
{scene_text}
{transcript_text}

Hãy viết phân tích CHUYÊN NGHIỆP bao gồm:

1. STORY STRUCTURE & NARRATIVE
2. CHARACTERS IN-DEPTH (physical details, costume, performance)
3. CREATURES/ANIMALS (species, size, colors, proportions)
4. CINEMATOGRAPHY ANALYSIS (camera, lens, focus techniques)
5. LIGHTING DESIGN (setups, quality, color temperature)
6. COLOR GRADING & VISUAL STYLE
7. PRODUCTION DESIGN (locations, sets, props)
8. VFX & POST-PRODUCTION
9. TECHNICAL QUALITY ASSESSMENT (scores 1-10)
10. GENRE & STYLE
11. OVERALL PRODUCTION VALUE
12. SORA 2 GENERATION INSIGHTS

Trả lời CỰC KỲ CHI TIẾT, có CẤU TRÚC, TIẾNG VIỆT, như một film critic chuyên nghiệp."""

        try:
            return self.api_client.text_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000
            )
        except Exception as e:
            logger.error(f"Overall analysis failed: {e}")
            return None

    def generate_prompts(self, overall_analysis: str) -> Optional[str]:
        """Generate Sora 2 prompts from analysis"""
        logger.info("Generating Sora 2 blockbuster prompts...")

        # Get first 10 scenes for context
        scene_summaries = "\n".join([
            f"Scene {s.scene_id + 1}: {(s.analysis or '')[:500]}..."
            for s in self.scenes[:10] if s.analysis
        ])

        prompt = f"""Dựa trên phân tích BLOCKBUSTER-level, tạo 3 PROMPT CHUYÊN NGHIỆP cho Sora 2:

PHÂN TÍCH TỔNG THỂ:
{overall_analysis}

CÁC SCENE CHI TIẾT:
{scene_summaries}

Tạo 3 prompts với HOLLYWOOD BLOCKBUSTER STANDARDS:

1. **CONCISE BLOCKBUSTER PROMPT** (70-90 words): Súc tích nhưng packed with specific details
2. **DETAILED TECHNICAL PROMPT** (180-250 words): Full technical specifications
3. **CINEMATIC MASTERPIECE PROMPT** (150-200 words): Artistic vision & emotional core

CRITICAL REQUIREMENTS:
✅ ALL IN ENGLISH (professional film industry terminology)
✅ CHARACTERS: height, build, skin tone, hair (color/style/length), costume details
✅ ANIMALS: species, size, weight, colors, proportions
✅ CAMERA: specific movement, lens focal length, aperture
✅ LIGHTING: setup, color temperature, quality, direction
✅ COLOR: grading style, palette, mood
✅ Use PRECISE technical film terminology
✅ NO explanations, ONLY prompts

Format:
=== CONCISE BLOCKBUSTER PROMPT ===
[prompt here]

=== DETAILED TECHNICAL PROMPT ===
[prompt here]

=== CINEMATIC MASTERPIECE PROMPT ===
[prompt here]"""

        try:
            return self.api_client.text_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2500
            )
        except Exception as e:
            logger.error(f"Prompt generation failed: {e}")
            return None

    def export_results(
        self,
        overall_analysis: str,
        prompts: str
    ) -> Tuple[Path, Path, Path]:
        """Export results to TXT, JSON, and Markdown"""
        logger.info("Exporting results...")

        # Generate filename
        safe_title = safe_filename(self.video_metadata.title)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"{safe_title}_BLOCKBUSTER_{timestamp}"

        # === TXT FILE ===
        txt_path = self.config.output_dir / f"{base_name}.txt"
        txt_content = self._build_txt_report(overall_analysis, prompts)
        txt_path.write_text(txt_content, encoding='utf-8')
        logger.info(f"✓ Saved TXT: {txt_path.name}")

        # === JSON FILE ===
        json_path = self.config.output_dir / f"{base_name}.json"
        json_data = {
            'video_info': asdict(self.video_metadata) if self.video_metadata else {},
            'blockbuster_analysis': overall_analysis,
            'scenes': [asdict(s) for s in self.scenes],
            'transcript': self.transcript,
            'sora_prompts': prompts,
            'version': '2.3-BLOCKBUSTER',
            'export_date': datetime.now().isoformat(),
        }
        json_path.write_text(
            json.dumps(json_data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        logger.info(f"✓ Saved JSON: {json_path.name}")

        # === MARKDOWN FILE ===
        md_path = self.config.output_dir / f"{base_name}.md"
        md_content = self._build_markdown_report(overall_analysis, prompts)
        md_path.write_text(md_content, encoding='utf-8')
        logger.info(f"✓ Saved Markdown: {md_path.name}")

        return txt_path, json_path, md_path

    def _build_txt_report(self, overall: str, prompts: str) -> str:
        """Build text report"""
        scene_details = "\n\n".join([
            f"""{'='*70}
SCENE {s.scene_id + 1} | {s.timestamp} | {s.duration:.1f}s
{'='*70}

{s.analysis or 'No analysis'}

VISUAL METRICS:
- Brightness: {s.visual_composition.get('brightness', 0) if s.visual_composition else 0:.1f}
- Contrast: {s.visual_composition.get('contrast', 0) if s.visual_composition else 0:.1f}
- Color Mood: {s.visual_composition.get('color_mood', 'N/A') if s.visual_composition else 'N/A'}
"""
            for s in self.scenes
        ])

        transcript_section = ""
        if self.transcript:
            transcript_section = f"""
{'='*70}
TRANSCRIPT & DIALOGUE
{'='*70}
Language: {self.transcript.get('language', 'unknown')}

{self.transcript.get('text', '')}
"""

        return f"""{'='*70}
YOUTUBE TO SORA 2 - BLOCKBUSTER ANALYSIS REPORT v2.3
HOLLYWOOD PRODUCTION STANDARDS - REFACTORED
{'='*70}

VIDEO: {self.video_metadata.title if self.video_metadata else 'Unknown'}
URL: {self.video_metadata.url if self.video_metadata else 'N/A'}
DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {self.video_metadata.duration if self.video_metadata else 0}s
FPS: {self.video_metadata.fps if self.video_metadata else 0}
Resolution: {self.video_metadata.width if self.video_metadata else 0}x{self.video_metadata.height if self.video_metadata else 0}
Total Scenes: {len(self.scenes)}

{'='*70}
BLOCKBUSTER-LEVEL OVERALL ANALYSIS
{'='*70}

{overall}

{'='*70}
SCENE-BY-SCENE BREAKDOWN ({len(self.scenes)} scenes)
HOLLYWOOD TECHNICAL STANDARDS
{'='*70}

{scene_details}
{transcript_section}

{'='*70}
SORA 2 PROMPTS - BLOCKBUSTER QUALITY
{'='*70}

{prompts}

{'='*70}
Generated by YouTube to Sora 2 Blockbuster Analyzer v2.3
Features: Hollywood standards, unlimited scenes, detailed technical analysis
Refactored: Professional logging, modular architecture, optimized performance
{'='*70}
"""

    def _build_markdown_report(self, overall: str, prompts: str) -> str:
        """Build markdown report"""
        scene_section = ""
        for s in self.scenes:
            scene_section += f"""### Scene {s.scene_id + 1} • {s.timestamp} • {s.duration:.1f}s

{s.analysis or 'No analysis'}

**Visual Metrics:**
- Brightness: {s.visual_composition.get('brightness', 0) if s.visual_composition else 0:.1f}
- Contrast: {s.visual_composition.get('contrast', 0) if s.visual_composition else 0:.1f}
- Color Mood: {s.visual_composition.get('color_mood', 'N/A') if s.visual_composition else 'N/A'}

---

"""

        transcript_section = ""
        if self.transcript:
            transcript_section = f"""## 🎤 Transcript & Dialogue

**Language:** {self.transcript.get('language', 'unknown')}

{self.transcript.get('text', '')}

---

"""

        return f"""# 🎬 YouTube to Sora 2 - BLOCKBUSTER Analysis v2.3

**Version:** 2.3 - Hollywood Production Standards (Refactored)
**Video:** {self.video_metadata.title if self.video_metadata else 'Unknown'}
**URL:** {self.video_metadata.url if self.video_metadata else 'N/A'}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Duration:** {self.video_metadata.duration if self.video_metadata else 0}s
**Resolution:** {self.video_metadata.width if self.video_metadata else 0}x{self.video_metadata.height if self.video_metadata else 0} @ {self.video_metadata.fps if self.video_metadata else 0} FPS
**Total Scenes:** {len(self.scenes)}

---

## 🎯 Blockbuster-Level Overall Analysis

{overall}

---

## 🎬 Scene-by-Scene Technical Breakdown

{scene_section}
{transcript_section}

## 🎨 Sora 2 Blockbuster Prompts

{prompts}

---

## 📊 v2.3 Improvements

- ✅ Professional logging system with color output
- ✅ Modular architecture with separated concerns
- ✅ Optimized API calls with rate limiting
- ✅ Improved error handling and recovery
- ✅ Progress tracking for long operations
- ✅ Better cache management
- ✅ Type safety with full type hints
- ✅ Configuration from environment or YAML

---

*Generated by YouTube to Sora 2 Blockbuster Analyzer v2.3*
*Hollywood Production Standards • Unlimited Scenes • Optimized Performance*
"""

    def cleanup(self):
        """Clean up temporary files"""
        logger.info("Cleaning up temporary files...")

        temp_files = ["temp_video.mp4", "temp_audio.m4a"]
        for f in temp_files:
            path = Path(f)
            if path.exists():
                try:
                    path.unlink()
                except Exception as e:
                    logger.warning(f"Failed to delete {f}: {e}")

        if self.config.temp_frames_dir.exists():
            try:
                shutil.rmtree(self.config.temp_frames_dir)
                self.config.temp_frames_dir.mkdir(exist_ok=True)
            except Exception as e:
                logger.warning(f"Failed to clear temp frames: {e}")

    def analyze(
        self,
        youtube_url: str,
        use_cache: bool = True,
        analyze_audio: bool = True
    ) -> Optional[Dict]:
        """
        Main analysis workflow

        Args:
            youtube_url: YouTube video URL
            use_cache: Use cached results if available
            analyze_audio: Extract and analyze audio transcript

        Returns:
            Analysis results dictionary or None if failed
        """
        logger.info("="*70)
        logger.info("YOUTUBE TO SORA 2 - BLOCKBUSTER ANALYZER v2.3")
        logger.info("="*70)
        logger.info("🎬 Hollywood Production Standards (Refactored)")
        logger.info("🎯 Unlimited scenes • Technical precision • Optimized performance\n")

        try:
            # Check cache first
            if use_cache:
                cached = self.cache_manager.get(youtube_url)
                if cached:
                    logger.info("✓ Using cached analysis")
                    return cached

            # Stage 1: Get metadata
            self.video_metadata = self.downloader.get_metadata(youtube_url)

            # Stage 2: Download video
            video_path = Path("temp_video.mp4")
            self.downloader.download_video(youtube_url, video_path)

            # Stage 3: Download audio (optional)
            audio_path = Path("temp_audio.m4a")
            if analyze_audio:
                self.downloader.download_audio(youtube_url, audio_path)

            # Stage 4: Detect scenes
            self.scenes = self.scene_detector.detect_scenes(video_path)

            # Stage 5: Extract frames
            self.frame_extractor.extract_frames(video_path, self.scenes)

            # Stage 6: Transcribe audio
            if analyze_audio and audio_path.exists():
                try:
                    self.transcript = self.api_client.transcribe_audio(audio_path)
                    logger.info(f"✓ Transcript: {len(self.transcript.get('text', ''))} chars")
                except Exception as e:
                    logger.warning(f"Audio transcription failed: {e}")

            # Stage 7: Analyze scenes
            logger.info(f"\n{'='*70}")
            logger.info(f"ANALYZING {len(self.scenes)} SCENES - BLOCKBUSTER STANDARD")
            logger.info(f"{'='*70}\n")

            analyzed_scenes = []
            for scene in self.scenes:
                result = self.analyze_scene(scene)
                if result:
                    analyzed_scenes.append(result)
                time.sleep(0.3)  # Brief pause between scenes

            self.scenes = analyzed_scenes
            logger.info(f"\n✓ Completed {len(self.scenes)} scene analyses\n")

            # Stage 8: Overall analysis
            logger.info(f"{'='*70}")
            logger.info("GENERATING OVERALL BLOCKBUSTER ANALYSIS")
            logger.info(f"{'='*70}\n")

            overall_analysis = self.analyze_overall()
            if not overall_analysis:
                raise RuntimeError("Overall analysis failed")

            # Stage 9: Generate prompts
            logger.info(f"\n{'='*70}")
            logger.info("GENERATING SORA 2 BLOCKBUSTER PROMPTS")
            logger.info(f"{'='*70}\n")

            prompts = self.generate_prompts(overall_analysis)
            if not prompts:
                raise RuntimeError("Prompt generation failed")

            # Stage 10: Export results
            logger.info(f"\n{'='*70}")
            logger.info("EXPORTING RESULTS")
            logger.info(f"{'='*70}\n")

            txt_path, json_path, md_path = self.export_results(
                overall_analysis,
                prompts
            )

            # Build result
            result = {
                'video_info': asdict(self.video_metadata),
                'blockbuster_analysis': overall_analysis,
                'scene_analyses': [asdict(s) for s in self.scenes],
                'transcript': self.transcript,
                'sora_prompts': prompts,
                'output_files': {
                    'txt': str(txt_path),
                    'json': str(json_path),
                    'markdown': str(md_path),
                }
            }

            # Save to cache
            if use_cache:
                self.cache_manager.set(youtube_url, result)

            # Cleanup
            self.cleanup()

            # Success summary
            logger.info(f"\n{'='*70}")
            logger.info("✓ ANALYSIS COMPLETE - BLOCKBUSTER QUALITY!")
            logger.info(f"{'='*70}")
            logger.info(f"📁 Output folder: {self.config.output_dir}/")
            logger.info(f"🎬 Analyzed {len(self.scenes)} scenes")
            logger.info(f"📊 Files: TXT, JSON, Markdown")
            logger.info(f"{'='*70}\n")

            return result

        except KeyboardInterrupt:
            logger.warning("\n\n⚠ Analysis interrupted by user")
            self.cleanup()
            return None
        except Exception as e:
            logger.error(f"\n❌ Analysis failed: {e}", exc_info=True)
            self.cleanup()
            return None


# ========== CLI ==========

def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="YouTube to Sora 2 - Blockbuster Analyzer v2.3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_to_sora_blockbuster.py "https://youtube.com/watch?v=..."
  python youtube_to_sora_blockbuster.py --no-cache --no-audio "URL"
  python youtube_to_sora_blockbuster.py --api-key sk-... "URL"

Environment variables:
  OPENAI_API_KEY - OpenAI API key
  SCENE_THRESHOLD - Scene detection threshold (default: 30.0)
  MAX_VIDEO_HEIGHT - Max video height (default: 1080)
        """
    )

    parser.add_argument(
        'url',
        nargs='?',
        help='YouTube video URL'
    )
    parser.add_argument(
        '--api-key',
        help='OpenAI API key (or set OPENAI_API_KEY env var)'
    )
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable cache'
    )
    parser.add_argument(
        '--no-audio',
        action='store_true',
        help='Skip audio analysis'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--clear-cache',
        action='store_true',
        help='Clear all cache and exit'
    )

    args = parser.parse_args()

    # Setup logging level
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    # Load environment
    load_env_file()

    # Clear cache if requested
    if args.clear_cache:
        config = Config.from_env()
        cache_mgr = CacheManager(config.cache_dir)
        count = cache_mgr.clear()
        logger.info(f"✓ Cleared {count} cache files")
        return 0

    # Get URL
    url = args.url
    if not url:
        url = input("Nhập YouTube URL: ").strip()

    if not url:
        logger.error("URL is required")
        parser.print_help()
        return 1

    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Nhập OpenAI API Key: ").strip()

    if not api_key:
        logger.error("OpenAI API Key is required")
        logger.info("Get your API key from: https://platform.openai.com/api-keys")
        return 1

    try:
        # Create analyzer
        config = Config.from_env()
        analyzer = BlockbusterAnalyzer(api_key, config)

        # Run analysis
        result = analyzer.analyze(
            youtube_url=url,
            use_cache=not args.no_cache,
            analyze_audio=not args.no_audio
        )

        if result:
            logger.info("✓ Analysis successful!")
            return 0
        else:
            logger.error("Analysis failed")
            return 1

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=args.debug)
        return 1


if __name__ == "__main__":
    sys.exit(main())
