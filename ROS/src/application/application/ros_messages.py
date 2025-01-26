import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
import threading


# Define all the topics
ROBOT_CONTROL_TOPIC = "/robot/control"
ROBOT_STATUS_TOPIC = "/robot/status"
ROBOT_VELOCITY_TOPIC = "/robot/velocity"
ROBOT_AUTO_MODE_TOPIC = "/robot/auto_mode"
ROBOT_STEERING_ANGLE_TOPIC = "/robot/steering_angle"
VIDEO_STREAM_TOPIC = "/video/stream"
CONTROLLER_JOYSTICK_INPUT_TOPIC = "/controller/joystick_input"

spin_thread = None

class RobotControlNode(Node):


    def __init__(self):
        super().__init__("robot_control_node")

        # Create callback functions for the topics
        self.callback_robot_control = None
        self.callback_robot_velocity = None
        self.callback_robot_auto_mode = None
        self.callback_robot_steering_angle = None
        self.callback_video_stream = None

        # Create publishers for the topics
        self.control_pub = self.create_publisher(String, ROBOT_CONTROL_TOPIC, 10)
        self.status_pub = self.create_publisher(String, ROBOT_STATUS_TOPIC, 10)
        self.velocity_pub = self.create_publisher(Float32, ROBOT_VELOCITY_TOPIC, 10)
        self.auto_mode_pub = self.create_publisher(Bool, ROBOT_AUTO_MODE_TOPIC, 10)
        self.steering_angle_pub = self.create_publisher(Float32, ROBOT_STEERING_ANGLE_TOPIC, 10)
        self.joystick_input_pub = self.create_publisher(String, CONTROLLER_JOYSTICK_INPUT_TOPIC, 10)

        # Create subscriber for video stream
        self.create_subscription(CompressedImage, VIDEO_STREAM_TOPIC, self.video_stream_callback, 10)

        # Create subscribers for other topics
        self.create_subscription(String, ROBOT_CONTROL_TOPIC, self.control_callback, 10)
        self.create_subscription(Float32, ROBOT_VELOCITY_TOPIC, self.velocity_callback, 10)
        self.create_subscription(Bool, ROBOT_AUTO_MODE_TOPIC, self.auto_mode_callback, 10)
        self.create_subscription(Float32, ROBOT_STEERING_ANGLE_TOPIC, self.steering_angle_callback, 10)

        # Publish initial robot status
        self.publish_robot_status("Initializing...")

    def set_callback_robot_control(self, callback):
        self.callback_robot_control = callback
    
    def set_callback_robot_velocity(self, callback):
        self.callback_robot_velocity = callback

    def set_callback_robot_auto_mode(self, callback):
        self.callback_robot_auto_mode = callback

    def set_callback_robot_steering_angle(self, callback):
        self.callback_robot_steering_angle = callback

    def set_callback_video_stream(self, callback):
        self.callback_video_stream = callback

        
    def control_callback(self, msg: String):

        if self.callback_robot_control is not None:
            self.callback_robot_control(msg.data)
        else:
            self.get_logger().info(f"Received control command: {msg.data}")

    def velocity_callback(self, msg: Float32):

        if self.callback_robot_velocity is not None:
            self.callback_robot_velocity(msg.data)
        else:
            self.get_logger().info(f"Received velocity update: {msg.data}")

    def auto_mode_callback(self, msg: Bool):

        if self.callback_robot_auto_mode is not None:
            self.callback_robot_auto_mode(msg.data)
        else:
            if msg.data:
                self.get_logger().info("Auto mode enabled")
            else:
                self.get_logger().info("Auto mode disabled")
        
    def steering_angle_callback(self, msg: Float32):

        if self.callback_robot_steering_angle is not None:
            self.callback_robot_steering_angle(msg.data)
        else:
            self.get_logger().info(f"Received steering angle: {msg.data}")

    def video_stream_callback(self, msg: CompressedImage):
        # Process the video frame (e.g., display, save, etc.)
        if self.callback_video_stream is not None:
            self.callback_video_stream(msg)
        else:
            self.get_logger().info("Received video frame")
    
    def publish_control_command(self, control_command):
        msg = String()
        msg.data = control_command
        self.control_pub.publish(msg)
        self.get_logger().info(f"Published control command: {msg.data}")

    def publish_robot_status(self, status_message):
        msg = String()
        msg.data = status_message
        self.status_pub.publish(msg)
        self.get_logger().info(f"Published robot status: {msg.data}")

    def publish_velocity(self, velocity_value):
        msg = Float32()
        msg.data = velocity_value
        self.velocity_pub.publish(msg)
        self.get_logger().info(f"Published velocity: {msg.data}")

    def publish_auto_mode(self, is_auto_mode):
        msg = Bool()
        msg.data = is_auto_mode
        self.auto_mode_pub.publish(msg)
        self.get_logger().info(f"Published auto mode status: {msg.data}")

    def publish_steering_angle(self, steering_angle):
        msg = Float32()
        msg.data = steering_angle
        self.steering_angle_pub.publish(msg)
        self.get_logger().info(f"Published steering angle: {msg.data}")

    def publish_joystick_input(self, joystick_data):
        msg = String()
        msg.data = joystick_data
        self.joystick_input_pub.publish(msg)
        self.get_logger().info(f"Published joystick input: {msg.data}")


def create_robot_control_node(spin=True):
    global spin_thread

    rclpy.init()

    robot_control_node = RobotControlNode()


    if spin:
        spin_thread = threading.Thread(target=rclpy.spin, args=(robot_control_node,))
        spin_thread.start()

    return robot_control_node


def destroy_robot_control_node(node):
    global spin_thread
    node.destroy_node()

    rclpy.shutdown()
    if spin_thread is not None:
        spin_thread.join()
        
    
