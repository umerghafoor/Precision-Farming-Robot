#include <Arduino.h>
#include <controller.h>
#include <mqtt_broker.h>

void setup() {
  Serial.begin(115200);
  setup_actuaters();

  setup_wifi();
  connectMQTT();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  controlRobot();
  // stopMotors();

  send_message("Robot is moving in direction: ");

}
