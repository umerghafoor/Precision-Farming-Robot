#ifndef CONSTANTS_H
#define CONSTANTS_H

#define ENA_M1 21
#define IN1_M1 22
#define IN2_M1 23
#define ENB_M2 5
#define IN3_M2 18
#define IN4_M2 19
#define ENA_M3 15
#define IN1_M3 0
#define IN2_M3 2
#define ENB_M4 17
#define IN3_M4 16
#define IN4_M4 4

// Servo pin
#define SERVO_PIN 32

// LED pin for indication
#define LED_PIN 2

// MQTT Broker details
#define MQTT_SERVER "192.168.240.180" // Replace with your broker's IP
#define MQTT_PORT 1883
#define SUBSCRIBE_TOPIC "robot/control"
#define PUBLISH_TOPIC "robot/status"

// WiFi credentials
#define SSID "Umer"
#define PASSWORD "umerghafoor1"

#endif