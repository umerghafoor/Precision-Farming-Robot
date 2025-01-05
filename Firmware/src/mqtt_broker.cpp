#include "mqtt_broker.h"
#include <ArduinoJson.h>
#include <WiFi.h>
#include <controller.h>
#include <constants.h>

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
}


void connectMQTT()
{
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32_Robot")) {
      Serial.println("Connected to MQTT Broker!");
      client.subscribe(SUBSCRIBE_TOPIC);
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}


void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived on topic: ");
    Serial.println(topic);

    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, payload, length);

    if (error) {
        Serial.print("JSON Parsing failed: ");
        Serial.println(error.f_str());
        return;
    }

    String command = doc["command"] | "";
    int speed = doc["speed"] | 255;
    int angle = doc["angle"] | 90;
    int stearAngle = doc["stearAngle"] | 0;
    bool continuous = doc["continuous"] | false;

    executeCommand(command, speed, angle,stearAngle, continuous);
}

void send_message(String message) {
  static unsigned long lastMsg = 0;
  unsigned long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;

    JsonDocument statusJson;
    statusJson["status"] = "online";
    statusJson["battery"] = 95;
    char buffer[200];
    serializeJson(statusJson, buffer);

    client.publish(PUBLISH_TOPIC, buffer);
    Serial.println("Status published: " + String(buffer));
  }
}