import cv2
import paho.mqtt.client as mqtt
import base64

# MQTT configuration
broker_address = "192.168.18.29"  # Replace with your Mosquitto broker address
port = 1883
topic = "video/stream"

# Initialize the MQTT client
client = mqtt.Client()
client.connect(broker_address, port)

# Start video capture
cap = cv2.VideoCapture(0)  # 0 for the default camera

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Encode the frame as JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    jpeg_data = base64.b64encode(buffer).decode('utf-8')

    # Publish the frame to the MQTT broker
    client.publish(topic, jpeg_data)

    # Display the frame locally (optional)
    cv2.imshow('Streaming', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
client.disconnect()
