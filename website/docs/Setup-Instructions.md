# Setup Instructions

## Table of Contents

1. [Directory structure](#1-directory-structure)
2. [Hardware Setup](#2-hardware-setup)
   1. [Motor Connection](#1-motor-connection)
   2. [Servo Motor for Laser Alignment](#2-servo-motor-for-laser-alignment)
   3. [Camera and Laser Pointer Installation](#3-camera-and-laser-pointer-installation)
   4. [Secure Mounting of Components](#4-secure-mounting-of-components)
   5. [Final Checks](#5-final-checks)
3. [Software Setup](#3-software-setup)
   1. [Install Required Software](#1-install-required-software)
   2. [Upload Code to ESP32](#2-upload-code-to-esp32)
   3. [Desktop Application Setup](#3-desktop-application-setup)
4. [Testing and Calibration](#4-testing-and-calibration)
   1. [Initial Testing](#1-initial-testing)
   2. [Calibrate Components](#2-calibrate-components)
5. [Troubleshooting](#5-troubleshooting)

## 1. Directory structure

```text
└── Precision-Farming-Robot/
    ├── README.md
    ├── LICENSE
    ├── Application/
    │   ├── readme.md
    │   ├── ControllerWidget.py
    │   ├── main.py
    │   └── style.qss
    ├── Firmware/
    │   ├── readme.md
    │   ├── platformio.ini
    │   ├── .gitignore
    │   ├── include/
    │   │   ├── README
    │   │   ├── constants.h
    │   │   ├── controller.h
    │   │   └── mqtt_broker.h
    │   ├── lib/
    │   │   └── README
    │   ├── src/
    │   │   ├── controller.cpp
    │   │   ├── main.cpp
    │   │   └── mqtt_broker.cpp
    │   ├── test/
    │   │   └── README
    │   └── .vscode/
    │       ├── extensions.json
    │       └── settings.json
    ├── Hardware/
    │   └── readme.md
    └── Software/
        ├── readme.md
        ├── aruco_mark_detection_module.py
        ├── dot_detection_module.py
        ├── dot_detection_module_mqtt._sub.py
        ├── main.py
        ├── pub.py
        ├── sub.py
        └── utility.py
```

## 2. Hardware Setup

### 1. **Motor Connection**

- **Attaching Motors to the Chassis**:  
    Secure the motors to the chassis using appropriate motor brackets and screws. Ensure the motors are positioned properly to allow smooth movement. Verify that the motor shafts align with the wheels or any other mechanical components you intend to use for movement.
- **Wiring the Motors to the Motor Driver**:  
    Connect the motors to the L298N motor driver as follows:

    **Motor 1**:  
  - `ENA_M1 (21)` for speed control (PWM).
  - `IN1_M1 (22)` and `IN2_M1 (23)` to control direction (high/low).

    **Motor 2**:  
  - `ENB_M2 (5)` for speed control (PWM).
  - `IN3_M2 (18)` and `IN4_M2 (19)` to control direction.

    **Motor 3**:  
  - `ENA_M3 (15)` for speed control.
  - `IN1_M3 (0)` and `IN2_M3 (2)` for direction control.

    **Motor 4**:  
  - `ENB_M4 (17)` for speed control.
  - `IN3_M4 (16)` and `IN4_M4 (4)` for direction control.

   These connections ensure that each motor can be individually controlled for precise movement and steering.

### 2. **Servo Motor for Laser Alignment**

- **Mounting the Servo Motor**:
    Attach the servo motor securely to the header module. Use screws or mounting brackets to ensure it stays in place during movement. The servo will be responsible for adjusting the angle of the laser, so make sure it's positioned to allow full rotation or adjustment.
- **Connecting the Servo**:  
    Wire the servo to the **`SERVO_PIN (32)`** on the ESP32. This pin will control the servo's rotation, allowing you to adjust the laser's alignment based on feedback or manual control.

### 3. **Camera and Laser Pointer Installation**

- **Mounting the Camera**:  
    Fix the camera onto the header module, ensuring it's aligned with the servo's range of motion. The camera should be positioned to capture the area in front of the robot, offering a clear view for any computer vision tasks or object detection applications.
- **Aligning the Laser Pointer**:  
    Attach the laser pointer to the same header module, making sure it's aligned with the camera. This alignment ensures that the laser can be used for accurate targeting or positioning. Double-check the alignment by testing the laser's focus and direction after the components are mounted.
- **Securing Components**:  
    All components, including the camera and laser pointer, should be securely fastened to avoid any shifting during movement. You can use mounting brackets, Velcro strips, or additional screws to ensure they remain in place.

### 4. **Secure Mounting of Components**

- **General Tips for Mounting**:  
     Ensure all components are securely mounted on the chassis. Loose components can cause instability during movement or affect performance. Use high-strength adhesives or screws for mounting, particularly for heavier components like the camera or motor driver.

- **Balance and Weight Distribution**:  
     Pay attention to the distribution of weight across the robot. Ideally, the center of gravity should be low and centered to improve stability. Distribute the components evenly to avoid tipping or erratic movements.

- **Cable Management**:  
     Carefully manage the wires between the components to avoid tangling or interference with moving parts. Use zip ties, cable clips, or channels to keep wires organized and out of the way. Ensure that the wires are long enough to reach each component without strain but short enough to avoid slack.

### 5. Final Checks

- **Power Supply**:  
     Ensure that the power supply can provide enough current to operate all the components (motors, ESP32, servo, camera, laser). If necessary, use a separate power source for motors and logic circuits to prevent power drops that could affect performance.

- **Testing the System**:  
     After mounting everything, run a series of tests. First, check the movement of the motors and servo to ensure correct wiring. Then, test the camera and laser alignment by activating the servo to move the laser and confirm it remains properly aligned with the camera.

Once all components are mounted, securely connected, and tested, your robot should be ready for further programming and functionality enhancements!

## 3. **Software Setup**

### 1. **Install Required Software**

- **Mosquitto MQTT Broker**:  
     Download and install Mosquitto to set up a local MQTT server. Follow these steps:
     1. Visit the [Mosquitto website](https://mosquitto.org/download/) to download the latest version for your operating system.
     2. Follow the installation instructions provided on the website.
     3. Once installed, start the Mosquitto service by running the command:

        ```bash
        mosquitto
        ```

     4. This will start the broker on the default port (1883), allowing devices to communicate over MQTT.

- **Python and Libraries**

- Install Python (version 3.x or above) on your machine from the [official Python website](https://www.python.org/downloads/).
- Install the required libraries for your desktop application by running:

    ```bash
    pip install -r requirements.txt
    ```

    Ensure that your `requirements.txt` file includes the necessary dependencies like:

  - `OpenCV`: For camera processing.
  - `Paho MQTT`: For MQTT communication.
  - `PyQt6`: For building the desktop GUI.

### 2. **Upload Code to ESP32**

- **Using Arduino IDE**
     If you're using Arduino IDE:
     1. Open **Arduino IDE**.
     2. Select the **ESP32 board**:
        - Go to **Tools > Board > ESP32 Dev Module** (or the specific ESP32 board you are using).
     3. Select the correct **COM port**:
        - Go to **Tools > Port** and select the appropriate port for your ESP32.
     4. Upload the code:
        - Make sure the code is properly configured to control motors and communicate via MQTT. Ensure that the Wi-Fi credentials and MQTT broker settings are correctly defined in the code.
        - Click **Upload** to flash the code to the ESP32.

- **Using PlatformIO**
     If you're using PlatformIO (within VSCode):
     1. Open **VSCode** and the PlatformIO extension.
     2. In **platformio.ini**, ensure that the ESP32 board is selected.
     3. Connect the ESP32 and select the correct **COM port**:
        - PlatformIO will detect the connected device, but if necessary, you can specify the port manually in the `platformio.ini` file.
     4. Upload the code:
        - Make sure the code is set up for controlling the motors and communication over MQTT, including the correct Wi-Fi and MQTT broker settings.
        - Click the **Upload** button in PlatformIO or run the following command in the terminal:

          ```bash
          pio run --target upload
          ```

- **Verify Settings in Code**

Ensure that the following settings are correctly configured:

- **Wi-Fi credentials**: Make sure the SSID and password are specified correctly for the network.

- **MQTT settings**: Verify that the IP address of the Mosquitto broker is set correctly, along with the MQTT topics for communication. For example:

```cpp
#define MQTT_SERVER "192.168.18.29" // Replace with your broker's IP
#define MQTT_PORT 1883
#define SUBSCRIBE_TOPIC "robot/control"
#define SUBSCRIBE_TOPIC_Pointer "robot/pointer"
#define PUBLISH_TOPIC "robot/status"
```

Once everything is uploaded and set up, the ESP32 will be ready to communicate with the MQTT broker, control the motors, and interact with the desktop application.

### 3. **Desktop Application Setup**  

- **PyQt6 Application**:
  - Open Application folder inside the main repo.
  - Run the application by executing `python main.py` or the appropriate start command.  
  - Ensure the application is connected to the MQTT broker for sending control commands.  
  - Check the user interface for manual control options and task scheduling.  

## 4. **Testing and Calibration**

### 1. **Initial Testing**

- After completing the hardware and software setup, power on the robot.  
- Open the desktop application to begin controlling the robot.  
- Verify that the robot can move, and the camera feed is visible on the control interface.  
- Check if the laser pointer aligns with detected targets accurately.

### 2. **Calibrate Components**

Here’s how you can approach the calibration and configuration of the components in your project:

- **Adjust the Servo Motor for Proper Targeting**:  
    The servo motor needs to be calibrated for precise targeting. This involves adjusting the servo to point the laser or camera at the target area.
  - If you have a known target, use the servo to move the laser or camera to the optimal position and verify if the target is correctly aligned with the camera's field of view.
  - Use the **DISTANCE** value to adjust the height of the servo and camera. Fine-tuning the servo will ensure the laser is pointing in the correct direction for effective weed detection.

- **Fine-Tune Image Processing Settings**:  
    To achieve optimal weed detection, you may need to adjust the image processing settings, particularly the thresholding parameters.
  - Thresholding is essential for distinguishing between weeds and the background in the image. Fine-tune the threshold values based on the lighting conditions and the appearance of weeds.
  - In your Python script (`main.py`), adjust the **DETECTION_MODE** parameter to select the appropriate mode for weed detection:
    - **"CIRCLE"**: Detect circular objects (useful for round weeds).
    - **"SHAPE"**: Detect specific shapes (useful for recognizing weeds with particular geometric characteristics).
    - **"ARUCO"**: Use ARUCO markers for detection (if you're using specific markers).
    - You can also adjust the thresholding and other processing parameters to improve the accuracy of weed detection.

- **Configuring the Python Script (`main.py`)**:
In your `main.py` file, set the values for the components and detection:

```python
# Configuration variables
DISTANCE = 27  # Height of the servo and camera in cm (adjust as needed)
SCALAR = 30  # Scale factor for processing or distance adjustment
BROKER = "192.168.18.29"  # Replace with your MQTT broker address
PORT = 1883  # MQTT broker port
TOPIC = "robot/pointer"  # MQTT topic for controlling the pointer/laser
TOPIC_VIDEO = "video/stream"  # MQTT topic for video stream
DETECTION_MODE = "CIRCLE"  # "CIRCLE", "SHAPE", "ARUCO" - Choose detection method
VIDEO_WIDTH = 640  # Width of video feed
VIDEO_HEIGHT = 360  # Height of video feed
```

#### Steps to Calibrate

1. **Set the correct `DISTANCE` value**:
   - This defines the height of the servo and camera. Adjust the value based on the actual physical height from the ground or platform to where the camera and servo are mounted.
   - Example: If the camera and servo are mounted 27 cm above the surface, set `DISTANCE = 27`.

2. **Fine-tune the `SCALAR` value**:  
   - The **SCALAR** variable could be used for adjusting the scale in calculations or for determining the relative distance to the target. This might be useful for distance-based adjustments or zoom levels in image processing.

3. **Set up the MQTT broker configuration**:  
   - Replace the `BROKER` value with the IP address of your Mosquitto MQTT broker (e.g., `BROKER = "192.168.18.29"`).
   - Make sure the MQTT server is running and accessible from the robot.

4. **Configure Detection Mode**:  
   - The `DETECTION_MODE` can be set to different modes depending on what kind of detection you want:
     - `"CIRCLE"`: Detects circular objects (ideal for circular weeds).
     - `"SHAPE"`: Detects shapes based on custom algorithms (ideal for irregularly shaped weeds).
     - `"ARUCO"`: Detects ARUCO markers (if you're using markers for precise positioning).

5. **Adjust Video Feed Resolution**:  
   - The `VIDEO_WIDTH` and `VIDEO_HEIGHT` values determine the resolution of the video stream. For example, setting `VIDEO_WIDTH = 640` and `VIDEO_HEIGHT = 360` gives a moderate resolution that balances performance and quality.

#### Final Steps

- Test the calibration by running the system and checking if the servo motor and camera are correctly aligned and focused on the target area.
- Fine-tune the image processing thresholds to make sure the weeds are detected accurately under different lighting conditions.

## 5. **Troubleshooting**

- **Connection Issues**:  
- Ensure the MQTT broker is running and accessible.  
- Verify the Wi-Fi connection for the ESP32.  
- Check the MQTT topic configurations in the code.  

- **Hardware Issues**:  
- Ensure that the motors are wired correctly to the driver and that the power supply is sufficient.  
- Test the servo motor and camera separately to ensure they are functioning properly.
