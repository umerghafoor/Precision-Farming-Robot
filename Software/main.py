import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json
from PyQt6.QtWidgets import QApplication
import base64

from dot_detection_module import detect_circles, detect_any_shape
from aruco_mark_detection_module import detect_aruco_markers
from utility import save_profile, load_profile, HSVControlWindow

DISTANCE = 10
SCALAR = 30
BROKER = "192.168.18.29"  # Replace with your MQTT broker address
PORT = 1883  # MQTT broker port
TOPIC = "robot/control"
TOPIC_VIDEO = "video/stream" 
DETECTION_MODE = "ARUCO"  # "CIRCLE", "SHAPE", "ARUCO"

frame = None

def return_angle(cx, width):
    x = (cx / width) * SCALAR
    x = (SCALAR / 2) - x
    angle = np.arctan(x / DISTANCE)
    # Convert radians to degrees
    angle = np.degrees(angle)
    return int(angle) + 90

def get_calibartion_settings(frame, strip_thickness_factor):
    height, width, _ = frame.shape
    strip_height = int(height * strip_thickness_factor / 100)
    y_start = height // 2 - strip_height // 2
    y_end = y_start + strip_height
    roi = frame[y_start:y_end, :]
    return width,y_start,y_end,roi

def on_message(client, userdata, msg):
    global frame
    jpeg_data = base64.b64decode(msg.payload)
    np_array = np.frombuffer(jpeg_data, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)


def my_camera_mode():
    app = QApplication([])

    hsv_window = HSVControlWindow()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    lower_hsv, upper_hsv = load_profile()
    print(lower_hsv, upper_hsv)
    if lower_hsv is not None and upper_hsv is not None:
        hsv_window.lower_h_slider.setValue(lower_hsv[0])
        hsv_window.lower_s_slider.setValue(lower_hsv[1])
        hsv_window.lower_v_slider.setValue(lower_hsv[2])
        hsv_window.upper_h_slider.setValue(upper_hsv[0])
        hsv_window.upper_s_slider.setValue(upper_hsv[1])
        hsv_window.upper_v_slider.setValue(upper_hsv[2])

    while True:
        hsv_window.show()

        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        lower_hsv, upper_hsv = hsv_window.get_hsv_values()
        strip_thickness_factor = hsv_window.strip_width_slider.value()
        
        width, y_start, y_end, roi = get_calibartion_settings(frame, strip_thickness_factor)
        if DETECTION_MODE == "CIRCLE":
            detected_circles, mask = detect_circles(roi, lower_hsv, upper_hsv)
        if DETECTION_MODE == "SHAPE":
            detected_circles, mask = detect_any_shape(roi, lower_hsv, upper_hsv)
        if DETECTION_MODE == "ARUCO":
            detected_circles, ids = detect_aruco_markers(roi)
            if ids is not None:
                print(f"Detected ArUco markers: {ids}")
            mask = None
            

        for cx, cy, radius in detected_circles:
            cy += y_start
            cv2.circle(frame, (cx, cy), radius, (0, 255, 0), 2)
            print(f"Weed found at: ({cx}, {cy}), Radius: {radius}")
            message = send_mqtt_message(width, cx)
            print(f"Published MQTT message: {message}")

        cv2.rectangle(frame, (0, y_start), (width, y_end), (255, 0, 0), 2)

        hsv_window.update_image(cv2.flip(frame, 1), mask)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


    app.exit()

def my_camera_mode_stealth(lower_hsv, upper_hsv):
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        width, y_start, y_end, roi = get_calibartion_settings(frame, 10)
        if DETECTION_MODE == "CIRCLE":
            detected_circles, mask = detect_circles(roi, lower_hsv, upper_hsv)
        if DETECTION_MODE == "SHAPE":
            detected_circles, mask = detect_any_shape(roi, lower_hsv, upper_hsv)
        if DETECTION_MODE == "ARUCO":
            detected_circles, _ = detect_aruco_markers(roi)

        for cx, cy, radius in detected_circles:
            cy += y_start
            message = send_mqtt_message(width, cx)
            print(f"Published MQTT message: {message}")

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def mqtt_stream():
    global frame
    app = QApplication([])
    hsv_window = HSVControlWindow()

    while frame is None:
        pass
    
    lower_hsv, upper_hsv = load_profile()
    if lower_hsv is not None and upper_hsv is not None:
        hsv_window.lower_h_slider.setValue(lower_hsv[0])
        hsv_window.lower_s_slider.setValue(lower_hsv[1])
        hsv_window.lower_v_slider.setValue(lower_hsv[2])
        hsv_window.upper_h_slider.setValue(upper_hsv[0])
        hsv_window.upper_s_slider.setValue(upper_hsv[1])
        hsv_window.upper_v_slider.setValue(upper_hsv[2])

    while True:
        if frame is not None:
            height, width, _ = frame.shape

            hsv_window.show()

            lower_hsv, upper_hsv = hsv_window.get_hsv_values()
            strip_thickness_factor = hsv_window.strip_width_slider.value()
            
            width, y_start, y_end, roi = get_calibartion_settings(frame, strip_thickness_factor)
            if DETECTION_MODE == "CIRCLE":
                detected_circles, mask = detect_circles(roi, lower_hsv, upper_hsv)
            if DETECTION_MODE == "SHAPE":
                detected_circles, mask = detect_any_shape(roi, lower_hsv, upper_hsv)
            if DETECTION_MODE == "ARUCO":
                detected_circles, ids = detect_aruco_markers(roi)
                if ids is not None:
                    print(f"Detected ArUco markers: {ids}")
                mask = None
                

            for cx, cy, radius in detected_circles:
                cy += y_start
                cv2.circle(frame, (cx, cy), radius, (0, 255, 0), 2)
                print(f"Weed found at: ({cx}, {cy}), Radius: {radius}")
                message = send_mqtt_message(width, cx)
                print(f"Published MQTT message: {message}")

            cv2.rectangle(frame, (0, y_start), (width, y_end), (255, 0, 0), 2)

            hsv_window.update_image(cv2.flip(frame, 1), mask)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    app.exit()

def mqtt_stream_stealth(lower_hsv, upper_hsv):
    global frame
    
    while frame is None:
        pass

    while True:
        if frame is not None:
            height, width, _ = frame.shape

            strip_thickness_factor = 10
            
            width, y_start, y_end, roi = get_calibartion_settings(frame, strip_thickness_factor)
            if DETECTION_MODE == "CIRCLE":
                detected_circles, mask = detect_circles(roi, lower_hsv, upper_hsv)
            if DETECTION_MODE == "SHAPE":
                detected_circles, mask = detect_any_shape(roi, lower_hsv, upper_hsv)
            if DETECTION_MODE == "ARUCO":
                detected_circles, ids = detect_aruco_markers(roi)
                if ids is not None:
                    print(f"Detected ArUco markers: {ids}")
                mask = None
                

            for cx, cy, radius in detected_circles:
                cy += y_start
                message = send_mqtt_message(width, cx)
                print(f"Published MQTT message: {message}")


def send_mqtt_message(width, cx):
    angle = return_angle(cx, width)
    message = json.dumps({"command": "SERVO", "angle": angle})
    client.publish(TOPIC, message)
    return message




if __name__ == '__main__':
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC_VIDEO)
    client.loop_start()

    # my_camera_mode()
    # my_camera_mode_stealth(np.array([169, 83, 121]), np.array([180, 156, 241]))
    mqtt_stream()
    client.disconnect()
