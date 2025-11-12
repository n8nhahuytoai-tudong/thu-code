"""
ComfyUI Custom Node for OpenAI Sora API Plus
Supports text-to-video and image-to-video generation using OpenAI's Sora API
"""

import os
import json
import time
import base64
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import torch
import folder_paths


class OpenAI_Sora_API_Plus:
    """
    OpenAI Sora API Plus Node for ComfyUI
    Generates videos from text prompts and optional reference images using OpenAI's Sora API
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1/sora"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "A cat sitting on a windowsill watching the rain",
                    "placeholder": "Enter your video generation prompt..."
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "placeholder": "Enter your OpenAI API key (or set OPENAI_API_KEY env var)"
                }),
                "duration": (["5s", "10s", "15s", "20s"], {
                    "default": "10s"
                }),
                "resolution": (["1920x1080", "1080x1920", "1280x720", "720x1280", "1024x1024"], {
                    "default": "1920x1080"
                }),
                "aspect_ratio": (["16:9", "9:16", "1:1", "4:3", "3:4"], {
                    "default": "16:9"
                }),
                "fps": ([24, 30, 60], {
                    "default": 30
                }),
                "quality": (["standard", "high", "ultra"], {
                    "default": "high"
                }),
            },
            "optional": {
                "reference_image": ("IMAGE",),
                "negative_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Enter negative prompt (optional)..."
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 0xffffffffffffffff
                }),
                "style_preset": (["none", "cinematic", "anime", "photographic", "digital_art", "3d_model"], {
                    "default": "none"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("video_url", "task_id", "status")
    FUNCTION = "generate_video"
    CATEGORY = "Sora API"
    OUTPUT_NODE = True

    DESCRIPTION = """
    Generate videos using OpenAI Sora API Plus.

    Supports:
    - Text-to-video generation
    - Image-to-video generation (with reference image)
    - Multiple resolutions and aspect ratios
    - Quality and style control
    - Seed control for reproducibility
    """

    def encode_image(self, image_tensor):
        """Convert ComfyUI image tensor to base64 encoded string"""
        # ComfyUI image format: [B, H, W, C] in range [0, 1]
        if image_tensor is None:
            return None

        # Take first image if batch
        img = image_tensor[0]

        # Convert to numpy and scale to [0, 255]
        img_np = (img.cpu().numpy() * 255).astype(np.uint8)

        # Convert to PIL Image
        pil_img = Image.fromarray(img_np)

        # Encode to base64
        buffered = BytesIO()
        pil_img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        return f"data:image/png;base64,{img_base64}"

    def generate_video(self, prompt, api_key, duration, resolution, aspect_ratio, fps, quality,
                       reference_image=None, negative_prompt="", seed=-1, style_preset="none"):
        """
        Main function to generate video using Sora API
        """

        # Use provided API key or fallback to environment variable
        final_api_key = api_key if api_key.strip() else self.api_key

        if not final_api_key:
            error_msg = "API key not provided. Set OPENAI_API_KEY environment variable or provide in node."
            print(f"[Sora API Error] {error_msg}")
            return ("", "", f"error: {error_msg}")

        # Prepare request payload
        payload = {
            "model": "sora-1.0-turbo",
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "fps": fps,
            "quality": quality,
        }

        # Add optional parameters
        if negative_prompt.strip():
            payload["negative_prompt"] = negative_prompt

        if seed != -1:
            payload["seed"] = seed

        if style_preset != "none":
            payload["style_preset"] = style_preset

        # Add reference image if provided
        if reference_image is not None:
            try:
                image_data = self.encode_image(reference_image)
                payload["reference_image"] = image_data
                print(f"[Sora API] Using reference image for image-to-video generation")
            except Exception as e:
                print(f"[Sora API Warning] Failed to encode reference image: {str(e)}")

        # Prepare headers
        headers = {
            "Authorization": f"Bearer {final_api_key}",
            "Content-Type": "application/json"
        }

        print(f"[Sora API] Starting video generation...")
        print(f"[Sora API] Prompt: {prompt[:100]}...")
        print(f"[Sora API] Resolution: {resolution}, Duration: {duration}, FPS: {fps}")

        try:
            # Make API request
            response = requests.post(
                f"{self.base_url}/generations",
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            # Extract task information
            task_id = result.get("id", "")
            status = result.get("status", "pending")
            video_url = result.get("video_url", "")

            print(f"[Sora API] Task created: {task_id}")
            print(f"[Sora API] Status: {status}")

            # If video is not ready, poll for completion
            if status in ["pending", "processing"] and task_id:
                print(f"[Sora API] Video is processing, waiting for completion...")
                video_url, status = self.wait_for_completion(task_id, final_api_key)

            if status == "completed" and video_url:
                print(f"[Sora API] ✓ Video generation completed!")
                print(f"[Sora API] Video URL: {video_url}")
                return (video_url, task_id, status)
            else:
                error_msg = result.get("error", {}).get("message", "Unknown error")
                print(f"[Sora API] ✗ Generation failed: {error_msg}")
                return ("", task_id, f"failed: {error_msg}")

        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            print(f"[Sora API Error] Request failed: {error_msg}")
            return ("", "", f"error: {error_msg}")
        except Exception as e:
            error_msg = str(e)
            print(f"[Sora API Error] Unexpected error: {error_msg}")
            return ("", "", f"error: {error_msg}")

    def wait_for_completion(self, task_id, api_key, max_wait_time=300, poll_interval=5):
        """
        Poll the API to wait for video generation completion
        """
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        start_time = time.time()

        while True:
            elapsed = time.time() - start_time

            if elapsed > max_wait_time:
                print(f"[Sora API] Timeout waiting for video generation (>{max_wait_time}s)")
                return ("", "timeout")

            try:
                response = requests.get(
                    f"{self.base_url}/generations/{task_id}",
                    headers=headers,
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()

                status = result.get("status", "unknown")
                video_url = result.get("video_url", "")

                if status == "completed":
                    return (video_url, status)
                elif status == "failed":
                    error_msg = result.get("error", {}).get("message", "Unknown error")
                    print(f"[Sora API] Generation failed: {error_msg}")
                    return ("", f"failed: {error_msg}")
                else:
                    # Still processing
                    print(f"[Sora API] Still processing... ({int(elapsed)}s elapsed)")
                    time.sleep(poll_interval)

            except Exception as e:
                print(f"[Sora API Warning] Error polling status: {str(e)}")
                time.sleep(poll_interval)


class Sora_Video_Downloader:
    """
    Download Sora-generated videos to local storage
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {
                    "default": "",
                    "placeholder": "Video URL from Sora API node"
                }),
                "output_filename": ("STRING", {
                    "default": "sora_video_%time%",
                    "placeholder": "Output filename (use %time% for timestamp)"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)
    FUNCTION = "download_video"
    CATEGORY = "Sora API"
    OUTPUT_NODE = True

    DESCRIPTION = "Download Sora-generated video from URL to local storage"

    def download_video(self, video_url, output_filename):
        """Download video from URL and save to output folder"""

        if not video_url or not video_url.startswith("http"):
            error_msg = "Invalid or empty video URL"
            print(f"[Sora Downloader] {error_msg}")
            return (f"error: {error_msg}",)

        try:
            # Get output directory
            output_dir = folder_paths.get_output_directory()

            # Replace timestamp placeholder
            if "%time%" in output_filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_filename = output_filename.replace("%time%", timestamp)

            # Ensure .mp4 extension
            if not output_filename.endswith(".mp4"):
                output_filename += ".mp4"

            output_path = os.path.join(output_dir, output_filename)

            print(f"[Sora Downloader] Downloading video from: {video_url}")

            # Download video
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()

            # Save to file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"[Sora Downloader] ✓ Video saved to: {output_path}")
            return (output_path,)

        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            print(f"[Sora Downloader Error] {error_msg}")
            return (f"error: {error_msg}",)


class Sora_Task_Status:
    """
    Check the status of a Sora API task
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1/sora"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "task_id": ("STRING", {
                    "default": "",
                    "placeholder": "Task ID from Sora API node"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "placeholder": "OpenAI API key (optional if env var set)"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("status", "video_url", "error_message")
    FUNCTION = "check_status"
    CATEGORY = "Sora API"
    OUTPUT_NODE = True

    DESCRIPTION = "Check the status of a Sora video generation task"

    def check_status(self, task_id, api_key):
        """Check task status via API"""

        if not task_id:
            return ("error", "", "Task ID is required")

        final_api_key = api_key if api_key.strip() else self.api_key

        if not final_api_key:
            return ("error", "", "API key not provided")

        headers = {
            "Authorization": f"Bearer {final_api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(
                f"{self.base_url}/generations/{task_id}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            status = result.get("status", "unknown")
            video_url = result.get("video_url", "")
            error_msg = result.get("error", {}).get("message", "")

            print(f"[Sora Status] Task {task_id}: {status}")

            return (status, video_url, error_msg)

        except Exception as e:
            error_msg = str(e)
            print(f"[Sora Status Error] {error_msg}")
            return ("error", "", error_msg)


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "OpenAI_Sora_API_Plus": OpenAI_Sora_API_Plus,
    "Sora_Video_Downloader": Sora_Video_Downloader,
    "Sora_Task_Status": Sora_Task_Status,
}

# Human-readable node names for ComfyUI UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAI_Sora_API_Plus": "OpenAI Sora API Plus ⚡",
    "Sora_Video_Downloader": "Sora Video Downloader 📥",
    "Sora_Task_Status": "Sora Task Status 📊",
}
