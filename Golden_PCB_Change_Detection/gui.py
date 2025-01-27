import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox, QGroupBox,
    QProgressBar, QMessageBox, QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class ImageProcessingThread(QThread):
    processing_finished = pyqtSignal(tuple)
    processing_error = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            subprocess.run(self.command, check=True)
            output_dir = next(arg.split('=')[1] for arg in self.command if arg.startswith('-output_dir='))
            input_path = next(arg.split('=')[1] for arg in self.command if arg.startswith('-input_path='))
            reference_path = next(arg.split('=')[1] for arg in self.command if arg.startswith('-reference_path='))
            diff_path = os.path.join(output_dir, "final_diff.jpg")

            if os.path.exists(diff_path):
                self.processing_finished.emit((input_path, reference_path, diff_path))
            else:
                self.processing_error.emit("Difference image not found")

        except subprocess.CalledProcessError as e:
            self.processing_error.emit(f"Script execution error: {str(e)}")

class ChangeChipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Golden_PCB_Change_Detection")
        self.showMaximized()  # Open in maximized mode with window decorations
        
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Left Panel for Inputs and Settings
        left_panel = QScrollArea()
        left_panel.setWidgetResizable(True)
        left_panel_content = QWidget()
        left_layout = QVBoxLayout(left_panel_content)

        # Image Selection Group
        image_group = QGroupBox("Image Selection")
        image_layout = QGridLayout()

        self.input_image_path = QLineEdit()
        input_browse_btn = QPushButton("Browse")
        input_browse_btn.clicked.connect(lambda: self.browse_image(self.input_image_path))
        image_layout.addWidget(QLabel("Input Image:"), 0, 0)
        image_layout.addWidget(self.input_image_path, 0, 1)
        image_layout.addWidget(input_browse_btn, 0, 2)

        self.ref_image_path = QLineEdit()
        ref_browse_btn = QPushButton("Browse")
        ref_browse_btn.clicked.connect(lambda: self.browse_image(self.ref_image_path))
        image_layout.addWidget(QLabel("Reference Image:"), 1, 0)
        image_layout.addWidget(self.ref_image_path, 1, 1)
        image_layout.addWidget(ref_browse_btn, 1, 2)

        self.output_dir_path = QLineEdit()
        self.output_dir_path.setText("example_output")
        output_browse_btn = QPushButton("Browse")
        output_browse_btn.clicked.connect(self.browse_output_dir)
        image_layout.addWidget(QLabel("Output Directory:"), 2, 0)
        image_layout.addWidget(self.output_dir_path, 2, 1)
        image_layout.addWidget(output_browse_btn, 2, 2)

        image_group.setLayout(image_layout)
        left_layout.addWidget(image_group)

        # Processing Parameters Group
        params_group = QGroupBox("Processing Parameters")
        params_layout = QGridLayout()

        params = [
            ("n", 16),
            ("Window Size", 5),
            ("PCA Dim Gray", 3),
            ("PCA Dim RGB", 9),
            ("Resize Factor", 0.2)
        ]

        self.param_inputs = {}
        for i, (name, default) in enumerate(params):
            label = QLabel(name + ":")
            input_field = QLineEdit(str(default))
            params_layout.addWidget(label, i, 0)
            params_layout.addWidget(input_field, i, 1)
            self.param_inputs[name] = input_field

        params_group.setLayout(params_layout)
        left_layout.addWidget(params_group)

        # Options Checkboxes
        checkbox_group = QGroupBox("Options")
        checkbox_layout = QHBoxLayout()

        self.lighting_fix = QCheckBox("Lighting Fix")
        self.use_homography = QCheckBox("Use Homography")
        self.save_extra = QCheckBox("Save Extra Stuff")

        checkbox_layout.addWidget(self.lighting_fix)
        checkbox_layout.addWidget(self.use_homography)
        checkbox_layout.addWidget(self.save_extra)
        checkbox_group.setLayout(checkbox_layout)
        left_layout.addWidget(checkbox_group)

        # Process Button and Progress Bar
        self.process_btn = QPushButton("Process Images")
        self.process_btn.clicked.connect(self.run_script)
        self.progress_bar = QProgressBar()

        left_layout.addWidget(self.process_btn)
        left_layout.addWidget(self.progress_bar)

        left_panel.setWidget(left_panel_content)
        main_layout.addWidget(left_panel, 2)

        # Right Panel for Image Display
        right_panel = QScrollArea()
        right_panel.setWidgetResizable(True)
        right_panel_content = QWidget()
        self.right_layout = QVBoxLayout(right_panel_content)
        self.right_layout.setAlignment(Qt.AlignTop)

        self.image_label = QLabel("Processed Images Will Appear Here")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.image_label)

        right_panel.setWidget(right_panel_content)
        main_layout.addWidget(right_panel, 3)

        self.setCentralWidget(main_widget)
        self.apply_dark_theme()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2C2C2C;
                color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit, QCheckBox {
                background-color: #3C3F41;
                color: #FFFFFF;
                border: 1px solid #555;
                padding: 5px;
            }
            QPushButton {
                background-color: #4C5052;
                color: #FFFFFF;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5C6062;
            }
            QGroupBox {
                border: 2px solid #555;
                margin-top: 10px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QProgressBar {
                background-color: #3C3F41;
                color: #FFFFFF;
                border: 1px solid #555;
                text-align: center;
            }
        """)

    def browse_image(self, line_edit):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if filename:
            line_edit.setText(filename)

    def browse_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_dir_path.setText(directory)

    def run_script(self):
        if not self.validate_inputs():
            return

        command = [
            "python", "main.py",
            f"-output_dir={self.output_dir_path.text()}",
            f"-input_path={self.input_image_path.text()}",
            f"-reference_path={self.ref_image_path.text()}",
            f"-n={self.param_inputs['n'].text()}",
            f"-window_size={self.param_inputs['Window Size'].text()}",
            f"-pca_dim_gray={self.param_inputs['PCA Dim Gray'].text()}",
            f"-pca_dim_rgb={self.param_inputs['PCA Dim RGB'].text()}",
            f"-resize_factor={self.param_inputs['Resize Factor'].text()}"
        ]

        if self.lighting_fix.isChecked():
            command.append("-lighting_fix")
        if self.use_homography.isChecked():
            command.append("-use_homography")
        if self.save_extra.isChecked():
            command.append("-save_extra_stuff")

        self.processing_thread = ImageProcessingThread(command)
        self.processing_thread.processing_finished.connect(self.display_result_images)
        self.processing_thread.processing_error.connect(self.show_error)

        self.process_btn.setEnabled(False)
        self.progress_bar.setRange(0, 0)

        self.processing_thread.start()

    def validate_inputs(self):
        if not self.input_image_path.text():
            QMessageBox.critical(self, "Error", "Please select an input image")
            return False
        if not self.ref_image_path.text():
            QMessageBox.critical(self, "Error", "Please select a reference image")
            return False
        if not self.output_dir_path.text():
            QMessageBox.critical(self, "Error", "Please select an output directory")
            return False
        return True

    def display_result_images(self, image_paths):
        input_path, reference_path, diff_path = image_paths

        # Clear the right layout before displaying new images
        while self.right_layout.count():
            child = self.right_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for path, label_text in zip(
            [input_path, reference_path, diff_path],
            ["Input Image", "Reference Image", "Difference Image"]
        ):
            # Add label for the image
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px 0;")
            self.right_layout.addWidget(label)

            # Add the image below the label
            pixmap = QPixmap(path).scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            self.right_layout.addWidget(image_label)

        self.process_btn.setEnabled(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)


    def show_error(self, error_message):
        QMessageBox.critical(self, "Processing Error", error_message)
        self.process_btn.setEnabled(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)


def main():
    app = QApplication(sys.argv)
    ex = ChangeChipApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()