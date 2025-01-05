# Precision-Farming-Robot

This repository contains the code and instructions for controlling a precision farming robot using an **ESP32** microcontroller. The robot can be controlled via a **GUI** and **MQTT** communication for movement control, live video streaming, and servo operation. This project aims to help automate tasks like farming and environmental monitoring using robotics.

## Table of Contents

1. [Features](#features)
2. [Dependencies](#dependencies)
   - [Firmware](#firmware)
   - [Software](#software)
   - [Hardware](#hardware)
3. [Setup Instructions](#setup-instructions)
   - [Firmware Setup](#1-firmware-setup)
   - [Software Setup](#2-software-setup)
   - [Application Setup](#3-application-setup)
4. [Usage](#usage)
   - [Robot Control](#robot-control)
   - [Video Streaming](#video-streaming)
   - [Motor Control](#motor-control)
   - [MQTT Commands](#mqtt-commands)
5. [Folder Structure](#folder-structure)
6. [License](#license)
7. [TODO](#todo)

## Features

- **Robot Control**: Control the robot's movement using a GUI and MQTT-based commands.
- **Live Video Feed**: Stream video from the robot to the control application via MQTT.
- **Wi-Fi and MQTT Communication**: Connect the ESP32 to Wi-Fi and communicate with a broker for control and feedback.
- **Robot Motor Control**: Control up to four motors for movement and a servo for additional movement or functionality.

## Dependencies

### Firmware

- **ESP32 Board Support** for Arduino IDE or PlatformIO.
- **Required Libraries**:
  - `WiFi.h` (for Wi-Fi connectivity)
  - `PubSubClient` (for MQTT communication)
  - `controller.h` (for actuator control)
  - `mqtt_broker.h` (for MQTT setup)

### Software

- **Python 3.x**
- **OpenCV** (for video processing)
- **Paho MQTT** (for MQTT communication)
- **NumPy** (for handling video data)

### Hardware

- **ESP32 Development Board**
- **DC Motors** (4 Motors for M1, M2, M3, M4)
- **Servo Motor**
- **Motor Driver** (L298N or similar)
- **Power Supply** for Motors and ESP32
- **Camera Module** (for video streaming)

## Setup Instructions

### 1. Firmware Setup

1. **Configure Wi-Fi credentials**: Edit the `mqtt_broker.h` file to add your Wi-Fi credentials and MQTT broker details.
2. **Upload firmware**: Upload the firmware to the ESP32 using Arduino IDE or PlatformIO.
3. **Connect hardware**: Connect the motors, motor driver, and camera according to the pin configuration found in the `Hardware/` folder.

### 2. Software Setup

1. **Install Python dependencies**:

   ```bash
   pip install opencv-python paho-mqtt numpy
   ```

2. **Run the Publisher (`pub.py`)** script to start streaming video from the robot.

3. **Run the Subscriber (`sub.py`)** script to view the live video stream.

### 3. Application Setup

1. **Install required libraries** for the GUI application:

   ```bash
   pip install PyQt6 paho-mqtt opencv-python
   ```

2. **Run the RobotCarControlApp** script to control the robot and view the video feed:

   ```bash
   python RobotCarControlApp.py
   ```

## Usage

### Robot Control

- Use the GUI to move the robot in four directions (up, down, left, right) and control its speed.
- Press the **Stop** button to halt the robot.
- Toggle the **Auto** button for autonomous control.

### Video Streaming

- The **Publisher** (`pub.py`) captures video from the robot’s camera and sends it to the MQTT broker.
- The **Subscriber** (`sub.py`) receives the video stream and displays it in a window.

### Motor Control

- Control the robot's four motors through the GUI, using buttons for directional movement and a slider for speed control.

### MQTT Commands

Control the robot using the following MQTT commands.

```shell
.\mosquitto_pub.exe -t robot/control -h <BROKER_IP> -m JSON_MESSAGE
.\mosquitto_sub.exe -t robot/control -h <BROKER_IP>
```

---

#### 1. **Forward Movement**

```json
{"command": "FORWARD", "speed": 100, "continuous": true, "stearAngle": 0}
```

#### 2. **Backward Movement**

```json
{"command": "BACKWARD", "speed": 100, "continuous": true, "stearAngle": 0}
```

#### 3. **Rotate Left**

```json
{"command": "LEFT", "speed": 100, "continuous": true, "stearAngle": 0}
```

#### 4. **Rotate Right**

```json
{"command": "RIGHT", "speed": 100, "continuous": true, "stearAngle": 0}
```

#### 5. **Turning Forward Right**

```json
{"command": "FORWARD_RIGHT", "speed": 100, "continuous": true, "stearAngle": 30}
```

#### 6. **Turning Forward Left**

```json
{"command": "FORWARD_LEFT", "speed": 100, "continuous": true, "stearAngle": 30}
```

#### 7. **Turning Backward Left**

```json
{"command": "BACKWARD_LEFT", "speed": 100, "continuous": true, "stearAngle": 30}
```

#### 8. **Turning Backward Right**

```json
{"command": "BACKWARD_RIGHT", "speed": 100, "continuous": true, "stearAngle": 30}
```

#### 9. **Stopping the Motors**

```json
{"command": "STOP"}
```

#### 10. **Controlling the Servo**

```json
{"command": "SERVO", "angle": 45}
```

## Folder Structure

```plaintext
├── Application/        # GUI application for robot control and video streaming
├── Firmware/           # ESP32 firmware for motor control and MQTT communication
├── Hardware/           # Pin configuration and hardware setup
├── Software/           # MQTT video streaming publisher and subscriber
└── README.md           # This file
```

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## TODO

- [ ] Implement autonomous pathfinding using sensors (e.g., ultrasonic, IR).
- [ ] Integrate additional sensors for environmental data (temperature, soil moisture).
- [ ] Develop and test the robot in real-world farming environments.
- [ ] Add features for battery monitoring and power-saving modes.
- [ ] Create an Android or iOS app for mobile control.
- [ ] Add advanced motor control algorithms for smoother movement.
- [ ] Implement a camera feed streaming feature with adjustable resolution.
- [ ] Optimize the GUI for better user experience.
- [ ] Add unit tests for the firmware and software components.
