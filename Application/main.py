import base64
import os
import sys
import cv2
import json
import numpy as np
import paho.mqtt.client as mqtt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QGridLayout, QFrame,
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QImage, QPixmap, QIcon

# MQTT Configuration Constants
MQTT_BROKER_IP = "192.168.18.29"  # Replace with your MQTT broker IP
MQTT_PORT = 1883                  # Default MQTT port
MQTT_TOPIC = "robot/control"      # Topic to publish commands
MQTT_TOPIC_SUB = "video/stream"      # Topic to publish commands
MQTT_USERNAME = None              # Optional: replace with username if authentication is required
MQTT_PASSWORD = None              # Optional: replace with password if authentication is required


icon_size = 50  # Change this size as needed

class RobotCarControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # MQTT Client setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message
        if MQTT_USERNAME and MQTT_PASSWORD:
            self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.mqtt_client.connect(MQTT_BROKER_IP, MQTT_PORT)
        
        self.mqtt_client.subscribe(MQTT_TOPIC_SUB)
        
        # Start the MQTT loop in a separate thread
        self.mqtt_client.loop_start()
        
        self.last_message = ""
        self.is_auto_mode = False
        
        
        # Callback function for receiving messages
    def on_message(self, mqtt_client, userdata, msg):
        jpeg_data = base64.b64decode(msg.payload)
        np_array = np.frombuffer(jpeg_data, dtype=np.uint8)
        self.frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    def update_frame(self):
        # If the frame is received from MQTT
        if hasattr(self, 'frame') and self.frame is not None:
            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            step = channel * width
            q_img = QImage(frame_rgb.data, width, height, step, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))


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
        self.up_button = QPushButton("\u2191")
        self.down_button = QPushButton("\u2193")
        self.left_button = QPushButton("\u2190")
        self.right_button = QPushButton("\u2192")

        # Settings for the buttons
        self.up_button.setFixedSize(60, 60)
        self.down_button.setFixedSize(60, 60)
        self.left_button.setFixedSize(60, 60)
        self.right_button.setFixedSize(60, 60)
        
                # set icons for the buttons up.png
        self.up_button.setIconSize(self.up_button.size())
        self.up_button.setIconSize(QSize(icon_size, icon_size))
        self.up_button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "up.png")))
        self.down_button.setIconSize(self.down_button.size())
        self.down_button.setIconSize(QSize(icon_size, icon_size))
        self.down_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"down.png"))))
        self.left_button.setIconSize(self.left_button.size())
        self.left_button.setIconSize(QSize(icon_size, icon_size))
        self.left_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"left.png"))))
        self.right_button.setIconSize(self.right_button.size())
        self.right_button.setIconSize(QSize(icon_size, icon_size))
        self.right_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"right.png"))))


        dpad_layout.addWidget(self.up_button, 0, 1)
        dpad_layout.addWidget(self.down_button, 2, 1)
        dpad_layout.addWidget(self.left_button, 1, 0)
        dpad_layout.addWidget(self.right_button, 1, 2)

        # Action buttons
        action_buttons_layout = QVBoxLayout()
        self.stop_button = QPushButton("Stop")
        self.auto_button = QPushButton("Auto")
        
        self.auto_button.setCheckable(True)
        self.auto_button.setChecked(False)
        self.auto_button.toggled.connect(self.auto_button_clicked)
        
        action_buttons_layout.addWidget(self.stop_button)
        action_buttons_layout.addWidget(self.auto_button)

        # Velocity slider and mode
        self.velocity_slider = QSlider(Qt.Orientation.Horizontal)
        self.velocity_slider.setRange(0, 255)
        self.velocity_slider.setValue(50)

        # Connect signals
        self.up_button.clicked.connect(self.up_button_clicked)
        self.down_button.clicked.connect(self.down_button_clicked)
        self.left_button.clicked.connect(self.left_button_clicked)
        self.right_button.clicked.connect(self.right_button_clicked)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        self.velocity_slider.valueChanged.connect(self.adjust_velocity)

        # Add widgets to controls layout
        controls_layout.addLayout(dpad_layout)
        controls_layout.addLayout(action_buttons_layout)
        controls_layout.addWidget(self.velocity_slider)

        # Right panel (Video Feed)
        self.video_label = QLabel()
        self.video_label.setText("Video Feed")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.video_label.setStyleSheet("border: 1px solid black;")  # Optional border for clarity

        # Add layouts to main layout
        main_layout.addWidget(controls_frame)
        main_layout.addWidget(self.video_label, stretch=1)

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
            self.video_label.setPixmap(QPixmap.fromImage(q_img))
            

    def send_command(self, command):
        speed = self.velocity_slider.value()
        message = {
            "command": command,
            "speed": speed,
            "continuous": self.is_auto_mode
        }
        self.mqtt_client.publish(MQTT_TOPIC, json.dumps(message))
        print(f"Command Sent: {message}")

    def adjust_velocity(self):
        self.send_command(self.last_message)
        print(f"Velocity Adjusted: ")

    def closeEvent(self, event):
        self.capture.release()
        self.mqtt_client.disconnect()  # Disconnect MQTT client
        super().closeEvent(event)

    def up_button_clicked(self):
        """Handles the up button click."""
        self.send_command("FORWARD")
        self.last_message = "FORWARD"
        print("Up button clicked: Moving FORWARD")

    def down_button_clicked(self):
        """Handles the down button click."""
        self.send_command("BACKWARD")
        self.last_message = "BACKWARD"
        print("Down button clicked: Moving BACKWARD")

    def left_button_clicked(self):
        """Handles the left button click."""
        self.send_command("LEFT")
        self.last_message = "LEFT"
        print("Left button clicked: Turning LEFT")

    def right_button_clicked(self):
        """Handles the right button click."""
        self.send_command("RIGHT")
        self.last_message = "RIGHT"
        print("Right button clicked: Turning RIGHT")

    def stop_button_clicked(self):
        """Handles the stop button click."""
        self.send_command("STOP")
        self.last_message = "STOP"
        print("Stop button clicked: Stopping the robot")

    def auto_button_clicked(self):
        """Handles the auto button click."""
        self.is_auto_mode = not self.is_auto_mode
        self.send_command(self.last_message)
        print("Auto button clicked: Switching to AUTO mode")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotCarControlApp()
    window.show()
    sys.exit(app.exec())