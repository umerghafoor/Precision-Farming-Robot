import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QSlider, QLabel, QPushButton, QFileDialog, QInputDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap

def save_profile(lower_hsv, upper_hsv):
    profile_name, ok = QInputDialog.getText(None, "Save Profile", "Enter profile name:")
    if ok and profile_name:
        filepath = f"{profile_name}.npz"
        np.savez(filepath, lower_hsv=lower_hsv, upper_hsv=upper_hsv)
        print(f"Profile '{profile_name}' saved successfully!")

def load_profile():
    options = QFileDialog().options()
    file_path, _ = QFileDialog.getOpenFileName(None, "Open Profile", "", "NPZ files (*.npz);;All Files (*)", options=options)
    if file_path:
        data = np.load(file_path)
        lower_hsv = data['lower_hsv']
        upper_hsv = data['upper_hsv']
        print(f"Loaded profile: {file_path}")
        return lower_hsv, upper_hsv
    return None, None

class HSVControlWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.lower_hsv = np.array([0, 120, 70])
        self.upper_hsv = np.array([180, 255, 255])

        self.initUI()

    def initUI(self):
        self.setWindowTitle('HSV Control Panel')

        layout = QVBoxLayout()

        # HSV sliders and labels
        self.lower_h_slider = self.create_slider('Lower H', 0, 180, self.lower_hsv[0])
        self.lower_s_slider = self.create_slider('Lower S', 0, 255, self.lower_hsv[1])
        self.lower_v_slider = self.create_slider('Lower V', 0, 255, self.lower_hsv[2])

        self.upper_h_slider = self.create_slider('Upper H', 0, 180, self.upper_hsv[0])
        self.upper_s_slider = self.create_slider('Upper S', 0, 255, self.upper_hsv[1])
        self.upper_v_slider = self.create_slider('Upper V', 0, 255, self.upper_hsv[2])

        self.strip_width_slider = self.create_slider('Strip Width', 1, 100, 10)

        layout.addWidget(QLabel('Lower HSV'))
        layout.addWidget(self.lower_h_slider)
        layout.addWidget(self.lower_s_slider)
        layout.addWidget(self.lower_v_slider)

        layout.addWidget(QLabel('Upper HSV'))
        layout.addWidget(self.upper_h_slider)
        layout.addWidget(self.upper_s_slider)
        layout.addWidget(self.upper_v_slider)

        layout.addWidget(QLabel('Strip Width'))
        layout.addWidget(self.strip_width_slider)

        # Save button
        save_button = QPushButton('Save Profile', self)
        save_button.clicked.connect(self.save_profile)
        layout.addWidget(save_button)

        hbox = QHBoxLayout()
        # Label to display frame
        self.frame_label = QLabel(self)
        hbox.addWidget(self.frame_label)

        # Label to display mask
        self.mask_label = QLabel(self)
        hbox.addWidget(self.mask_label)

        layout.addLayout(hbox)

        self.setLayout(layout)

    def create_slider(self, label, min_val, max_val, initial_val):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(initial_val)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(10)
        return slider

    def save_profile(self):
        lower_hsv = np.array([self.lower_h_slider.value(), self.lower_s_slider.value(), self.lower_v_slider.value()])
        upper_hsv = np.array([self.upper_h_slider.value(), self.upper_s_slider.value(), self.upper_v_slider.value()])
        save_profile(lower_hsv, upper_hsv)

    def get_hsv_values(self):
        lower_hsv = np.array([self.lower_h_slider.value(), self.lower_s_slider.value(), self.lower_v_slider.value()])
        upper_hsv = np.array([self.upper_h_slider.value(), self.upper_s_slider.value(), self.upper_v_slider.value()])
        return lower_hsv, upper_hsv

    def get_strip_width(self):
        return self.strip_width_slider.value()

    def update_image(self, frame, mask = None):
        # Convert OpenCV frame to QImage
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(qt_image)
        self.frame_label.setPixmap(pixmap)

        if mask is None:
            return
        # Convert OpenCV mask to QImage
        height, width = mask.shape
        qt_mask = QImage(mask.data, width, height, width, QImage.Format.Format_Grayscale8)
        mask_pixmap = QPixmap.fromImage(qt_mask)
        self.mask_label.setPixmap(mask_pixmap)
