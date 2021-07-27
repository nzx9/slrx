import cv2
import numpy as np


class WebCam:
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def capture(self):
        success, image = self.video.read()

        fliped = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode(".jpg", fliped)
        return jpeg.tobytes()
