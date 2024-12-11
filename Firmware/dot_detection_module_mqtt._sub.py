import base64
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json

# Constants
DISTANCE = 10
SCALAR = 30
BROKER = "192.168.18.29"  # Replace with your MQTT broker address
PORT = 1883  # MQTT broker port
TOPIC_VIDEO = "video/stream"  # Topic for video stream
TOPIC_CONTROL = "robot/control"  # Topic for control messages

# Initialize variables
frame = None

# Function to calculate the angle
def return_angle(cx, width):
    x = (cx / width) * SCALAR
    x = (SCALAR / 2) - x
    angle = np.arctan(x / DISTANCE)
    # Convert radians to degrees
    angle = np.degrees(angle)
    # return angle in int
    return int(angle)
    

# Callback function to receive video stream messages
def on_message(client, userdata, msg):
    global frame
    jpeg_data = base64.b64decode(msg.payload)
    np_array = np.frombuffer(jpeg_data, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

# Function to detect red dots in a line
def detect_red_dots_in_line():
    global frame

    # Initialize the MQTT client
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC_VIDEO)

    # Start MQTT loop in a separate thread
    client.loop_start()

    # Wait for frames to start arriving
    while frame is None:
        pass

    while True:
        if frame is not None:
            # Get frame dimensions
            height, width, _ = frame.shape

            # Define the horizontal strip (e.g., 10% of the frame height)
            strip_height = int(height * 0.1)
            y_start = height // 2 - strip_height // 2
            y_end = y_start + strip_height
            roi = frame[y_start:y_end, :]

            # Convert the ROI to HSV (Hue, Saturation, Value) color space
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Define range for red color in HSV space
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])

            # Create masks for red color
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            # Combine the two masks to capture all red shades
            mask = cv2.bitwise_or(mask1, mask2)

            # Find contours of the red dots
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Iterate through the contours and draw circles at their centroids
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # Minimum area to avoid noise
                    # Calculate the centroid of the contour
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"]) + y_start  # Add offset to match original frame

                        # Draw a circle at the centroid
                        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)  # Green circle

                        # Print the coordinates
                        print(f"Red dot found at: ({cx}, {cy})")

                        # Calculate angle
                        angle = return_angle(cx, width)

                        # Create JSON message
                        message = json.dumps({"command": "SERVO", "angle": angle})

                        # Publish the message to the MQTT broker
                        client.publish(TOPIC_CONTROL, message)

                        # Print the angle and MQTT message
                        print(f"Angle: ({angle})")
                        print(f"Published MQTT message: {message}")

            # Draw the ROI strip on the original frame for visualization
            cv2.rectangle(frame, (0, y_start), (width, y_end), (255, 0, 0), 2)

            # Display the resulting frame
            cv2.imshow('Red Dots Detection (Line)', frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release resources
    cv2.destroyAllWindows()
    client.loop_stop()
    client.disconnect()

# Call the function
detect_red_dots_in_line()