#pragma once

#include <ESP32Servo.h>
#include <ArduinoJson.h>

enum Direction {
  FORWARD,
  BACKWARD,
  LEFT,
  RIGHT,
  STOP,
  FORWARD_LEFT,
  FORWARD_RIGHT,
  BACKWARD_LEFT,
  BACKWARD_RIGHT
};


void setup_actuaters();
void executeCommand(String command, int speed, int angle, int stearAngle, bool continuous);
void controlRobot();
void moveForward(int speed);
void moveBackward(int speed);
void turnLeft(int speed);
void turnRight(int speed);
void stopMotors();
void moveForwardLeft(int speed);
void moveForwardRight(int speed);
void moveBackwardLeft(int speed);
void moveBackwardRight(int speed);