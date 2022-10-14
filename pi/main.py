from Cameras.TestVideo import *
from WandDetector import *
from SpellMatch import *
import ImageProcessor as im


cam = Camera()
detector = WandDetector()
matcher = SpellMatch()


def run():
    while True:
        image = cam.CaptureImage()
        if image is None:
            # Something went wrong
            break
        image = im.Preprocess(image)
        trace = detector.TraceWand(image)
        if len(detector.WandPoints) > 15:
            # TODO: check if trace is recognized spell
            pass


test_image = cam.CaptureImage()
detector.Reset(cam.frameHeight, cam.frameWidth)
run()
