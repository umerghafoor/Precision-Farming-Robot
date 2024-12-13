# ESP32 Robot Firmware

This firmware controls the ESP32-based robot, managing motor movements and MQTT communication for command execution.

## Features

- **Robot Control**: Processes movement commands and controls actuators.
- **Wi-Fi Connectivity**: Connects the ESP32 to a Wi-Fi network.
- **MQTT Communication**: Sends and receives messages from the MQTT broker.
- **Serial Debugging**: Provides real-time debugging information over serial.

## Dependencies

- Arduino IDE / PlatformIO
- ESP32 Board Support
- Required Libraries:
  - `WiFi.h`
  - `PubSubClient` (for MQTT)
  - `controller.h` (Custom actuator control)
  - `mqtt_broker.h` (Custom MQTT configuration)

## Installation

1. Install required libraries in Arduino IDE or PlatformIO.
2. Configure Wi-Fi and MQTT credentials in `mqtt_broker.h`.
3. Upload the code to your ESP32.

## Usage

1. Connect the ESP32 to your robot hardware.
2. Upload the firmware.
3. Monitor the serial output for debugging.
4. Control the robot via MQTT commands.
