import os
import sys
import cv2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QRadioButton, QGridLayout, QFrame,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QIcon


class RobotCarControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.capture = cv2.VideoCapture(0)  # OpenCV Video Feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_ui(self):
        # Main layout
        main_layout = QHBoxLayout()

        # Left panel (Controls)
        controls_frame = QFrame()
        controls_frame.setFixedWidth(200)  # Fix the width of the left-hand side
        controls_layout = QVBoxLayout()
        controls_frame.setLayout(controls_layout)
        dpad_layout = QGridLayout()

        # D-pad buttons with arrows
        self.up_button = QPushButton("↑")
        self.down_button = QPushButton("↓")
        self.left_button = QPushButton("←")
        self.right_button = QPushButton("→")

        # setings for the buttons
        self.up_button.setFixedSize(60, 60)
        self.down_button.setFixedSize(60, 60)
        self.left_button.setFixedSize(60, 60)
        self.right_button.setFixedSize(60, 60)

        # set icons for the buttons up.png
        self.up_button.setIconSize(self.up_button.size())
        self.up_button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "up.png")))
        self.down_button.setIconSize(self.down_button.size())
        self.down_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"down.png"))))
        self.left_button.setIconSize(self.left_button.size())
        self.left_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"left.png"))))
        self.right_button.setIconSize(self.right_button.size())
        self.right_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"right.png"))))

        dpad_layout.addWidget(self.up_button, 0, 1)
        dpad_layout.addWidget(self.down_button, 2, 1)
        dpad_layout.addWidget(self.left_button, 1, 0)
        dpad_layout.addWidget(self.right_button, 1, 2)

        # Action buttons
        action_buttons_layout = QVBoxLayout()
        self.circle_button = QPushButton("Circle")
        self.square_button = QPushButton("Square")
        action_buttons_layout.addWidget(self.circle_button)
        action_buttons_layout.addWidget(self.square_button)

        # Velocity slider and mode
        self.velocity_slider = QSlider(Qt.Orientation.Horizontal)
        self.velocity_slider.setRange(0, 100)
        self.velocity_slider.setValue(50)
        self.mode_radio = QRadioButton("Auto Mode")

        # Connect signals
        self.up_button.clicked.connect(lambda: self.send_command("UP"))
        self.down_button.clicked.connect(lambda: self.send_command("DOWN"))
        self.left_button.clicked.connect(lambda: self.send_command("LEFT"))
        self.right_button.clicked.connect(lambda: self.send_command("RIGHT"))
        self.circle_button.clicked.connect(lambda: self.send_command("CIRCLE"))
        self.square_button.clicked.connect(lambda: self.send_command("SQUARE"))
        self.velocity_slider.valueChanged.connect(self.adjust_velocity)

        # Add widgets to controls layout
        controls_layout.addLayout(dpad_layout)
        controls_layout.addLayout(action_buttons_layout)
        controls_layout.addWidget(self.velocity_slider)
        controls_layout.addWidget(self.mode_radio)

        # Right panel (Video Feed)
        self.video_label = QLabel()
        self.video_label.setText("Video Feed")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("border: 1px solid black;")  # Optional border for clarity

        # Add layouts to main layout
        main_layout.addWidget(controls_frame)
        main_layout.addWidget(self.video_label, stretch=1)  # Allow video feed to expand

        self.setLayout(main_layout)
        self.setWindowTitle("Robot Car Control")

        # Load QSS Stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "style.qss"), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("QSS file not found. Using default styles.")

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            q_img = QImage(frame.data, width, height, step, QImage.Format.Format_RGB888)
            window_width, window_height = self.size().width(), self.size().height()

            scaled_frame = cv2.resize(frame, (window_width, window_height))

            self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def send_command(self, direction):
        print(f"Command Sent: {direction}")

    def adjust_velocity(self):
        velocity = self.velocity_slider.value()
        print(f"Velocity Adjusted: {velocity}")

    def closeEvent(self, event):
        self.capture.release()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotCarControlApp()
    window.show()
    sys.exit(app.exec())
