import cv2
import numpy as np
import time


class WandDetector:
    def __init__(self):
        self.blobParams = cv2.SimpleBlobDetector_Params()
        self.InitBlobParams()
        self.blobDetector = cv2.SimpleBlobDetector_create(self.blobParams)
        self.TracingFrame = None
        self.WandPoints = []
        self.time = None
        self.backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(400, detectShadows=False)

    def InitBlobParams(self):
        self.blobParams.minThreshold = 150
        self.blobParams.maxThreshold = 255
        self.blobParams.filterByColor = 1
        self.blobParams.blobColor = 255
        self.blobParams.filterByArea = 1
        self.blobParams.minArea = 5
        self.blobParams.maxArea = 10000
        self.blobParams.filterByCircularity = 0
        self.blobParams.filterByConvexity = 0
        self.blobParams.filterByInertia = 0

    def Reset(self, height, width):
        self.TracingFrame = np.zeros((height, width), np.uint8)
        self.WandPoints = []
        self.time = None

    def RemoveBackground(self, image):
        return self.backgroundSubtractor.apply(image)

    def DetectWand(self, image):
        return self.blobDetector.detect(image)

    def TraceWand(self, image):
        mask = self.RemoveBackground(image)
        blobs = self.DetectWand(mask)
        wandDetected = len(blobs) > 0
        if wandDetected:
            if self.time is None:
                self.time = time.time()
            elif time.time() - self.time > 3:
                cv2.imwrite("trace.jpg", self.TracingFrame)
                self.Reset(self.TracingFrame.shape[0], self.TracingFrame.shape[1])
                return self.TracingFrame
            # self.TracingFrame += mask
            if len(self.WandPoints) > 0:
                prev = self.WandPoints[len(self.WandPoints) - 1]
                curr = blobs[0]
                cv2.line(self.TracingFrame, (int(prev.pt[0]), int(prev.pt[1])), (int(curr.pt[0]), int(curr.pt[1])),
                         (255, 255, 255), 4)
            self.WandPoints.append(blobs[0])
        return self.TracingFrame
