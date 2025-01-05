import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json

def detect_aruco_markers(image, marker_type=cv2.aruco.DICT_6X6_250):

    # Initialize the ArUco detector
    aruco_dict = cv2.aruco.getPredefinedDictionary(marker_type)
    parameters = cv2.aruco.DetectorParameters()
    
    # Detect ArUco markers
    corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)
    
    detected_circles = []

    if ids is not None:
        for i, corner in enumerate(corners):
            # Get the centroid of the marker
            cx = int(np.mean(corner[0][:, 0]))
            cy = int(np.mean(corner[0][:, 1]))

            detected_circles.append((cx, cy, 2))
    
    return detected_circles, ids