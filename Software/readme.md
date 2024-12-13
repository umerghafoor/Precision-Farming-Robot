# Video Streaming over MQTT

This software enables live video streaming using MQTT for communication between a publisher and a subscriber.

## Features

- **Publisher** (`pub.py`): Captures video from a camera, encodes it, and publishes it to an MQTT topic.
- **Subscriber** (`sub.py`): Receives the video stream via MQTT, decodes it, and displays the video.
- **Red Dot Detection** (`detect_red_dots_in_line.py`): Detects red dots in a horizontal strip of the video frame and publishes the angle to an MQTT topic.

## Dependencies

- Python 3.x
- OpenCV
- Paho MQTT
- NumPy

## Installation

1. Install dependencies:

   ```bash
   pip install opencv-python paho-mqtt numpy
   ```

2. Ensure your MQTT broker is running and accessible.

## Usage

### Publisher

1. Run the publisher script to stream the video:

   ```bash
   python pub.py
   ```

2. Press `q` to stop streaming.

### Subscriber

1. Run the subscriber script to receive and display the video:

   ```bash
   python sub.py
   ```

2. Press `q` to stop the video stream.

### Red Dot Detection

1. Run the red dot detection script to detect red dots and publish the angle:

   ```bash
   python detect_red_dots_in_line.py
   ```

2. Press `q` to stop the detection.
