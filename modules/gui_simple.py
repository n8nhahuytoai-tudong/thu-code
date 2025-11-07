"""
Simple PyQt5 GUI without async complications
Uses QThread for browser automation
"""
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox,
    QMessageBox, QGroupBox, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .config import config


class BrowserWorker(QThread):
    """Worker thread for browser operations"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, operation, *args, **kwargs):
        super().__init__()
        self.operation = operation
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Run operation in separate event loop"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Run the async operation
            if self.operation == 'login':
                result = loop.run_until_complete(self.do_login())
            elif self.operation == 'generate':
                result = loop.run_until_complete(self.do_generate())
            elif self.operation == 'download':
                result = loop.run_until_complete(self.do_download())
            else:
                result = False

            loop.close()

            self.finished.emit(result, "")

        except Exception as e:
            self.finished.emit(False, str(e))

    async def do_login(self):
        """Async login operation"""
        from .browser_automation import sora_browser

        email = self.kwargs.get('email')
        password = self.kwargs.get('password')
        headless = self.kwargs.get('headless', False)

        self.progress.emit("Initializing browser...")

        # Initialize
        success = await sora_browser.init_browser(headless=headless)
        if not success:
            self.progress.emit("Failed to initialize browser")
            return False

        # Login
        success = await sora_browser.login_with_gmail(
            email=email,
            password=password,
            callback=self.progress.emit
        )

        return success

    async def do_generate(self):
        """Async video generation"""
        from .browser_automation import sora_browser

        prompt = self.kwargs.get('prompt')

        video_url = await sora_browser.generate_video(
            prompt=prompt,
            callback=self.progress.emit
        )

        # Store video URL globally for download
        if video_url:
            self.kwargs['result_video_url'] = video_url

        return video_url is not None

    async def do_download(self):
        """Async download"""
        from .browser_automation import sora_browser

        output_path = self.kwargs.get('output_path')

        success = await sora_browser.download_video(
            output_path=output_path,
            callback=self.progress.emit
        )

        return success


class BrowserLoginWidget(QWidget):
    """Widget for browser login"""
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("🔐 Login to Sora with Gmail")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Info
        info = QLabel(
            "Enter your Gmail credentials to login to sora.chatgpt.com\n"
            "The browser will open automatically and login for you."
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(info)

        # Login form
        form_group = QGroupBox("Gmail Credentials")
        form_layout = QVBoxLayout()

        # Email
        email_label = QLabel("Gmail Address:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your.email@gmail.com")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)

        # Password
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Your Gmail password")
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        # Show password checkbox
        self.show_password_cb = QCheckBox("Show password")
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)
        form_layout.addWidget(self.show_password_cb)

        # Headless mode
        self.headless_cb = QCheckBox("Headless mode (hide browser window)")
        self.headless_cb.setChecked(False)
        form_layout.addWidget(self.headless_cb)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Login button
        self.login_btn = QPushButton("🚀 Login to Sora")
        self.login_btn.setMinimumHeight(50)
        self.login_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.login_btn.clicked.connect(self.start_login)
        layout.addWidget(self.login_btn)

        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Log
        log_group = QGroupBox("Login Log")
        log_layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        layout.addStretch()

    def toggle_password_visibility(self, state):
        """Toggle password visibility"""
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def log(self, message):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {message}")

    def start_login(self):
        """Start login process"""
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter both email and password")
            return

        if "@gmail.com" not in email:
            QMessageBox.warning(self, "Error", "Please enter a valid Gmail address")
            return

        self.login_btn.setEnabled(False)
        self.status_label.setText("⏳ Starting browser...")
        self.log("Starting login process...")

        # Start worker thread
        headless = self.headless_cb.isChecked()
        self.worker = BrowserWorker('login', email=email, password=password, headless=headless)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_progress(self, message):
        """Handle progress updates"""
        self.status_label.setText(message)
        self.log(message)

    def on_finished(self, success, error):
        """Handle completion"""
        self.login_btn.setEnabled(True)

        if success:
            self.status_label.setText("✅ Login successful!")
            self.log("✅ Login completed successfully")
            self.login_success.emit()
            QMessageBox.information(
                self,
                "Success",
                "Successfully logged in to Sora!\n\n"
                "You can now generate videos in the Generate tab."
            )
        else:
            self.status_label.setText(f"❌ Login failed: {error}")
            self.log(f"❌ Login failed: {error}")
            QMessageBox.critical(
                self,
                "Login Failed",
                f"Failed to login to Sora.\n\n{error}\n\n"
                "Please check your credentials and try again."
            )


class VideoGenerationWidget(QWidget):
    """Widget for video generation"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.current_video_url = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("🎬 Generate AI Video")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Prompt group
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

        # Generate button
        self.generate_btn = QPushButton("🎥 Generate Video")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.generate_btn.clicked.connect(self.generate_video)
        layout.addWidget(self.generate_btn)

        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Download button
        self.download_btn = QPushButton("💾 Download Video")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.clicked.connect(self.download_video)
        self.download_btn.setVisible(False)
        layout.addWidget(self.download_btn)

        # Log
        log_group = QGroupBox("Generation Log")
        log_layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        layout.addStretch()

    def log(self, message):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {message}")

    def generate_video(self):
        """Start video generation"""
        from .browser_automation import sora_browser

        prompt = self.prompt_input.toPlainText().strip()

        if not prompt:
            QMessageBox.warning(self, "Error", "Please enter a video description")
            return

        if not sora_browser.is_logged_in:
            QMessageBox.warning(
                self,
                "Error",
                "Please login first in the Login tab"
            )
            return

        self.generate_btn.setEnabled(False)
        self.download_btn.setVisible(False)
        self.status_label.setText("⏳ Starting generation...")
        self.log(f"Generating: {prompt[:50]}...")

        # Start worker
        self.worker = BrowserWorker('generate', prompt=prompt)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_generate_finished)
        self.worker.start()

    def on_progress(self, message):
        """Handle progress"""
        self.status_label.setText(message)
        self.log(message)

    def on_generate_finished(self, success, error):
        """Handle generation completion"""
        self.generate_btn.setEnabled(True)

        if success:
            # Get video URL from worker
            self.current_video_url = getattr(self.worker.kwargs, 'result_video_url', None)

            self.log("✅ Video generated!")
            self.status_label.setText("✅ Video ready!")
            self.download_btn.setVisible(True)

            QMessageBox.information(
                self,
                "Success",
                "Video generated successfully!\n\nClick Download to save it."
            )
        else:
            self.log(f"❌ Generation failed: {error}")
            self.status_label.setText(f"❌ Failed: {error}")
            QMessageBox.critical(
                self,
                "Failed",
                f"Video generation failed:\n{error}"
            )

    def download_video(self):
        """Download video"""
        # Create output directory
        output_dir = Path(config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"sora_video_{timestamp}.mp4"

        self.download_btn.setEnabled(False)
        self.log(f"Downloading to: {output_path}")

        # Start download worker
        self.worker = BrowserWorker('download', output_path=str(output_path))
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(lambda s, e: self.on_download_finished(s, e, str(output_path)))
        self.worker.start()

    def on_download_finished(self, success, error, output_path):
        """Handle download completion"""
        self.download_btn.setEnabled(True)

        if success:
            self.log(f"✅ Saved to: {output_path}")
            QMessageBox.information(
                self,
                "Success",
                f"Video downloaded!\n\n{output_path}"
            )

            # Open folder
            if sys.platform == 'win32':
                os.startfile(Path(output_path).parent)
        else:
            self.log(f"❌ Download failed: {error}")
            QMessageBox.critical(self, "Failed", f"Download failed:\n{error}")


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Sora AI Video Generator v1.2.3")
        self.setMinimumSize(800, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # Tabs
        tabs = QTabWidget()

        # Login tab
        self.login_widget = BrowserLoginWidget()
        self.login_widget.login_success.connect(self.on_login_success)
        tabs.addTab(self.login_widget, "1. Login")

        # Generate tab
        self.generate_widget = VideoGenerationWidget()
        tabs.addTab(self.generate_widget, "2. Generate Video")

        layout.addWidget(tabs)

        # Status bar
        self.statusBar().showMessage("Ready - Please login first")

    def on_login_success(self):
        """Handle successful login"""
        self.statusBar().showMessage("✅ Logged in - Ready to generate videos")

    def closeEvent(self, event):
        """Handle window close"""
        # Close browser in separate thread
        from .browser_automation import sora_browser
        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(sora_browser.close())
            loop.close()
        except:
            pass
        event.accept()


def create_app():
    """Create QApplication"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    return app


def create_main_window():
    """Create and show main window"""
    window = MainWindow()
    window.show()
    return window
