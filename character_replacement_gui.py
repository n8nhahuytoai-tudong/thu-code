"""
GUI Interface cho Character Replacement
Giao diện đồ họa để thay thế nhân vật trong video
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QFileDialog, QProgressBar,
    QCheckBox, QSpinBox, QGroupBox, QTextEdit, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from character_replacement import CharacterReplacer
import json


class VideoProcessThread(QThread):
    """Thread để xử lý video không block UI"""

    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, replacer, params):
        super().__init__()
        self.replacer = replacer
        self.params = params

    def run(self):
        try:
            self.status.emit("Đang xử lý video...")

            stats = self.replacer.process_video(
                output_path=self.params['output_path'],
                replacement_method=self.params['method'],
                replacement_image=self.params.get('replacement_image'),
                character_filter=self.params.get('character_filter'),
                show_bboxes=self.params['show_bboxes'],
                frame_skip=self.params['frame_skip']
            )

            self.finished.emit(stats)

        except Exception as e:
            self.error.emit(str(e))


class CharacterReplacementGUI(QMainWindow):
    """Main GUI Window"""

    def __init__(self):
        super().__init__()
        self.replacer = None
        self.process_thread = None
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle("Character Replacement Tool - Thay thế nhân vật trong video")
        self.setGeometry(100, 100, 900, 700)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main layout
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Title
        title = QLabel("🎬 THAY THẾ NHÂN VẬT TRONG VIDEO")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Input section
        input_group = QGroupBox("📁 File đầu vào")
        input_layout = QVBoxLayout()

        input_row = QHBoxLayout()
        self.input_path_label = QLabel("Chưa chọn file")
        self.input_path_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
        input_row.addWidget(self.input_path_label, 1)

        self.btn_select_input = QPushButton("Chọn video")
        self.btn_select_input.clicked.connect(self.select_input_video)
        input_row.addWidget(self.btn_select_input)

        input_layout.addLayout(input_row)

        # Video info
        self.video_info_label = QLabel("Thông tin video sẽ hiển thị ở đây sau khi chọn file")
        self.video_info_label.setStyleSheet("padding: 5px; color: #666;")
        input_layout.addWidget(self.video_info_label)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Settings section
        settings_group = QGroupBox("⚙️ Cài đặt xử lý")
        settings_layout = QVBoxLayout()

        # Method selection
        method_row = QHBoxLayout()
        method_row.addWidget(QLabel("Phương pháp thay thế:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "blur - Làm mờ",
            "pixelate - Khảm/Mosaic",
            "color - Tô màu đen",
            "image - Thay bằng ảnh khác"
        ])
        self.method_combo.currentIndexChanged.connect(self.on_method_changed)
        method_row.addWidget(self.method_combo, 1)
        settings_layout.addLayout(method_row)

        # Replacement image (for image method)
        self.image_row = QHBoxLayout()
        self.image_row.addWidget(QLabel("Ảnh thay thế:"))
        self.replacement_image_label = QLabel("Chưa chọn")
        self.replacement_image_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
        self.image_row.addWidget(self.replacement_image_label, 1)
        self.btn_select_image = QPushButton("Chọn ảnh")
        self.btn_select_image.clicked.connect(self.select_replacement_image)
        self.image_row.addWidget(self.btn_select_image)
        self.image_row_widget = QWidget()
        self.image_row_widget.setLayout(self.image_row)
        self.image_row_widget.setVisible(False)
        settings_layout.addWidget(self.image_row_widget)

        # Character filter
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Lọc loại nhân vật:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "all - Tất cả",
            "face - Chỉ khuôn mặt",
            "body - Chỉ toàn thân"
        ])
        filter_row.addWidget(self.filter_combo, 1)
        settings_layout.addLayout(filter_row)

        # Frame skip
        skip_row = QHBoxLayout()
        skip_row.addWidget(QLabel("Bỏ qua frames (tăng tốc):"))
        self.skip_spin = QSpinBox()
        self.skip_spin.setRange(0, 10)
        self.skip_spin.setValue(0)
        self.skip_spin.setSuffix(" frames")
        skip_row.addWidget(self.skip_spin, 1)
        settings_layout.addLayout(skip_row)

        # Show bboxes
        self.bbox_checkbox = QCheckBox("Hiển thị bounding boxes (khung nhận diện)")
        settings_layout.addWidget(self.bbox_checkbox)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Output section
        output_group = QGroupBox("💾 File đầu ra")
        output_layout = QVBoxLayout()

        output_row = QHBoxLayout()
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("Nhập đường dẫn file output hoặc để trống (tự động)")
        output_row.addWidget(self.output_path_edit, 1)

        self.btn_select_output = QPushButton("Chọn vị trí lưu")
        self.btn_select_output.clicked.connect(self.select_output_path)
        output_row.addWidget(self.btn_select_output)

        output_layout.addLayout(output_row)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Progress section
        progress_group = QGroupBox("📊 Tiến trình")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setStyleSheet("color: #0066cc; font-weight: bold;")
        progress_layout.addWidget(self.status_label)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Log section
        log_group = QGroupBox("📝 Log")
        log_layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # Action buttons
        button_layout = QHBoxLayout()

        self.btn_extract_info = QPushButton("📋 Trích xuất thông tin nhân vật")
        self.btn_extract_info.clicked.connect(self.extract_character_info)
        self.btn_extract_info.setEnabled(False)
        button_layout.addWidget(self.btn_extract_info)

        self.btn_process = QPushButton("▶️ Bắt đầu xử lý")
        self.btn_process.clicked.connect(self.start_processing)
        self.btn_process.setEnabled(False)
        self.btn_process.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        button_layout.addWidget(self.btn_process)

        layout.addLayout(button_layout)

        # Initial log
        self.log("Ứng dụng đã sẵn sàng. Vui lòng chọn video đầu vào.")

    def log(self, message):
        """Thêm message vào log"""
        self.log_text.append(f"• {message}")
        # Auto scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_method_changed(self):
        """Xử lý khi thay đổi phương pháp"""
        method = self.method_combo.currentText().split(" - ")[0]
        self.image_row_widget.setVisible(method == "image")

    def select_input_video(self):
        """Chọn video đầu vào"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn video đầu vào",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)"
        )

        if file_path:
            try:
                self.replacer = CharacterReplacer(file_path)
                self.input_path_label.setText(file_path)

                # Hiển thị thông tin video
                info = self.replacer.get_video_info()
                info_text = f"""
                📹 {info['filename']}
                📐 Resolution: {info['resolution']}
                ⏱ FPS: {info['fps']:.1f}
                🎞 Total frames: {info['total_frames']}
                ⏳ Duration: {info['duration_seconds']:.1f}s
                """
                self.video_info_label.setText(info_text)

                # Tự động đặt output path
                if not self.output_path_edit.text():
                    input_path = Path(file_path)
                    output_path = input_path.parent / f"{input_path.stem}_replaced.mp4"
                    self.output_path_edit.setText(str(output_path))

                self.btn_process.setEnabled(True)
                self.btn_extract_info.setEnabled(True)

                self.log(f"✓ Đã tải video: {info['filename']}")
                self.log(f"  Resolution: {info['resolution']}, Duration: {info['duration_seconds']:.1f}s")

            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể tải video:\n{str(e)}")
                self.log(f"✗ Lỗi: {str(e)}")

    def select_replacement_image(self):
        """Chọn ảnh thay thế"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn ảnh thay thế",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )

        if file_path:
            self.replacement_image_label.setText(file_path)
            self.log(f"✓ Đã chọn ảnh thay thế: {Path(file_path).name}")

    def select_output_path(self):
        """Chọn đường dẫn output"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Chọn vị trí lưu video",
            "",
            "MP4 Video (*.mp4);;All Files (*)"
        )

        if file_path:
            self.output_path_edit.setText(file_path)
            self.log(f"✓ Đường dẫn output: {file_path}")

    def extract_character_info(self):
        """Trích xuất thông tin nhân vật"""
        if not self.replacer:
            return

        try:
            output_path = self.output_path_edit.text()
            if not output_path:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn đường dẫn output")
                return

            json_path = output_path.replace('.mp4', '_character_info.json')

            self.status_label.setText("Đang trích xuất thông tin...")
            self.btn_extract_info.setEnabled(False)
            self.btn_process.setEnabled(False)

            QApplication.processEvents()

            info = self.replacer.extract_characters_info(json_path, frame_step=30)

            self.status_label.setText("Hoàn thành!")
            self.log(f"✓ Đã lưu thông tin nhân vật vào: {json_path}")
            self.log(f"  Phát hiện {len(info['characters_timeline'])} điểm thời gian")

            QMessageBox.information(
                self,
                "Thành công",
                f"Đã trích xuất thông tin nhân vật!\nFile: {json_path}"
            )

            self.btn_extract_info.setEnabled(True)
            self.btn_process.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi trích xuất:\n{str(e)}")
            self.log(f"✗ Lỗi: {str(e)}")
            self.btn_extract_info.setEnabled(True)
            self.btn_process.setEnabled(True)

    def start_processing(self):
        """Bắt đầu xử lý video"""
        if not self.replacer:
            return

        output_path = self.output_path_edit.text()
        if not output_path:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn đường dẫn output")
            return

        method = self.method_combo.currentText().split(" - ")[0]

        # Kiểm tra nếu method là image nhưng chưa chọn ảnh
        replacement_image = None
        if method == "image":
            replacement_image = self.replacement_image_label.text()
            if replacement_image == "Chưa chọn":
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn ảnh thay thế")
                return

        # Lấy character filter
        character_filter = None
        filter_text = self.filter_combo.currentText().split(" - ")[0]
        if filter_text != "all":
            character_filter = filter_text

        # Prepare parameters
        params = {
            'output_path': output_path,
            'method': method,
            'replacement_image': replacement_image,
            'character_filter': character_filter,
            'show_bboxes': self.bbox_checkbox.isChecked(),
            'frame_skip': self.skip_spin.value()
        }

        # Disable buttons
        self.btn_process.setEnabled(False)
        self.btn_extract_info.setEnabled(False)
        self.btn_select_input.setEnabled(False)

        self.log("▶️ Bắt đầu xử lý video...")
        self.log(f"  Phương pháp: {method}")
        self.log(f"  Output: {output_path}")

        # Start processing thread
        self.process_thread = VideoProcessThread(self.replacer, params)
        self.process_thread.status.connect(self.on_process_status)
        self.process_thread.finished.connect(self.on_process_finished)
        self.process_thread.error.connect(self.on_process_error)
        self.process_thread.start()

        self.status_label.setText("Đang xử lý... Vui lòng chờ")
        self.progress_bar.setMaximum(0)  # Indeterminate progress

    def on_process_status(self, message):
        """Update status"""
        self.status_label.setText(message)

    def on_process_finished(self, stats):
        """Xử lý khi hoàn thành"""
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)
        self.status_label.setText("✓ Hoàn thành!")

        self.log("✓ Xử lý video hoàn thành!")
        self.log(f"  Frames processed: {stats['frames_processed']}")
        self.log(f"  Characters replaced: {stats['characters_replaced']}")
        if stats['processing_errors'] > 0:
            self.log(f"  ⚠ Errors: {stats['processing_errors']}")

        # Save stats
        stats_file = stats['output_video'].replace('.mp4', '_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        self.log(f"  Stats saved: {stats_file}")

        QMessageBox.information(
            self,
            "Thành công",
            f"Đã xử lý video thành công!\n\nOutput: {stats['output_video']}\nFrames: {stats['frames_processed']}\nCharacters replaced: {stats['characters_replaced']}"
        )

        # Re-enable buttons
        self.btn_process.setEnabled(True)
        self.btn_extract_info.setEnabled(True)
        self.btn_select_input.setEnabled(True)
        self.progress_bar.setValue(0)

    def on_process_error(self, error_msg):
        """Xử lý khi có lỗi"""
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.status_label.setText("✗ Lỗi xử lý")

        self.log(f"✗ Lỗi: {error_msg}")

        QMessageBox.critical(self, "Lỗi", f"Lỗi khi xử lý video:\n{error_msg}")

        # Re-enable buttons
        self.btn_process.setEnabled(True)
        self.btn_extract_info.setEnabled(True)
        self.btn_select_input.setEnabled(True)


def main():
    """Main function"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    window = CharacterReplacementGUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
