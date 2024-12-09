#include <Arduino.h>
#include "controller.h"
#include "constants.h"

Direction currentDirection = STOP;
int currentSpeed = 255;

Servo myServo;

int isMoving = 0;

void setup_actuaters() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);

  // Servo initialization
  myServo.attach(SERVO_PIN);
  myServo.write(90);

}

void executeCommand(String command, int speed, int angle, bool continuous) {
    // Execute commands based on JSON input
    if (command == "FORWARD") {
        moveForward(speed);
        if (continuous) {
            isMoving = 1;
            currentDirection = FORWARD;
            currentSpeed = speed;
        }
    } else if (command == "BACKWARD") {
        moveBackward(speed);
        if (continuous) {
            isMoving = 1;
            currentDirection = BACKWARD;
            currentSpeed = speed;
        }
    } else if (command == "LEFT") {
        turnLeft(speed);
        if (continuous) {
            isMoving = 1;
            currentDirection = LEFT;
            currentSpeed = speed;
        }
    } else if (command == "RIGHT") {
        turnRight(speed);
        if (continuous) {
            isMoving = 1;
            currentDirection = RIGHT;
            currentSpeed = speed;
        }
    } else if (command == "STOP") {
        stopMotors();
        isMoving = 0;
    } else if (command == "SERVO") {
        myServo.write(angle);
        Serial.println("Servo moved to: " + String(angle));
    } else {
        Serial.println("Unknown command: " + command);
    }
}


void controlRobot() {
  switch(currentDirection) {
    case FORWARD:
      moveForward(currentSpeed);
      break;
    case BACKWARD:
      moveBackward(currentSpeed);
      break;
    case LEFT:
      turnLeft(currentSpeed);
      break;
    case RIGHT:
      turnRight(currentSpeed);
      break;
    case STOP:
      stopMotors();
      break;
  }
}

// Motor control functions
void moveForward(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("Moving forward at speed: " + String(speed));
}

void moveBackward(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  Serial.println("Moving backward at speed: " + String(speed));
}

void turnLeft(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("Turning left at speed: " + String(speed));
}

void turnRight(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  Serial.println("Turning right at speed: " + String(speed));
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  Serial.println("Motors stopped");
}
