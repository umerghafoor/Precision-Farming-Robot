#pragma once

#include <PubSubClient.h>
#include <WiFi.h>

struct Command {
    String command;
    int speed;
    int angle;
    bool continuous;
};


// WiFi and MQTT clients
extern WiFiClient espClient;
extern PubSubClient client;

void setup_wifi();
void connectMQTT();
void reconnect();
void callback(char* topic, byte* payload, unsigned int length);
void send_message(String message);
