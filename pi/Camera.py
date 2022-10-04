import cv2

FRAME_HEIGHT = 1080
FRAME_WIDTH = 1920

class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    def CaptureImage(self):
        res, image = self.cam.read()
        return image
