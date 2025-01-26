#!/usr/bin/env python3
import base64
import os
import sys
import cv2
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QGridLayout, QFrame,QDial
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QImage, QPixmap, QIcon

from ControllerWidget import ControllerWidget
from ros_messages import create_robot_control_node, destroy_robot_control_node


icon_size = 50

class RobotCarControlApp(QWidget):
    def __init__(self, robot_control_node):
        super().__init__()
        self.init_ui()
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # check varibles
        self.last_command = "STOP"
        self.is_auto_mode = False
        
        self.userdata = {'frame': None}

        self.robot_control_node = robot_control_node
        
    def init_ui(self):
        # Main layout
        main_layout = QHBoxLayout()

        # Left panel (Controls)
        controls_frame = QFrame()
        controls_frame.setFixedWidth(200)
        controls_layout = QVBoxLayout()
        controls_frame.setLayout(controls_layout)
        dpad_layout = QGridLayout()

        # D-pad buttons with arrows
        self.up_button = QPushButton("\u2191")
        self.down_button = QPushButton("\u2193")
        self.left_button = QPushButton("\u2190")
        self.right_button = QPushButton("\u2192")
        self.upleft_button = QPushButton("\u2196")
        self.upright_button = QPushButton("\u2197")
        self.downleft_button = QPushButton("\u2199")
        self.downright_button = QPushButton("\u2198")

        frame = QFrame(self)
        frame.setFixedSize(200, 200)
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        self.pygame_widget = ControllerWidget(width=180, height=180, anchor_radius=20, drag_radius=10, max_drag_distance=80)
        self.pygame_widget.drag_info_signal.connect(self.controller_drag)
        self.pygame_widget.set_anchor_color((236, 239, 244))
        self.pygame_widget.set_drag_color((236, 239, 244))
        self.pygame_widget.set_max_drag_circle_color((236, 239, 244))
        self.pygame_widget.set_background_color( (30, 30, 46))
        self.pygame_widget.set_outer_anchor_radius(10)
        self.pygame_widget.set_center_anchor_radius(10)
        self.pygame_widget.set_drag_line_thickness(18)

        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(self.pygame_widget)

        # Settings for the buttons
        self.up_button.setFixedSize(60, 60)
        self.down_button.setFixedSize(60, 60)
        self.left_button.setFixedSize(60, 60)
        self.right_button.setFixedSize(60, 60)
        self.upleft_button.setFixedSize(60, 60)
        self.upright_button.setFixedSize(60, 60)
        self.downleft_button.setFixedSize(60, 60)
        self.downright_button.setFixedSize(60, 60)
        
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
        self.upleft_button.setIconSize(self.upleft_button.size())
        self.upleft_button.setIconSize(QSize(icon_size, icon_size))
        self.upleft_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"upleft.png"))))
        self.upright_button.setIconSize(self.upright_button.size())
        self.upright_button.setIconSize(QSize(icon_size, icon_size))
        self.upright_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"upright.png"))))
        self.downleft_button.setIconSize(self.downleft_button.size())
        self.downleft_button.setIconSize(QSize(icon_size, icon_size))
        self.downleft_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"downleft.png"))))
        self.downright_button.setIconSize(self.downright_button.size())
        self.downright_button.setIconSize(QSize(icon_size, icon_size))
        self.downright_button.setIcon(QIcon(QIcon(os.path.join(os.path.dirname(__file__),"downright.png"))))
                                      
        dpad_layout.addWidget(self.up_button, 0, 1)
        dpad_layout.addWidget(self.down_button, 2, 1)
        dpad_layout.addWidget(self.left_button, 1, 0)
        dpad_layout.addWidget(self.right_button, 1, 2)
        dpad_layout.addWidget(self.upleft_button, 0, 0)
        dpad_layout.addWidget(self.upright_button, 0, 2)
        dpad_layout.addWidget(self.downleft_button, 2, 0)
        dpad_layout.addWidget(self.downright_button, 2, 2)

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
        self.velocity_slider = QSlider(Qt.Orientation.Vertical)
        self.velocity_slider.setRange(0, 255)
        self.velocity_slider.setValue(50)
        self.velocity_slider.setFixedWidth(24)

        self.stearAngle_slider = QDial()
        self.stearAngle_slider.setRange(0, 90)
        self.stearAngle_slider.setValue(0)
        self.stearAngle_slider.setNotchesVisible(True)
        self.stearAngle_slider.setNotchTarget(5)
        self.stearAngle_slider.setWrapping(False)

        # Connect signals
        self.up_button.pressed.connect(lambda: self.start_continuous_command("FORWARD"))
        self.up_button.released.connect(self.stop_continuous_command)
        self.down_button.pressed.connect(lambda: self.start_continuous_command("BACKWARD"))
        self.down_button.released.connect(self.stop_continuous_command)
        self.left_button.pressed.connect(lambda: self.start_continuous_command("LEFT"))
        self.left_button.released.connect(self.stop_continuous_command)
        self.right_button.pressed.connect(lambda: self.start_continuous_command("RIGHT"))
        self.right_button.released.connect(self.stop_continuous_command)
        self.upleft_button.pressed.connect(lambda: self.start_continuous_command("FORWARD_LEFT"))
        self.upleft_button.released.connect(self.stop_continuous_command)
        self.upright_button.pressed.connect(lambda: self.start_continuous_command("FORWARD_RIGHT"))
        self.upright_button.released.connect(self.stop_continuous_command)
        self.downleft_button.pressed.connect(lambda: self.start_continuous_command("BACKWARD_LEFT"))
        self.downleft_button.released.connect(self.stop_continuous_command)
        self.downright_button.pressed.connect(lambda: self.start_continuous_command("BACKWARD_RIGHT"))
        self.downright_button.released.connect(self.stop_continuous_command)

        self.stop_button.clicked.connect(self.stop_button_clicked)
        self.velocity_slider.valueChanged.connect(self.adjust_velocity)
        self.stearAngle_slider.valueChanged.connect(self.adjust_stearAngle)

        # Add widgets to controls layout
        controls_layout.addLayout(dpad_layout)
        action_buttons_layout.addWidget(self.stearAngle_slider)
        othercontrols_layout = QHBoxLayout()
        othercontrols_layout.addWidget(self.velocity_slider)
        othercontrols_layout.addLayout(action_buttons_layout)
        controls_layout.addLayout(othercontrols_layout)
        controls_layout.addWidget(frame)

        # Right panel (Video Feed)
        self.video_label = QLabel()
        self.video_label.setText("Video Feed")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add layouts to main layout
        main_layout.addWidget(controls_frame)
        main_layout.addWidget(self.video_label, stretch=1)

        self.setLayout(main_layout)
        self.setWindowTitle("Robot Car Control")

        # Load QSS Stylesheet
        self.load_stylesheet()
    
    def start_continuous_command(self, command):
        print(f"Command Sent: {command}")
        self.last_command = command
        self.robot_control_node.publish_control_command(command)

    def stop_continuous_command(self):
        print(f"Command Sent: {self.last_command}")
        if not self.is_auto_mode:
            self.robot_control_node.publish_control_command("STOP")

    def controller_drag(self, drag_length, drag_angle):
        """Handle the printed drag information in the required format."""
        
        stearAngle = 0

        if 0 <= drag_angle < 90:
            command = 'FORWARD_RIGHT'
            stearAngle = 90 - int(drag_angle)
        elif 90 <= drag_angle < 180:
            command = 'FORWARD_LEFT'
            stearAngle = int(drag_angle) - 90
        elif -180 <= drag_angle < -90:
            command = 'BACKWARD_LEFT'
            stearAngle = 90 -( int(drag_angle) + 180)
        else:
            command = 'BACKWARD_RIGHT'
            stearAngle = 90 + int(drag_angle)

        # Calculate speed as a percentage of max drag distance
        speed = int(drag_length / self.pygame_widget.max_drag_distance * 255)


        if drag_length == 0:
            command = self.last_command

        current_time = time.time()
        if not hasattr(self, '_last_message_time') or (current_time - self._last_message_time >= 0.3) or speed == 0:
            print(f"Command Sent: {command} Speed: {speed} SteerAngle: {stearAngle}")
            self._last_message_time = current_time
            self.robot_control_node.publish_control_command(command)
            self.robot_control_node.publish_velocity(float(speed))
            self.robot_control_node.publish_steering_angle(float(stearAngle))


    def load_stylesheet(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "style.qss"), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("QSS file not found. Using default styles.")

    def update_frame(self):
        if self.userdata['frame'] is not None:
            # Retrieve the latest frame
            frame = self.userdata['frame']
            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            step = channel * width
            q_img = QImage(frame_rgb.data, width, height, step, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))


    def adjust_velocity(self):
        velocity = float(self.velocity_slider.value())
        print(f"Velocity Adjusted: {velocity}")
        self.robot_control_node.publish_velocity(velocity)

    def adjust_stearAngle(self):
        stearangle = float(self.stearAngle_slider.value())
        print(f"StearAngle Adjusted: ", stearangle)
        self.robot_control_node.publish_steering_angle(stearangle)

    def closeEvent(self, event):
        self.capture.release()
        super().closeEvent(event)

    def auto_button_clicked(self):
        """Handles the auto button click."""
        self.is_auto_mode = not self.is_auto_mode
        if self.is_auto_mode:
            self.auto_button.setStyleSheet("background-color: green;")
            self.auto_button.setText("Auto Mode ON")
        else:
            self.auto_button.setStyleSheet("")
            self.auto_button.setText("Auto Mode OFF")
        
        print("Auto button clicked: Switching to AUTO mode")
        self.robot_control_node.publish_auto_mode(self.is_auto_mode)
    
    def stop_button_clicked(self):
        """Handles the stop button click."""
        self.last_command = "STOP"
        print("Stop button clicked: Stopping the robot")
        self.robot_control_node.publish_control_command("STOP")

def main(args=None):

    robot_control_node = create_robot_control_node()

    app = QApplication(sys.argv)
    window = RobotCarControlApp(robot_control_node)
    window.show()
    app.exec()
    destroy_robot_control_node(robot_control_node)

if __name__ == '__main__':
    main()