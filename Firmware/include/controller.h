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
void executeCommandControls(String command, int speed, int stearAngle, bool continuous);
void excuteCommandPointer(int angle);
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