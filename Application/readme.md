# Robot Car Control Application

This application is a GUI-based control system for a robot car that includes real-time video streaming and MQTT-based communication. It is built using PyQt6 and OpenCV.

## Features

- **Real-Time Video Streaming**: Receives video feed via MQTT and displays it.
- **Robot Control**: Move the robot in multiple directions (Forward, Backward, Left, Right).
- **Velocity Adjustment**: Control speed using a slider.
- **Auto Mode**: Toggle automatic movement mode.
- **Stop Command**: Instantly stop the robot.

## Dependencies

- Python 3.x
- PyQt6
- OpenCV
- Paho MQTT
- NumPy

## Installation

1. Install dependencies:

   ```bash
   pip install PyQt6 opencv-python paho-mqtt numpy
   ```

2. Ensure MQTT broker configuration in the script matches your environment.

3. Place the control icons (`up.png`, `down.png`, `left.png`, `right.png`) and `style.qss` in the same directory.

## Usage

1. Run the script:

   ```bash
   python main.py
   ```

2. Use the control buttons and slider to interact with the robot.
