import cv2
import numpy as np

def detect_circles(image, lower_hsv, upper_hsv):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    blurred = cv2.GaussianBlur(mask, (9, 9), 2)

    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, 
                               param1=50, param2=30, minRadius=10, maxRadius=50)

    detected_circles = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            cx, cy, radius = circle
            detected_circles.append((cx, cy, radius))

    return detected_circles, mask

def detect_any_shape(image, lower_hsv, upper_hsv, min_area=100):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_shapes = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            # Get the center and size (similar to how we detect circles)
            moments = cv2.moments(contour)
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])
            else:
                cx, cy = 0, 0

            x, y, w, h = cv2.boundingRect(approx)
            detected_shapes.append((cx, cy, (w + h) // 2))

    return detected_shapes, mask
