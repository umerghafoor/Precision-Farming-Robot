# Features  

## 1. **Weed Detection and Targeting**

The system employs basic image processing techniques, such as thresholding, to detect weeds represented by simple patterns like dots or marks in the camera feed. Once a target is identified, the robot's laser pointer is used for precise alignment, ensuring accurate targeting. This ability to pinpoint weeds allows for efficient and automated intervention, reducing the need for manual labor or herbicide application in the future phases of development.

## 2. **Modular System Design**

The project is built around a modular architecture consisting of two primary components: the **Rover** and the **Header**. The Rover, equipped with DC or stepper motors, provides mobility, while the Header carries the camera, servo motor, and laser pointer. This separation of concerns allows each module to function independently, enabling parallel development and easy upgrades. This design enhances system flexibility, making it easier to integrate advanced sensors, machine learning algorithms, or GPS technology as the project progresses.

## 3. **Communication and Control**

To ensure seamless communication between the robot and the control systems, the project uses the MQTT protocol, a lightweight messaging protocol suited for IoT applications. Data transmission occurs through two main topics: the **Video Topic**, which streams the camera feed in UTF-8 format, and the **Control Topic**, which transmits control commands in JSON format. This enables efficient data exchange with minimal latency, supporting real-time operation and control of the robot from both desktop and mobile applications.

## 4. **Custom Applications**

The project is supported by two custom applications that offer easy control and monitoring. The **Desktop Application** is developed using PyQt6 and provides a simple interface for manual control of the robot’s movement, as well as task scheduling functionalities. The **Mobile Application**, built using Flutter, allows users to stream live video from the robot’s camera, enabling on-the-go monitoring. Both applications connect to the robot via MQTT, offering real-time feedback and control from anywhere.

## 5. **Compact and Scalable Prototype**

The robot is designed to be both compact and scalable. The chassis is constructed using lightweight aluminum and wood, providing a stable yet portable base for the components. While the prototype currently focuses on basic navigation and weed detection, the modular approach ensures scalability, enabling easy upgrades for advanced navigation, machine learning-based weed identification, and autonomous operation. The scalable nature of the design allows it to evolve into a fully functional precision farming robot for real-world applications.

## 6. **Hardware Integration**

The robot is powered by an **ESP32 microcontroller**, which manages motor and servo control, as well as communication via MQTT. The **L298N motor driver** ensures smooth movement for the Rover by controlling the motors with precise speed and direction. Additionally, the laser pointer’s alignment is controlled through a servo motor, making the system capable of fine-tuning its targeting precision. This hardware integration enables effective navigation and targeting, forming the backbone of the robot’s functionality.

## 7. **Sustainability and Innovation**

One of the key goals of this project is to support sustainable farming practices by reducing the reliance on herbicides. By automating weed detection and targeting, the system minimizes the environmental impact associated with traditional weed management methods. This approach not only improves resource efficiency but also serves as a foundation for future innovations in precision farming. The system is designed to be adaptable, allowing for the incorporation of more advanced technologies as they become available.

## 8. **Results-Oriented Functionality**

The system has been successfully tested in controlled environments, demonstrating accurate movement and targeting capabilities. The robot’s ability to follow control commands and adjust the laser pointer to target weeds has been validated. Furthermore, real-time video streaming and control commands were transmitted seamlessly through MQTT, ensuring a smooth user experience with minimal latency. These results indicate that the prototype meets its objectives, establishing a solid foundation for further development and refinement.
