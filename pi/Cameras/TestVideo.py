from Cameras.Camera import Camera
import cv2


class Video(Camera):
    def __init__(self, path):
        self.cam = cv2.VideoCapture(path)
        self.frameHeight = 1080
        self.frameWidth = 1920
        self.out = None

    def CaptureImage(self):
        res, image = self.cam.read()
        if res:
            self.frameHeight = image.shape[0]
            self.frameWidth = image.shape[1]
        return image

    def WriteVideoFrame(self, image):
        self.out.write(image)

    def InitVideoWriter(self, height, width):
        self.out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))
