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

  // seting pin modes
  pinMode(ENA_M1, OUTPUT);
  pinMode(IN1_M1, OUTPUT);
  pinMode(IN2_M1, OUTPUT);
  pinMode(ENB_M2, OUTPUT);
  pinMode(IN3_M2, OUTPUT);
  pinMode(IN4_M2, OUTPUT);
  pinMode(ENA_M3, OUTPUT);
  pinMode(IN1_M3, OUTPUT);
  pinMode(IN2_M3, OUTPUT);
  pinMode(ENB_M4, OUTPUT);
  pinMode(IN3_M4, OUTPUT);
  pinMode(IN4_M4, OUTPUT);

  // Servo initialization
  myServo.attach(SERVO_PIN);
  myServo.write(90);

}

void executeCommand(String command, int speed, int angle, bool continuous) {
    // Execute commands based on JSON input
    if (command == "FORWARD") {
        moveForward(speed);
        if (continuous) {
            isMoving = continuous;
            currentDirection = FORWARD;
            currentSpeed = speed;
        }
    } else if (command == "BACKWARD") {
        moveBackward(speed);
        if (continuous) {
            isMoving = continuous;
            currentDirection = BACKWARD;
            currentSpeed = speed;
        }
    } else if (command == "LEFT") {
        turnLeft(speed);
        if (continuous) {
            isMoving = continuous;
            currentDirection = LEFT;
            currentSpeed = speed;
        }
    } else if (command == "RIGHT") {
        turnRight(speed);
        if (continuous) {
            isMoving = continuous;
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
  if (isMoving) {
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
}

// Motor control functions
void moveForward(int speed) {
  // Motor 1
  analogWrite(ENA_M1, speed);
  digitalWrite(IN1_M1, HIGH);
  digitalWrite(IN2_M1, LOW);
  
  // Motor 2
  analogWrite(ENB_M2, speed);
  digitalWrite(IN3_M2, HIGH);
  digitalWrite(IN4_M2, LOW);
  
  // Motor 3
  analogWrite(ENA_M3, speed);
  digitalWrite(IN1_M3, HIGH);
  digitalWrite(IN2_M3, LOW);
  
  // Motor 4
  analogWrite(ENB_M4, speed);
  digitalWrite(IN3_M4, HIGH);
  digitalWrite(IN4_M4, LOW);

  Serial.println("Moving forward at speed: " + String(speed));
}

void moveBackward(int speed) {
  // Motor 1
  analogWrite(ENA_M1, speed);
  digitalWrite(IN1_M1, LOW);
  digitalWrite(IN2_M1, HIGH);

  // Motor 2
  analogWrite(ENB_M2, speed);
  digitalWrite(IN3_M2, LOW);
  digitalWrite(IN4_M2, HIGH);

  // Motor 3
  analogWrite(ENA_M3, speed);
  digitalWrite(IN1_M3, LOW);
  digitalWrite(IN2_M3, HIGH);

  // Motor 4
  analogWrite(ENB_M4, speed);
  digitalWrite(IN3_M4, LOW);
  digitalWrite(IN4_M4, HIGH);

  Serial.println("Moving backward at speed: " + String(speed));
}

void turnLeft(int speed) {
  // Motor 1
  analogWrite(ENA_M1, speed);
  digitalWrite(IN1_M1, LOW);
  digitalWrite(IN2_M1, HIGH);

  // Motor 2
  analogWrite(ENB_M2, speed);
  digitalWrite(IN3_M2, HIGH);
  digitalWrite(IN4_M2, LOW);

  // Motor 3
  analogWrite(ENA_M3, speed);
  digitalWrite(IN1_M3, LOW);
  digitalWrite(IN2_M3, HIGH);

  // Motor 4
  analogWrite(ENB_M4, speed);
  digitalWrite(IN3_M4, HIGH);
  digitalWrite(IN4_M4, LOW);

  Serial.println("Turning left at speed: " + String(speed));
}

void turnRight(int speed) {
  // Motor 1
  analogWrite(ENA_M1, speed);
  digitalWrite(IN1_M1, HIGH);
  digitalWrite(IN2_M1, LOW);

  // Motor 2
  analogWrite(ENB_M2, speed);
  digitalWrite(IN3_M2, LOW);
  digitalWrite(IN4_M2, HIGH);

  // Motor 3
  analogWrite(ENA_M3, speed);
  digitalWrite(IN1_M3, HIGH);
  digitalWrite(IN2_M3, LOW);

  // Motor 4
  analogWrite(ENB_M4, speed);
  digitalWrite(IN3_M4, LOW);
  digitalWrite(IN4_M4, HIGH);

  Serial.println("Turning right at speed: " + String(speed));
}

void stopMotors() {

  // Motor 1
  analogWrite(ENA_M1, 0);
  digitalWrite(IN1_M1, LOW);
  digitalWrite(IN2_M1, LOW);

  // Motor 2
  analogWrite(ENB_M2, 0);
  digitalWrite(IN3_M2, LOW);
  digitalWrite(IN4_M2, LOW);

  // Motor 3
  analogWrite(ENA_M3, 0);
  digitalWrite(IN1_M3, LOW);
  digitalWrite(IN2_M3, LOW);

  // Motor 4
  analogWrite(ENB_M4, 0);
  digitalWrite(IN3_M4, LOW);
  digitalWrite(IN4_M4, LOW);

  Serial.println("Motors stopped");
}