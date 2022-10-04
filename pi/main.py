from Camera import *
from WandDetector import *

cam = Camera()
detector = WandDetector()
numFrames = 0
detector.Reset(FRAME_HEIGHT, FRAME_WIDTH)


while True:
    image = cam.CaptureImage()
    trace = detector.TraceWand(image)
    if trace is not None:
        # TODO: check if image is a recognized spell
        # Collect frames and save result for now
        numFrames += 1
        if numFrames >= 100:
            cv2.imwrite("trace.jpg", trace)
            numFrames = 0
            detector.Reset(FRAME_HEIGHT, FRAME_WIDTH)
