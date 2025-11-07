"""
Configuration management for Sora Tool
"""
import os
import json
from pathlib import Path

class Config:
    """Application configuration"""

    def __init__(self):
        self.config_file = Path.home() / ".sora_config.json"
        self.load()

    def load(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.api_key = data.get('api_key', '')
                    self.output_dir = data.get('output_dir', str(Path.home() / 'SoraVideos'))
                    self.default_resolution = data.get('default_resolution', '1920x1080')
                    self.default_duration = data.get('default_duration', 5)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.set_defaults()
        else:
            self.set_defaults()

    def set_defaults(self):
        """Set default configuration values"""
        self.api_key = ''
        self.output_dir = str(Path.home() / 'SoraVideos')
        self.default_resolution = '1920x1080'
        self.default_duration = 5

    def save(self):
        """Save configuration to file"""
        try:
            data = {
                'api_key': self.api_key,
                'output_dir': self.output_dir,
                'default_resolution': self.default_resolution,
                'default_duration': self.default_duration
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def validate_api_key(self):
        """Check if API key is configured"""
        return bool(self.api_key and len(self.api_key) > 10)

# Global config instance
config = Config()
