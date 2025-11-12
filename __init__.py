"""
ComfyUI Custom Nodes for OpenAI Sora API Plus
Author: Claude AI Assistant
Version: 1.0.0
"""

from .sora_nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Web directory for custom UI elements (optional)
WEB_DIRECTORY = "./web"

print("\033[34m[Sora API]\033[0m OpenAI Sora API Plus nodes loaded successfully!")
print("\033[34m[Sora API]\033[0m Available nodes:")
print("\033[34m[Sora API]\033[0m   - OpenAI Sora API Plus ⚡")
print("\033[34m[Sora API]\033[0m   - Sora Video Downloader 📥")
print("\033[34m[Sora API]\033[0m   - Sora Task Status 📊")
