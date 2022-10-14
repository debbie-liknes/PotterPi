import cv2


class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.frameHeight = 1080
        self.frameWidth = 1920
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.frameWidth)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frameHeight)

    def CaptureImage(self):
        res, image = self.cam.read()
        return image
