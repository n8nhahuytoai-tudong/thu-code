"""
OpenAI Sora API Integration
"""
import requests
import json
from pathlib import Path
from typing import Optional, Dict, Any
from .config import config


class SoraAPI:
    """Handle Sora API requests"""

    def __init__(self):
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Content-Type": "application/json"
        }

    def set_api_key(self, api_key: str):
        """Set API key for authentication"""
        self.headers["Authorization"] = f"Bearer {api_key}"
        config.api_key = api_key

    def generate_video(
        self,
        prompt: str,
        duration: int = 5,
        resolution: str = "1920x1080",
        callback=None
    ) -> Dict[str, Any]:
        """
        Generate video using Sora API

        Args:
            prompt: Text description for video generation
            duration: Video duration in seconds (3-10)
            resolution: Video resolution (e.g., "1920x1080")
            callback: Optional callback function for progress updates

        Returns:
            Dict containing status and video URL or error message
        """
        if not config.validate_api_key():
            return {
                "success": False,
                "error": "API key not configured"
            }

        try:
            # Update callback
            if callback:
                callback("Sending request to Sora API...")

            # Prepare request payload
            payload = {
                "model": "sora-1.0-turbo",
                "prompt": prompt,
                "duration": duration,
                "resolution": resolution,
                "format": "mp4"
            }

            # Make API request
            response = requests.post(
                f"{self.base_url}/videos/generations",
                headers=self.headers,
                json=payload,
                timeout=300
            )

            if callback:
                callback("Processing response...")

            # Handle response
            if response.status_code == 200:
                result = response.json()

                if callback:
                    callback("Video generation started successfully!")

                return {
                    "success": True,
                    "data": result,
                    "video_url": result.get("url", ""),
                    "id": result.get("id", "")
                }
            else:
                error_msg = f"API Error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", error_msg)
                except:
                    pass

                return {
                    "success": False,
                    "error": error_msg
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout - Sora API is taking too long to respond"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Connection error - Please check your internet connection"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def download_video(self, url: str, output_path: str, callback=None) -> bool:
        """
        Download generated video

        Args:
            url: Video URL from API response
            output_path: Local path to save video
            callback: Optional callback for progress updates

        Returns:
            bool: True if download successful
        """
        try:
            if callback:
                callback("Downloading video...")

            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if callback and total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            callback(f"Downloading... {progress}%")

            if callback:
                callback("Download complete!")

            return True

        except Exception as e:
            if callback:
                callback(f"Download failed: {str(e)}")
            return False

    def check_status(self, video_id: str) -> Dict[str, Any]:
        """
        Check video generation status

        Args:
            video_id: ID from generation request

        Returns:
            Dict containing status information
        """
        try:
            response = requests.get(
                f"{self.base_url}/videos/{video_id}",
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"Status check failed: {response.status_code}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global API instance
sora_api = SoraAPI()
