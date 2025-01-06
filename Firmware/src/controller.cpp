#include <Arduino.h>
#include "controller.h"
#include "constants.h"

Direction currentDirection = STOP;
int currentSpeed = 255;
int currentAngle = 0;

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

void executeCommandControls(String command, int speed, int stearAngle, bool continuous) {
    // Execute commands based on JSON input
    if (command == "FORWARD") {
        moveForward(speed);
        isMoving = continuous;
        currentDirection = FORWARD;
        currentSpeed = speed;
    } else if (command == "BACKWARD") {
        moveBackward(speed);
        isMoving = continuous;
        currentDirection = BACKWARD;
        currentSpeed = speed;
    } else if (command == "LEFT") {
        turnLeft(speed);
        isMoving = continuous;
        currentDirection = LEFT;
        currentSpeed = speed;
    } else if (command == "RIGHT") {
        turnRight(speed);
        isMoving = continuous;
        currentDirection = RIGHT;
        currentSpeed = speed;
    } else if (command == "STOP") {
        stopMotors();
        isMoving = 0;
    } else if (command == "FORWARD_LEFT") {
        moveForwardLeft(speed);
        isMoving = continuous;
        currentDirection = FORWARD_LEFT;
        currentSpeed = speed;
        currentAngle = stearAngle;
    } else if (command == "FORWARD_RIGHT") {
        moveForwardRight(speed);
        isMoving = continuous;
        currentDirection = FORWARD_RIGHT;
        currentSpeed = speed;
        currentAngle = stearAngle;
    } else if (command == "BACKWARD_LEFT") {
        moveBackwardLeft(speed);
        isMoving = continuous;
        currentDirection = BACKWARD_LEFT;
        currentSpeed = speed;
        currentAngle = stearAngle;
    } else if (command == "BACKWARD_RIGHT") {
        moveBackwardRight(speed);
        isMoving = continuous;
        currentDirection = BACKWARD_RIGHT;
        currentSpeed = speed;
        currentAngle = stearAngle;
    } else {
        Serial.println("Unknown command: " + command);
    }
    // delay(500);
}

void excuteCommandPointer(int angle) 
{
    myServo.write(angle);
    Serial.println("Servo moved to: " + String(angle));
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
      case FORWARD_LEFT:
        moveForwardLeft(currentSpeed);
        break;
      case FORWARD_RIGHT:
        moveForwardRight(currentSpeed);
        break;
      case BACKWARD_LEFT:
        moveBackwardLeft(currentSpeed);
        break;
      case BACKWARD_RIGHT:
        moveBackwardRight(currentSpeed);
        break;
      default:
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

void moveForwardLeft(int speed)
{
  int strearingFactor = currentAngle/90;
  int leftSpeed = speed - (speed * strearingFactor);
  // Motor 1
  analogWrite(ENA_M1, speed);
  digitalWrite(IN1_M1, HIGH);
  digitalWrite(IN2_M1, LOW);

  // Motor 2
  analogWrite(ENB_M2, leftSpeed);
  digitalWrite(IN3_M2, HIGH);
  digitalWrite(IN4_M2, LOW);

  // Motor 3
  analogWrite(ENA_M3, speed);
  digitalWrite(IN1_M3, HIGH);
  digitalWrite(IN2_M3, LOW);

  // Motor 4
  analogWrite(ENB_M4, leftSpeed);
  digitalWrite(IN3_M4, LOW);
  digitalWrite(IN4_M4, HIGH);

  Serial.println("Moving forward left at speed: " + String(speed));
}

void moveForwardRight(int speed){
  int strearingFactor = currentAngle/90;
  int rightSpeed = speed - (speed * strearingFactor);
  // Motor 1
  analogWrite(ENA_M1, rightSpeed);
  digitalWrite(IN1_M1, HIGH);
  digitalWrite(IN2_M1, LOW);

  // Motor 2
  analogWrite(ENB_M2, speed);
  digitalWrite(IN3_M2, HIGH);
  digitalWrite(IN4_M2, LOW);

  // Motor 3
  analogWrite(ENA_M3, rightSpeed);
  digitalWrite(IN1_M3, HIGH);
  digitalWrite(IN2_M3, LOW);

  // Motor 4
  analogWrite(ENB_M4, speed);
  digitalWrite(IN3_M4, LOW);
  digitalWrite(IN4_M4, HIGH);

  Serial.println("Moving forward right at speed: " + String(speed));
}

void moveBackwardLeft(int speed)
{
  int strearingFactor = currentAngle/90;
  int leftSpeed = speed - (speed * strearingFactor);
  // Motor 1
  analogWrite(ENA_M1, speed);
  digitalWrite(IN1_M1, LOW);
  digitalWrite(IN2_M1, HIGH);

  // Motor 2
  analogWrite(ENB_M2, leftSpeed);
  digitalWrite(IN3_M2, LOW);
  digitalWrite(IN4_M2, HIGH);

  // Motor 3
  analogWrite(ENA_M3, speed);
  digitalWrite(IN1_M3, LOW);
  digitalWrite(IN2_M3, HIGH);

  // Motor 4
  analogWrite(ENB_M4, leftSpeed);
  digitalWrite(IN3_M4, HIGH);
  digitalWrite(IN4_M4, LOW);

  Serial.println("Moving backward left at speed: " + String(speed));
}

void moveBackwardRight(int speed)
{
  int strearingFactor = currentAngle/90;
  int rightSpeed = speed - (speed * strearingFactor);
  // Motor 1
  analogWrite(ENA_M1, rightSpeed);
  digitalWrite(IN1_M1, LOW);
  digitalWrite(IN2_M1, HIGH);

  // Motor 2
  analogWrite(ENB_M2, speed);
  digitalWrite(IN3_M2, LOW);
  digitalWrite(IN4_M2, HIGH);

  // Motor 3
  analogWrite(ENA_M3, rightSpeed);
  digitalWrite(IN1_M3, LOW);
  digitalWrite(IN2_M3, HIGH);

  // Motor 4
  analogWrite(ENB_M4, speed);
  digitalWrite(IN3_M4, HIGH);
  digitalWrite(IN4_M4, LOW);

  Serial.println("Moving backward right at speed: " + String(speed));
}
