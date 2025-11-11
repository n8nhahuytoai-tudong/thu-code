"""
Module để tạo báo cáo phân tích video
Hỗ trợ export sang JSON, HTML, Markdown
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import os


class ReportGenerator:
    """Tạo báo cáo phân tích video"""

    def __init__(self, output_dir: str = "./output/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(
        self,
        video_info: Dict,
        scenes: List[Dict],
        formats: List[str] = ["json", "html", "markdown"]
    ) -> Dict[str, str]:
        """
        Tạo báo cáo đầy đủ

        Args:
            video_info: Thông tin về video
            scenes: List các scene đã phân tích
            formats: Danh sách format cần export

        Returns:
            Dict với key là format và value là đường dẫn file
        """
        report_data = {
            'video_info': video_info,
            'scenes': scenes,
            'summary': self._generate_summary(video_info, scenes),
            'generated_at': datetime.now().isoformat()
        }

        video_name = Path(video_info['filename']).stem
        output_files = {}

        if "json" in formats:
            json_path = self._export_json(report_data, video_name)
            output_files['json'] = json_path

        if "html" in formats:
            html_path = self._export_html(report_data, video_name)
            output_files['html'] = html_path

        if "markdown" in formats:
            md_path = self._export_markdown(report_data, video_name)
            output_files['markdown'] = md_path

        return output_files

    def _generate_summary(self, video_info: Dict, scenes: List[Dict]) -> Dict:
        """Tạo tóm tắt thống kê"""
        total_duration = video_info.get('duration', 0)
        num_scenes = len(scenes)

        avg_scene_duration = total_duration / num_scenes if num_scenes > 0 else 0

        # Tìm scene ngắn nhất và dài nhất
        shortest_scene = min(scenes, key=lambda x: x['duration']) if scenes else None
        longest_scene = max(scenes, key=lambda x: x['duration']) if scenes else None

        return {
            'total_scenes': num_scenes,
            'total_duration': total_duration,
            'average_scene_duration': avg_scene_duration,
            'shortest_scene': {
                'number': shortest_scene['scene_number'],
                'duration': shortest_scene['duration']
            } if shortest_scene else None,
            'longest_scene': {
                'number': longest_scene['scene_number'],
                'duration': longest_scene['duration']
            } if longest_scene else None
        }

    def _export_json(self, report_data: Dict, video_name: str) -> str:
        """Export sang JSON"""
        output_path = self.output_dir / f"{video_name}_report.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"✓ Đã tạo báo cáo JSON: {output_path}")
        return str(output_path)

    def _export_html(self, report_data: Dict, video_name: str) -> str:
        """Export sang HTML với styling đẹp"""
        output_path = self.output_dir / f"{video_name}_report.html"

        html_content = self._generate_html_content(report_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ Đã tạo báo cáo HTML: {output_path}")
        return str(output_path)

    def _export_markdown(self, report_data: Dict, video_name: str) -> str:
        """Export sang Markdown"""
        output_path = self.output_dir / f"{video_name}_report.md"

        md_content = self._generate_markdown_content(report_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✓ Đã tạo báo cáo Markdown: {output_path}")
        return str(output_path)

    def _generate_html_content(self, report_data: Dict) -> str:
        """Tạo nội dung HTML"""
        video_info = report_data['video_info']
        scenes = report_data['scenes']
        summary = report_data['summary']

        html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phân tích Video: {video_info['filename']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}

        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .info-item {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
        }}

        .info-label {{
            font-weight: bold;
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}

        .info-value {{
            color: #2c3e50;
            font-size: 1.2em;
        }}

        .scene-card {{
            background: #fff;
            border: 1px solid #ddd;
            border-left: 4px solid #3498db;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .scene-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        .scene-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .scene-number {{
            background: #3498db;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}

        .scene-time {{
            color: #7f8c8d;
            font-size: 0.95em;
        }}

        .scene-description {{
            color: #555;
            line-height: 1.8;
            white-space: pre-line;
        }}

        .frames-container {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}

        .frame-box {{
            flex: 1;
            min-width: 200px;
            text-align: center;
        }}

        .frame-box img {{
            width: 100%;
            border-radius: 5px;
            border: 2px solid #ecf0f1;
        }}

        .frame-label {{
            margin-top: 5px;
            font-size: 0.85em;
            color: #7f8c8d;
            font-weight: bold;
        }}

        .summary-stats {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}

        .summary-stats h2 {{
            color: white;
            margin-top: 0;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .stat-item {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: bold;
        }}

        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}

        .timestamp {{
            color: #95a5a6;
            font-size: 0.85em;
            margin-top: 30px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📹 Phân tích Video: {video_info['filename']}</h1>

        <div class="summary-stats">
            <h2>📊 Tổng quan</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{summary['total_scenes']}</div>
                    <div class="stat-label">Cảnh</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{self._format_duration(summary['total_duration'])}</div>
                    <div class="stat-label">Tổng thời lượng</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{summary['average_scene_duration']:.1f}s</div>
                    <div class="stat-label">TB thời lượng/cảnh</div>
                </div>
            </div>
        </div>

        <h2>ℹ️ Thông tin Video</h2>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Độ phân giải</div>
                <div class="info-value">{video_info['width']} × {video_info['height']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Frame Rate</div>
                <div class="info-value">{video_info['fps']:.2f} fps</div>
            </div>
            <div class="info-item">
                <div class="info-label">Tổng số Frames</div>
                <div class="info-value">{video_info['total_frames']:,}</div>
            </div>
        </div>

        <h2>🎬 Chi tiết từng cảnh</h2>
"""

        # Add scenes
        for scene in scenes:
            start_time = self._format_duration(scene['start_time'])
            end_time = self._format_duration(scene['end_time'])
            duration = scene['duration']

            html += f"""
        <div class="scene-card">
            <div class="scene-header">
                <div class="scene-number">Cảnh {scene['scene_number']}</div>
                <div class="scene-time">⏱️ {start_time} - {end_time} ({duration:.1f}s)</div>
            </div>
            <div class="scene-description">{scene.get('description', 'Chưa có mô tả')}</div>
"""

            # Add frames if available
            if 'frames' in scene and scene['frames']:
                html += '            <div class="frames-container">\n'

                for frame_type, frame_path in scene['frames'].items():
                    if os.path.exists(frame_path):
                        # Convert to relative path for HTML
                        rel_path = os.path.relpath(frame_path, self.output_dir)
                        label = {
                            'first': 'Frame đầu',
                            'middle': 'Frame giữa',
                            'last': 'Frame cuối'
                        }.get(frame_type, frame_type.title())

                        html += f"""                <div class="frame-box">
                    <img src="../{rel_path}" alt="{label}">
                    <div class="frame-label">{label}</div>
                </div>
"""

                html += '            </div>\n'

            html += '        </div>\n'

        html += f"""
        <div class="timestamp">
            Báo cáo được tạo lúc: {report_data['generated_at']}
        </div>
    </div>
</body>
</html>
"""

        return html

    def _generate_markdown_content(self, report_data: Dict) -> str:
        """Tạo nội dung Markdown"""
        video_info = report_data['video_info']
        scenes = report_data['scenes']
        summary = report_data['summary']

        md = f"""# 📹 Phân tích Video: {video_info['filename']}

## 📊 Tổng quan

- **Tổng số cảnh**: {summary['total_scenes']}
- **Thời lượng**: {self._format_duration(summary['total_duration'])}
- **Trung bình/cảnh**: {summary['average_scene_duration']:.1f}s

## ℹ️ Thông tin Video

| Thuộc tính | Giá trị |
|------------|---------|
| Độ phân giải | {video_info['width']} × {video_info['height']} |
| Frame Rate | {video_info['fps']:.2f} fps |
| Tổng số Frames | {video_info['total_frames']:,} |
| Thời lượng | {self._format_duration(video_info['duration'])} |

---

## 🎬 Chi tiết từng cảnh

"""

        for scene in scenes:
            start_time = self._format_duration(scene['start_time'])
            end_time = self._format_duration(scene['end_time'])

            md += f"""### Cảnh {scene['scene_number']}

**⏱️ Thời gian**: {start_time} - {end_time} ({scene['duration']:.1f}s)

**📝 Mô tả**:

{scene.get('description', 'Chưa có mô tả')}

"""

            # Add frame paths
            if 'frames' in scene and scene['frames']:
                md += "**🖼️ Frames**:\n\n"
                for frame_type, frame_path in scene['frames'].items():
                    if os.path.exists(frame_path):
                        rel_path = os.path.relpath(frame_path, self.output_dir)
                        label = {
                            'first': 'Frame đầu',
                            'middle': 'Frame giữa',
                            'last': 'Frame cuối'
                        }.get(frame_type, frame_type.title())
                        md += f"- {label}: `{rel_path}`\n"

            md += "\n---\n\n"

        md += f"""
## 📄 Metadata

- **Báo cáo tạo lúc**: {report_data['generated_at']}
"""

        return md

    def _format_duration(self, seconds: float) -> str:
        """Format thời gian"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


if __name__ == "__main__":
    # Test
    generator = ReportGenerator()

    video_info = {
        'filename': 'test_video.mp4',
        'width': 1920,
        'height': 1080,
        'fps': 30.0,
        'total_frames': 900,
        'duration': 30.0
    }

    scenes = [
        {
            'scene_number': 1,
            'start_time': 0.0,
            'end_time': 10.0,
            'duration': 10.0,
            'description': 'Test scene 1',
            'frames': {}
        }
    ]

    reports = generator.generate_report(video_info, scenes)
    print("Generated reports:", reports)
