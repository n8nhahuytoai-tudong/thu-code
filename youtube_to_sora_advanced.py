#!/usr/bin/env python3
"""
YouTube Video Analyzer to Sora 2 Prompt Generator - ADVANCED VERSION
Phân tích video chi tiết với scene detection, audio analysis, và nhiều tính năng nâng cao
"""

import os
import sys
import subprocess
import cv2
import base64
import numpy as np
from pathlib import Path
import json
from openai import OpenAI
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import hashlib
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

# Khởi tạo OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AdvancedYouTubeToSoraPrompt:
    def __init__(self, api_key=None, cache_dir="cache"):
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI()

        self.video_path = None
        self.audio_path = None
        self.frames = []
        self.scenes = []
        self.youtube_url = None
        self.video_title = None
        self.cache_dir = cache_dir
        self.video_metadata = {}

        # Tạo thư mục cache
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs("output_results", exist_ok=True)
        os.makedirs("temp_frames", exist_ok=True)

    def get_cache_key(self, url):
        """Tạo cache key từ URL"""
        return hashlib.md5(url.encode()).hexdigest()

    def save_to_cache(self, key, data):
        """Lưu dữ liệu vào cache"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_cache(self, key):
        """Load dữ liệu từ cache"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def print_progress(self, message, step=None, total_steps=None):
        """In progress với format đẹp"""
        if step and total_steps:
            progress = f"[{step}/{total_steps}]"
            print(f"{progress} {message}")
        else:
            print(f"• {message}")

    def get_video_metadata(self, youtube_url):
        """Lấy metadata chi tiết từ YouTube"""
        self.print_progress("Đang lấy thông tin video...")

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
                    'duration': metadata.get('duration'),
                    'description': metadata.get('description', '')[:500],  # First 500 chars
                    'uploader': metadata.get('uploader'),
                    'width': metadata.get('width'),
                    'height': metadata.get('height'),
                    'fps': metadata.get('fps'),
                }
                return self.video_metadata
        except Exception as e:
            self.print_progress(f"Không lấy được metadata: {e}")

        # Fallback
        self.video_title = f"Video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return {}

    def download_video(self, youtube_url):
        """Tải video và audio riêng biệt"""
        self.print_progress("Đang tải video và audio...")

        try:
            video_output = "temp_video.mp4"
            audio_output = "temp_audio.m4a"

            # Tải video (chất lượng tốt nhưng không quá lớn)
            subprocess.run(
                ["yt-dlp", "-f", "best[height<=1080][ext=mp4]", "-o", video_output, youtube_url],
                check=True,
                capture_output=True
            )

            # Tải audio riêng
            subprocess.run(
                ["yt-dlp", "-f", "bestaudio[ext=m4a]", "-o", audio_output, youtube_url],
                check=True,
                capture_output=True
            )

            self.video_path = video_output
            self.audio_path = audio_output
            self.print_progress(f"✓ Video và audio đã tải xong")
            return video_output

        except Exception as e:
            self.print_progress(f"✗ Lỗi tải video: {e}")
            return None

    def extract_audio_transcript(self):
        """Trích xuất transcript từ audio bằng Whisper API"""
        if not self.audio_path or not os.path.exists(self.audio_path):
            return None

        self.print_progress("Đang phân tích audio và transcript...")

        try:
            # Sử dụng Whisper API của OpenAI
            with open(self.audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    language="vi"  # Có thể auto-detect
                )

            result = {
                'text': transcript.text,
                'language': getattr(transcript, 'language', 'unknown'),
                'duration': getattr(transcript, 'duration', 0),
            }

            self.print_progress(f"✓ Transcript đã trích xuất ({len(result['text'])} ký tự)")
            return result

        except Exception as e:
            self.print_progress(f"⚠ Không thể trích xuất transcript: {e}")
            return None

    def detect_scenes(self, threshold=30.0, min_scene_length=15):
        """Phát hiện scenes bằng scene detection thông minh"""
        if not self.video_path or not os.path.exists(self.video_path):
            return []

        self.print_progress("Đang phát hiện scenes...")

        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        prev_frame = None
        scene_boundaries = [0]
        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Downsample để tính nhanh hơn
            small_frame = cv2.resize(frame, (320, 180))
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

            if prev_frame is not None:
                # Tính histogram difference
                diff = cv2.absdiff(gray, prev_frame)
                mean_diff = np.mean(diff)

                # Nếu sự khác biệt lớn hơn threshold -> scene mới
                if mean_diff > threshold:
                    # Đảm bảo scene đủ dài
                    if frame_idx - scene_boundaries[-1] > min_scene_length:
                        scene_boundaries.append(frame_idx)

            prev_frame = gray
            frame_idx += 1

            # Progress
            if frame_idx % 100 == 0:
                progress = (frame_idx / total_frames) * 100
                print(f"\r  Đang xử lý: {progress:.1f}%", end='')

        print()  # New line
        scene_boundaries.append(total_frames - 1)
        cap.release()

        # Tạo thông tin scenes
        scenes = []
        for i in range(len(scene_boundaries) - 1):
            start_frame = scene_boundaries[i]
            end_frame = scene_boundaries[i + 1]
            scenes.append({
                'scene_id': i,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'start_time': start_frame / fps,
                'end_time': end_frame / fps,
                'duration': (end_frame - start_frame) / fps
            })

        self.scenes = scenes
        self.print_progress(f"✓ Đã phát hiện {len(scenes)} scenes")
        return scenes

    def extract_key_frames_from_scenes(self, frames_per_scene=3):
        """Trích xuất key frames từ mỗi scene"""
        if not self.scenes:
            self.detect_scenes()

        self.print_progress(f"Đang trích xuất {frames_per_scene} frames từ mỗi scene...")

        cap = cv2.VideoCapture(self.video_path)
        all_frames = []

        for idx, scene in enumerate(self.scenes):
            scene_frames = []
            start = scene['start_frame']
            end = scene['end_frame']

            # Lấy frames đều từ scene
            frame_positions = np.linspace(start, end, frames_per_scene, dtype=int)

            for pos in frame_positions:
                cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
                ret, frame = cap.read()

                if ret:
                    frame_path = f"temp_frames/scene_{idx}_frame_{len(scene_frames)}.jpg"
                    cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                    scene_frames.append(frame_path)

            scene['frames'] = scene_frames
            all_frames.extend(scene_frames)

        cap.release()
        self.frames = all_frames
        self.print_progress(f"✓ Đã trích xuất {len(all_frames)} frames tổng cộng")
        return all_frames

    def analyze_visual_composition(self, frame_path):
        """Phân tích composition, màu sắc, lighting của frame"""
        try:
            img = cv2.imread(frame_path)

            # Phân tích màu sắc dominant
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = img_rgb.reshape(-1, 3)

            # Tính màu trung bình
            avg_color = np.mean(pixels, axis=0)

            # Tính brightness
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)

            # Tính contrast
            contrast = np.std(gray)

            return {
                'dominant_color_rgb': avg_color.tolist(),
                'brightness': float(brightness),
                'contrast': float(contrast),
                'color_mood': self._classify_color_mood(avg_color, brightness)
            }
        except Exception as e:
            return {}

    def _classify_color_mood(self, rgb, brightness):
        """Phân loại mood dựa trên màu sắc"""
        r, g, b = rgb

        if brightness < 85:
            return "dark, moody"
        elif brightness > 170:
            return "bright, airy"
        elif r > g and r > b:
            return "warm, energetic"
        elif b > r and b > g:
            return "cool, calm"
        else:
            return "balanced, natural"

    def encode_frame_to_base64(self, frame_path):
        """Chuyển frame sang base64"""
        with open(frame_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

    def analyze_scene_detailed(self, scene_data):
        """Phân tích chi tiết một scene cụ thể"""
        scene_id = scene_data['scene_id']
        frames = scene_data.get('frames', [])

        if not frames:
            return None

        self.print_progress(f"Đang phân tích scene {scene_id + 1}...", scene_id + 1, len(self.scenes))

        try:
            # Chuẩn bị content với frames của scene
            content = [
                {
                    "type": "text",
                    "text": f"""Phân tích chi tiết scene này (thời lượng: {scene_data['duration']:.1f}s):

1. MÔ TẢ HÀNH ĐỘNG: Điều gì đang xảy ra trong scene này? Hành động chính?
2. NHÂN VẬT/ĐỐI TƯỢNG: Ai/cái gì xuất hiện? Đặc điểm nổi bật?
3. CẢM XÚC & KHÔNG KHÍ: Tâm trạng, cảm xúc của scene?
4. BỐI CẢNH: Địa điểm, môi trường, bối cảnh?
5. CAMERA MOVEMENT: Camera di chuyển như thế nào? (static, pan, zoom, tracking)
6. LIGHTING & COLORS: Ánh sáng, màu sắc chủ đạo?
7. COMPOSITION: Cách bố cục hình ảnh (rule of thirds, symmetry, depth)

Trả lời ngắn gọn, chi tiết, bằng tiếng Việt."""
                }
            ]

            # Thêm frames
            for frame_path in frames:
                base64_frame = self.encode_frame_to_base64(frame_path)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_frame}",
                        "detail": "high"
                    }
                })

            # Gọi Vision API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                max_tokens=1500,
                messages=[{"role": "user", "content": content}]
            )

            analysis = response.choices[0].message.content

            # Phân tích visual composition
            visual_analysis = self.analyze_visual_composition(frames[0])

            return {
                'scene_id': scene_id,
                'analysis': analysis,
                'visual_composition': visual_analysis,
                'duration': scene_data['duration'],
                'timestamp': f"{scene_data['start_time']:.1f}s - {scene_data['end_time']:.1f}s"
            }

        except Exception as e:
            self.print_progress(f"✗ Lỗi phân tích scene {scene_id}: {e}")
            return None

    def analyze_overall_video(self, scene_analyses, transcript_data):
        """Phân tích tổng thể video dựa trên tất cả scenes và transcript"""
        self.print_progress("Đang tổng hợp phân tích tổng thể...")

        try:
            # Tổng hợp các phân tích scene
            all_scene_summaries = "\n\n".join([
                f"SCENE {s['scene_id'] + 1} ({s['timestamp']}):\n{s['analysis']}"
                for s in scene_analyses if s
            ])

            transcript_text = ""
            if transcript_data:
                transcript_text = f"\n\nTRANSCRIPT/AUDIO:\n{transcript_data.get('text', '')}"

            metadata_text = ""
            if self.video_metadata:
                duration = self.video_metadata.get('duration', 0)
                metadata_text = f"\nThời lượng video: {duration}s\nĐộ phân giải: {self.video_metadata.get('width')}x{self.video_metadata.get('height')}"

            prompt = f"""Dựa trên phân tích từng scene và transcript dưới đây, hãy viết một bản tổng hợp phân tích video hoàn chỉnh:

VIDEO METADATA:{metadata_text}

PHÂN TÍCH TỪNG SCENE:
{all_scene_summaries}
{transcript_text}

Hãy viết phân tích tổng thể bao gồm:
1. TÓNG TẮT CỐT TRUYỆN/NỘI DUNG: Nội dung chính của video
2. PHONG CÁCH HÌNH ẢNH: Đặc điểm visual, màu sắc, lighting
3. KỸ THUẬT QUAY: Camera movements, transitions
4. KHÔNG KHÍ TỔNG THỂ: Mood, tone, cảm xúc
5. THỂ LOẠI: (Documentary, Narrative, Music Video, Commercial, etc.)
6. ĐẶC ĐIỂM NỔI BẬT: Những yếu tố làm cho video này đặc biệt

Trả lời chi tiết, bằng tiếng Việt."""

            response = self.client.chat.completions.create(
                model="gpt-4o",
                max_tokens=2500,
                messages=[{"role": "user", "content": prompt}]
            )

            overall_analysis = response.choices[0].message.content
            self.print_progress("✓ Hoàn thành phân tích tổng thể")

            return overall_analysis

        except Exception as e:
            self.print_progress(f"✗ Lỗi phân tích tổng thể: {e}")
            return None

    def generate_sora_prompts(self, overall_analysis, scene_analyses):
        """Tạo nhiều variants của Sora prompts"""
        self.print_progress("Đang tạo Sora 2 prompts...")

        try:
            # Tổng hợp scene info
            scene_summaries = "\n".join([
                f"Scene {s['scene_id'] + 1}: {s['analysis'][:200]}..."
                for s in scene_analyses[:5] if s  # Chỉ lấy 5 scenes đầu
            ])

            prompt = f"""Dựa trên phân tích video này, hãy tạo 3 PHIÊN BẢN PROMPT cho Sora 2:

PHÂN TÍCH TỔNG THỂ:
{overall_analysis}

CÁC SCENE CHỦ YẾU:
{scene_summaries}

Hãy tạo 3 prompts khác nhau:

1. **PROMPT NGẮN GỌN** (50-70 từ): Tập trung vào hành động chính, súc tích
2. **PROMPT CHI TIẾT** (120-150 từ): Mô tả đầy đủ visual, camera, lighting, mood
3. **PROMPT SÁNG TẠO** (100-130 từ): Thêm yếu tố nghệ thuật, metaphor, cinematic

YÊU CẦU:
- Tất cả prompts PHẢI BẰNG TIẾNG ANH
- Rõ ràng, cụ thể, sinh động
- Phù hợp với Sora 2 (AI video generation)
- Mô tả camera movement, lighting, mood
- Không giải thích, chỉ viết prompts

Format:
=== SHORT PROMPT ===
[prompt here]

=== DETAILED PROMPT ===
[prompt here]

=== CREATIVE PROMPT ===
[prompt here]"""

            response = self.client.chat.completions.create(
                model="gpt-4o",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            prompts = response.choices[0].message.content
            self.print_progress("✓ Đã tạo 3 phiên bản prompts")

            return prompts

        except Exception as e:
            self.print_progress(f"✗ Lỗi tạo prompts: {e}")
            return None

    def save_detailed_results(self, overall_analysis, scene_analyses, transcript_data, sora_prompts):
        """Lưu kết quả chi tiết ra file"""
        try:
            safe_title = "".join(c for c in self.video_title if c.isalnum() or c in (' ', '_', '-'))[:50]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f"{safe_title}_{timestamp}"

            # ============ TXT FILE ============
            txt_path = f"output_results/{file_name}.txt"

            scene_details = "\n\n".join([
                f"""{'='*60}
SCENE {s['scene_id'] + 1} | {s['timestamp']} | Thời lượng: {s['duration']:.1f}s
{'='*60}

{s['analysis']}

VISUAL COMPOSITION:
- Brightness: {s.get('visual_composition', {}).get('brightness', 'N/A'):.1f}
- Contrast: {s.get('visual_composition', {}).get('contrast', 'N/A'):.1f}
- Color Mood: {s.get('visual_composition', {}).get('color_mood', 'N/A')}
"""
                for s in scene_analyses if s
            ])

            transcript_section = ""
            if transcript_data:
                transcript_section = f"""
{'='*60}
TRANSCRIPT & AUDIO ANALYSIS
{'='*60}

Language: {transcript_data.get('language', 'unknown')}
Duration: {transcript_data.get('duration', 0):.1f}s

TRANSCRIPT:
{transcript_data.get('text', 'N/A')}
"""

            metadata_section = ""
            if self.video_metadata:
                metadata_section = f"""
Thời lượng: {self.video_metadata.get('duration', 0)}s
Độ phân giải: {self.video_metadata.get('width')}x{self.video_metadata.get('height')}
FPS: {self.video_metadata.get('fps')}
Uploader: {self.video_metadata.get('uploader', 'N/A')}
"""

            txt_content = f"""{'='*70}
YOUTUBE TO SORA 2 - ADVANCED ANALYSIS REPORT
{'='*70}

VIDEO INFORMATION
{'='*70}

Tên video: {self.video_title}
URL: {self.youtube_url}
Thời gian phân tích: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{metadata_section}

{'='*70}
PHÂN TÍCH TỔNG THỂ
{'='*70}

{overall_analysis}

{'='*70}
PHÂN TÍCH CHI TIẾT TỪNG SCENE ({len(scene_analyses)} scenes)
{'='*70}

{scene_details}
{transcript_section}

{'='*70}
SORA 2 PROMPTS (3 VARIANTS)
{'='*70}

{sora_prompts}

{'='*70}
END OF REPORT
{'='*70}
"""

            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(txt_content)

            self.print_progress(f"✓ Đã lưu file TXT: {txt_path}")

            # ============ JSON FILE (for programmatic use) ============
            json_path = f"output_results/{file_name}.json"
            json_data = {
                'video_info': {
                    'title': self.video_title,
                    'url': self.youtube_url,
                    'metadata': self.video_metadata,
                    'analysis_date': datetime.now().isoformat()
                },
                'overall_analysis': overall_analysis,
                'scenes': scene_analyses,
                'transcript': transcript_data,
                'sora_prompts': sora_prompts
            }

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            self.print_progress(f"✓ Đã lưu file JSON: {json_path}")

            # ============ DOCX FILE ============
            try:
                from docx import Document
                from docx.shared import Pt, RGBColor, Inches
                from docx.enum.text import WD_ALIGN_PARAGRAPH

                doc = Document()

                # Title
                title = doc.add_heading('YouTube to Sora 2 - Advanced Analysis', 0)
                title.alignment = WD_ALIGN_PARAGRAPH.CENTER

                # Video Info
                doc.add_heading('Video Information', level=1)
                info_table = doc.add_table(rows=4, cols=2)
                info_table.style = 'Light Grid Accent 1'
                info_table.cell(0, 0).text = 'Title'
                info_table.cell(0, 1).text = self.video_title
                info_table.cell(1, 0).text = 'URL'
                info_table.cell(1, 1).text = self.youtube_url
                info_table.cell(2, 0).text = 'Analysis Date'
                info_table.cell(2, 1).text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                info_table.cell(3, 0).text = 'Total Scenes'
                info_table.cell(3, 1).text = str(len(scene_analyses))

                # Overall Analysis
                doc.add_heading('Overall Analysis', level=1)
                doc.add_paragraph(overall_analysis)

                # Scene Details
                doc.add_heading('Scene-by-Scene Analysis', level=1)
                for s in scene_analyses:
                    if s:
                        doc.add_heading(f"Scene {s['scene_id'] + 1} ({s['timestamp']})", level=2)
                        doc.add_paragraph(s['analysis'])

                # Transcript
                if transcript_data:
                    doc.add_heading('Transcript', level=1)
                    doc.add_paragraph(transcript_data.get('text', ''))

                # Prompts
                doc.add_heading('Sora 2 Prompts', level=1)
                doc.add_paragraph(sora_prompts)

                docx_path = f"output_results/{file_name}.docx"
                doc.save(docx_path)
                self.print_progress(f"✓ Đã lưu file DOCX: {docx_path}")

            except ImportError:
                self.print_progress("⚠ Cài python-docx để xuất file DOCX: pip install python-docx")

            return txt_path

        except Exception as e:
            self.print_progress(f"✗ Lỗi lưu file: {e}")
            return None

    def cleanup(self, keep_cache=True):
        """Dọn dẹp files tạm"""
        self.print_progress("Đang dọn dẹp files tạm...")

        if self.video_path and os.path.exists(self.video_path):
            os.remove(self.video_path)

        if self.audio_path and os.path.exists(self.audio_path):
            os.remove(self.audio_path)

        # Xóa frames
        import shutil
        if os.path.exists("temp_frames"):
            shutil.rmtree("temp_frames")
            os.makedirs("temp_frames", exist_ok=True)

        self.print_progress("✓ Đã dọn dẹp xong")

    def process(self, youtube_url, api_key=None, use_cache=True, analyze_audio=True):
        """Xử lý toàn bộ quy trình - ADVANCED VERSION"""

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            self.client = OpenAI(api_key=api_key)

        self.youtube_url = youtube_url
        cache_key = self.get_cache_key(youtube_url)

        print("\n" + "="*70)
        print("YOUTUBE TO SORA 2 - ADVANCED PROMPT GENERATOR")
        print("="*70 + "\n")

        # Check cache
        if use_cache:
            cached_data = self.load_from_cache(cache_key)
            if cached_data:
                print("✓ Tìm thấy kết quả trong cache!")
                self.video_title = cached_data['video_info']['title']
                print(f"Video: {self.video_title}\n")

                # Show cached results
                print("="*70)
                print("PHÂN TÍCH TỔNG THỂ (từ cache)")
                print("="*70)
                print(cached_data['overall_analysis'])
                print("\n" + "="*70)
                print("SORA 2 PROMPTS (từ cache)")
                print("="*70)
                print(cached_data['sora_prompts'])
                print("="*70 + "\n")

                return cached_data

        # Step 1: Get metadata
        self.get_video_metadata(youtube_url)
        print(f"\nVideo: {self.video_title}")
        if self.video_metadata.get('duration'):
            print(f"Thời lượng: {self.video_metadata['duration']}s\n")

        # Step 2: Download
        if not self.download_video(youtube_url):
            return None

        # Step 3: Scene detection
        self.detect_scenes()

        # Step 4: Extract key frames
        self.extract_key_frames_from_scenes(frames_per_scene=3)

        # Step 5: Audio transcript (optional)
        transcript_data = None
        if analyze_audio:
            transcript_data = self.extract_audio_transcript()

        # Step 6: Analyze each scene
        print("\n" + "="*70)
        print("PHÂN TÍCH CHI TIẾT TỪNG SCENE")
        print("="*70 + "\n")

        scene_analyses = []
        for scene in self.scenes:
            analysis = self.analyze_scene_detailed(scene)
            if analysis:
                scene_analyses.append(analysis)

        # Step 7: Overall analysis
        print("\n" + "="*70)
        overall_analysis = self.analyze_overall_video(scene_analyses, transcript_data)

        if overall_analysis:
            print("PHÂN TÍCH TỔNG THỂ")
            print("="*70)
            print(overall_analysis)
            print("="*70 + "\n")

        # Step 8: Generate Sora prompts
        sora_prompts = self.generate_sora_prompts(overall_analysis, scene_analyses)

        if sora_prompts:
            print("\n" + "="*70)
            print("SORA 2 PROMPTS")
            print("="*70)
            print(sora_prompts)
            print("="*70 + "\n")

        # Step 9: Save results
        self.save_detailed_results(overall_analysis, scene_analyses, transcript_data, sora_prompts)

        # Save to cache
        if use_cache:
            cache_data = {
                'video_info': {
                    'title': self.video_title,
                    'url': self.youtube_url,
                    'metadata': self.video_metadata
                },
                'overall_analysis': overall_analysis,
                'scene_analyses': scene_analyses,
                'transcript': transcript_data,
                'sora_prompts': sora_prompts
            }
            self.save_to_cache(cache_key, cache_data)
            self.print_progress("✓ Đã lưu vào cache")

        # Step 10: Cleanup
        self.cleanup()

        print("\n" + "="*70)
        print("✓ HOÀN TẤT! Kiểm tra folder 'output_results' để xem kết quả chi tiết")
        print("="*70 + "\n")

        return {
            'overall_analysis': overall_analysis,
            'scene_analyses': scene_analyses,
            'transcript': transcript_data,
            'sora_prompts': sora_prompts
        }


def main():
    """Hàm chính - Interactive mode"""
    print("\n" + "="*70)
    print("YOUTUBE TO SORA 2 - ADVANCED PROMPT GENERATOR")
    print("="*70)

    # Input
    youtube_url = input("\nNhập YouTube URL: ").strip()

    if not youtube_url:
        print("✗ URL không hợp lệ")
        return

    # API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Nhập OpenAI API Key: ").strip()

    if not api_key:
        print("✗ Cần OpenAI API Key")
        return

    # Options
    print("\n--- TÙY CHỌN ---")
    use_cache = input("Sử dụng cache? (y/n, mặc định: y): ").strip().lower() != 'n'
    analyze_audio = input("Phân tích audio/transcript? (y/n, mặc định: y): ").strip().lower() != 'n'

    # Process
    processor = AdvancedYouTubeToSoraPrompt(api_key=api_key)
    result = processor.process(
        youtube_url,
        api_key=api_key,
        use_cache=use_cache,
        analyze_audio=analyze_audio
    )

    if result:
        print("\n✓ Thành công! Kết quả đã được lưu.")
    else:
        print("\n✗ Có lỗi xảy ra trong quá trình xử lý")


if __name__ == "__main__":
    main()
