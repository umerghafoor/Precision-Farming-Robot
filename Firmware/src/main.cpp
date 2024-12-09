#include <Arduino.h>
#include <controller.h>
#include <mqtt_broker.h>

void setup() {
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

  send_message("Robot is moving in direction: ");

}
