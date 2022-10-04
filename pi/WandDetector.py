import cv2
import numpy as np


class WandDetector:
    def __init__(self):
        self.blobParams = cv2.SimpleBlobDetector_Params()
        self.InitBlobParams()
        self.blobDetector = cv2.SimpleBlobDetector_create(self.blobParams)
        self.TracingFrame = None
        self.WandPoints = []

    def InitBlobParams(self):
        self.blobParams.minThreshold = 150
        self.blobParams.maxThreshold = 255
        self.blobParams.filterByColor = 1
        self.blobParams.blobColor = 255
        self.blobParams.filterByArea = 1
        self.blobParams.minArea = 0.05
        self.blobParams.maxArea = 20
        self.blobParams.filterByCircularity = 0
        self.blobParams.minCircularity = 0.5
        self.blobParams.filterByConvexity = 1
        self.blobParams.minConvexity = 0.5
        self.blobParams.filterByInertia = 0

    def Reset(self, height, width):
        self.TracingFrame = np.zeros((height, width, 3), np.uint8)
        self.WandPoints = []

    def DetectWand(self, image):
        return self.blobDetector.detect(image)

    def TraceWand(self, image):
        keypoints = self.DetectWand(image)
        print(len(keypoints))

        if len(keypoints) > 0:
            keypoint = keypoints[0]
            if len(self.WandPoints) > 0:
                prev = self.WandPoints.pop(len(self.WandPoints) - 1)
                x1 = int(prev.pt[0])
                y1 = int(prev.pt[1])
                x2 = int(keypoint.pt[0])
                y2 = int(keypoint.pt[1])
                cv2.line(self.TracingFrame, (x1, y1), (x2, y2), [255, 255, 255], 2)
            self.WandPoints.append(keypoint)
        else:
            return None

        return self.TracingFrame
