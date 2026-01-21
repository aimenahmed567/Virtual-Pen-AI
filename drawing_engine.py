import cv2
import numpy as np

class DrawingEngine:
    def __init__(self, width, height):
        self.canvas = np.zeros((height, width, 3), dtype="uint8")
        self.prev = None

    def clear(self):
        self.canvas[:] = 0
        self.prev = None

    def draw(self, point, color=(255, 0, 255), thickness=5):
        if self.prev:
            cv2.line(self.canvas, self.prev, point, color, thickness)
        self.prev = point

    def erase(self, point, size=30):
        cv2.circle(self.canvas, point, size, (0, 0, 0), -1)
        self.prev = None

    def reset_prev(self):
        self.prev = None
