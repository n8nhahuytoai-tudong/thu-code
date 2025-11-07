"""
PyQt5 GUI for Sora Video Generation Tool
"""
import sys
import os
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QSpinBox, QComboBox,
    QFileDialog, QMessageBox, QProgressBar, QGroupBox, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from .config import config
from .sora_api import sora_api


class VideoGenerationThread(QThread):
    """Thread for video generation to prevent UI freezing"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)

    def __init__(self, prompt, duration, resolution):
        super().__init__()
        self.prompt = prompt
        self.duration = duration
        self.resolution = resolution

    def run(self):
        """Run video generation"""
        result = sora_api.generate_video(
            prompt=self.prompt,
            duration=self.duration,
            resolution=self.resolution,
            callback=self.progress.emit
        )
        self.finished.emit(result)


class VideoDownloadThread(QThread):
    """Thread for video download"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, url, output_path):
        super().__init__()
        self.url = url
        self.output_path = output_path

    def run(self):
        """Run video download"""
        success = sora_api.download_video(
            url=self.url,
            output_path=self.output_path,
            callback=self.progress.emit
        )
        self.finished.emit(success)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_video_url = None
        self.generation_thread = None
        self.download_thread = None

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Sora AI Video Generator - ManixAI Tools v1.2.3")
        self.setMinimumSize(800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # Create tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_generation_tab(), "Generate Video")
        tabs.addTab(self.create_settings_tab(), "Settings")

        layout.addWidget(tabs)

        # Status bar
        self.statusBar().showMessage("Ready")

        # Load saved API key if exists
        if config.validate_api_key():
            sora_api.set_api_key(config.api_key)
            self.statusBar().showMessage("API Key loaded from config")

    def create_generation_tab(self):
        """Create video generation tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Title
        title = QLabel("🎬 Generate AI Video with Sora")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Prompt input group
        prompt_group = QGroupBox("Video Description")
        prompt_layout = QVBoxLayout()

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
            "Enter your video description here...\n\n"
            "Example: A serene sunset over a calm ocean, "
            "with gentle waves and seagulls flying in the distance."
        )
        self.prompt_input.setMinimumHeight(120)
        prompt_layout.addWidget(self.prompt_input)

        prompt_group.setLayout(prompt_layout)
        layout.addWidget(prompt_group)

        # Parameters group
        params_group = QGroupBox("Generation Parameters")
        params_layout = QHBoxLayout()

        # Duration
        duration_layout = QVBoxLayout()
        duration_label = QLabel("Duration (seconds):")
        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(3)
        self.duration_spin.setMaximum(10)
        self.duration_spin.setValue(config.default_duration)
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.duration_spin)
        params_layout.addLayout(duration_layout)

        # Resolution
        resolution_layout = QVBoxLayout()
        resolution_label = QLabel("Resolution:")
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "1920x1080",
            "1280x720",
            "3840x2160",
            "1080x1920"  # Portrait
        ])
        self.resolution_combo.setCurrentText(config.default_resolution)
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_combo)
        params_layout.addLayout(resolution_layout)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Generate button
        self.generate_btn = QPushButton("🎥 Generate Video")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.generate_btn.clicked.connect(self.generate_video)
        layout.addWidget(self.generate_btn)

        # Progress
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_label)

        # Download button (hidden initially)
        self.download_btn = QPushButton("💾 Download Video")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.clicked.connect(self.download_video)
        self.download_btn.setVisible(False)
        layout.addWidget(self.download_btn)

        # Log output
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        layout.addStretch()

        return tab

    def create_settings_tab(self):
        """Create settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Title
        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # API Key group
        api_group = QGroupBox("OpenAI API Configuration")
        api_layout = QVBoxLayout()

        api_label = QLabel("API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your OpenAI API key (sk-...)")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        if config.api_key:
            self.api_key_input.setText(config.api_key)

        save_api_btn = QPushButton("💾 Save API Key")
        save_api_btn.clicked.connect(self.save_api_key)

        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_key_input)
        api_layout.addWidget(save_api_btn)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # Output directory group
        output_group = QGroupBox("Output Settings")
        output_layout = QVBoxLayout()

        output_label = QLabel("Output Directory:")
        output_path_layout = QHBoxLayout()
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setText(config.output_dir)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_output_dir)
        output_path_layout.addWidget(self.output_dir_input)
        output_path_layout.addWidget(browse_btn)

        save_output_btn = QPushButton("💾 Save Output Settings")
        save_output_btn.clicked.connect(self.save_output_settings)

        output_layout.addWidget(output_label)
        output_layout.addLayout(output_path_layout)
        output_layout.addWidget(save_output_btn)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Info
        info_label = QLabel(
            "ℹ️ Get your OpenAI API key from: https://platform.openai.com/api-keys\n"
            "Note: Sora API access may require special approval."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(info_label)

        layout.addStretch()

        return tab

    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {message}")

    def save_api_key(self):
        """Save API key to config"""
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Error", "Please enter an API key")
            return

        config.api_key = api_key
        sora_api.set_api_key(api_key)

        if config.save():
            QMessageBox.information(self, "Success", "API key saved successfully!")
            self.log("API key saved")
        else:
            QMessageBox.warning(self, "Error", "Failed to save API key")

    def browse_output_dir(self):
        """Browse for output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            config.output_dir
        )
        if directory:
            self.output_dir_input.setText(directory)

    def save_output_settings(self):
        """Save output directory settings"""
        output_dir = self.output_dir_input.text().strip()
        if not output_dir:
            QMessageBox.warning(self, "Error", "Please select an output directory")
            return

        config.output_dir = output_dir
        if config.save():
            QMessageBox.information(self, "Success", "Output settings saved!")
            self.log("Output settings saved")
        else:
            QMessageBox.warning(self, "Error", "Failed to save settings")

    def generate_video(self):
        """Start video generation"""
        # Validate inputs
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Error", "Please enter a video description")
            return

        if not config.validate_api_key():
            QMessageBox.warning(
                self,
                "Error",
                "Please configure your API key in Settings tab"
            )
            return

        # Get parameters
        duration = self.duration_spin.value()
        resolution = self.resolution_combo.currentText()

        # Disable button
        self.generate_btn.setEnabled(False)
        self.download_btn.setVisible(False)
        self.progress_label.setText("⏳ Starting generation...")
        self.log(f"Generating video: {prompt[:50]}...")

        # Start generation thread
        self.generation_thread = VideoGenerationThread(prompt, duration, resolution)
        self.generation_thread.progress.connect(self.on_generation_progress)
        self.generation_thread.finished.connect(self.on_generation_finished)
        self.generation_thread.start()

    def on_generation_progress(self, message):
        """Handle generation progress updates"""
        self.progress_label.setText(message)
        self.log(message)

    def on_generation_finished(self, result):
        """Handle generation completion"""
        self.generate_btn.setEnabled(True)

        if result.get("success"):
            self.current_video_url = result.get("video_url")
            video_id = result.get("id", "unknown")

            self.log(f"✅ Video generated successfully! ID: {video_id}")
            self.progress_label.setText("✅ Video ready! Click download to save.")
            self.download_btn.setVisible(True)

            QMessageBox.information(
                self,
                "Success",
                "Video generated successfully!\nClick 'Download Video' to save it."
            )
        else:
            error = result.get("error", "Unknown error")
            self.log(f"❌ Generation failed: {error}")
            self.progress_label.setText(f"❌ Error: {error}")

            QMessageBox.critical(
                self,
                "Generation Failed",
                f"Failed to generate video:\n{error}"
            )

    def download_video(self):
        """Download generated video"""
        if not self.current_video_url:
            QMessageBox.warning(self, "Error", "No video to download")
            return

        # Create output directory if needed
        output_dir = Path(config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"sora_video_{timestamp}.mp4"

        # Disable button
        self.download_btn.setEnabled(False)
        self.progress_label.setText("⏳ Downloading video...")
        self.log(f"Downloading to: {output_path}")

        # Start download thread
        self.download_thread = VideoDownloadThread(
            self.current_video_url,
            str(output_path)
        )
        self.download_thread.progress.connect(self.on_download_progress)
        self.download_thread.finished.connect(
            lambda success: self.on_download_finished(success, str(output_path))
        )
        self.download_thread.start()

    def on_download_progress(self, message):
        """Handle download progress updates"""
        self.progress_label.setText(message)
        self.log(message)

    def on_download_finished(self, success, output_path):
        """Handle download completion"""
        self.download_btn.setEnabled(True)

        if success:
            self.log(f"✅ Video saved to: {output_path}")
            self.progress_label.setText("✅ Download complete!")

            QMessageBox.information(
                self,
                "Success",
                f"Video downloaded successfully!\n\nSaved to:\n{output_path}"
            )

            # Open folder
            if sys.platform == 'win32':
                os.startfile(Path(output_path).parent)
        else:
            self.log("❌ Download failed")
            self.progress_label.setText("❌ Download failed")
            QMessageBox.critical(self, "Error", "Failed to download video")


def create_app():
    """Create and return QApplication instance"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    return app


def create_main_window():
    """Create and return main window"""
    window = MainWindow()
    window.show()
    return window
