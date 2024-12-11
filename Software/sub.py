import cv2
import paho.mqtt.client as mqtt
import base64
import numpy as np

# MQTT configuration
broker_address = "192.168.18.29"
port = 1883
topic = "video/stream"

# Callback function for receiving messages
def on_message(client, userdata, msg):
    jpeg_data = base64.b64decode(msg.payload)
    np_array = np.frombuffer(jpeg_data, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if frame is not None:
        cv2.imshow('Received Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            client.disconnect()

# Initialize the MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, port)
client.subscribe(topic)

# Start the MQTT loop to listen for messages
client.loop_forever()

cv2.destroyAllWindows()
