#pragma once

#include <ESP32Servo.h>
#include <ArduinoJson.h>

enum Direction {
  FORWARD,
  BACKWARD,
  LEFT,
  RIGHT,
  STOP
};


void setup_actuaters();
void executeCommand(String command, int speed, int angle, bool continuous);
void controlRobot();
void moveForward(int speed);
void moveBackward(int speed);
void turnLeft(int speed);
void turnRight(int speed);
void stopMotors();