import pygame
import math
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QImage

class ControllerWidget(QWidget):
    drag_info_signal = pyqtSignal(float, float)

    def __init__(self, width=800, height=600, anchor_radius=20, drag_radius=10, max_drag_distance=200):
        super().__init__()
        self.setWindowTitle("Car Controller with PyQt6")
        self.setGeometry(100, 100, width, height)

        # Initialize pygame
        pygame.init()

        # Screen settings
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.Surface((self.WIDTH, self.HEIGHT))

        # Default colors (can be customized later)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        # Anchor settings
        self.anchor_pos = (self.WIDTH // 2, self.HEIGHT // 2)
        self.drag_pos = self.anchor_pos
        self.direction_vector = (0, 0)
        self.dragging = False
        self.max_drag_distance = max_drag_distance
        self.anchor_radius = anchor_radius
        self.drag_radius = drag_radius
        self.drag_line_radius = 3

        # Set up timer to update screen regularly
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(16)  # roughly 60 FPS

    def set_anchor_color(self, color):
        """Set the color of the anchor point"""
        self.RED = color

    def set_drag_color(self, color):
        """Set the color of the drag line and drag circle"""
        self.BLUE = color

    def set_max_drag_circle_color(self, color):
        """Set the color of the max drag circle"""
        self.BLUE = color
    
    def set_background_color(self, color):
        """Set the background color of the controller widget"""
        self.WHITE = color
    
    def set_outer_anchor_radius(self, thickness):
        """Set the thickness of the drag line"""
        self.drag_radius = thickness
    
    def set_center_anchor_radius(self, radius):
        """Set the radius of the center anchor point"""
        self.anchor_radius = radius

    def set_drag_line_thickness(self, thickness):
        """Set the thickness of the drag line"""
        self.drag_line_radius = thickness

    def calculate_drag_properties(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        distance = min(distance, self.max_drag_distance)
        angle = math.atan2(-dy, dx)
        normalized_dx = dx / (distance if distance != 0 else 1)
        normalized_dy = dy / (distance if distance != 0 else 1)
        return distance, math.degrees(angle), (normalized_dx, normalized_dy)

    def mousePressEvent(self, event):
        if math.dist(self.anchor_pos, (event.position().x(), event.position().y())) < self.anchor_radius:
            self.dragging = True

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.drag_info_signal.emit(0, 0)

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.drag_pos = (event.position().x(), event.position().y())
            drag_length, drag_angle, self.direction_vector = self.calculate_drag_properties(self.anchor_pos, self.drag_pos)
            self.drag_info_signal.emit(drag_length, drag_angle)

    def update_screen(self):
        self.screen.fill(self.WHITE)
        pygame.draw.circle(self.screen, self.RED, self.anchor_pos, self.anchor_radius)
        
        # Draw the max drag distance circle
        pygame.draw.circle(self.screen, self.BLUE, self.anchor_pos, self.max_drag_distance, 3)
        
        if self.dragging:
            pygame.draw.line(self.screen, self.BLUE, self.anchor_pos, self.drag_pos, self.drag_line_radius)
            pygame.draw.circle(self.screen, self.BLUE, self.drag_pos, self.drag_radius)
            
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        raw_data = pygame.image.tostring(self.screen, 'RGBA')
        qimage = QImage(raw_data, self.WIDTH, self.HEIGHT, QImage.Format.Format_RGBA8888)
        painter.drawImage(0, 0, qimage)
