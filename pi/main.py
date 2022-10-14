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
            resized = im.SquareCropToSymbol(trace, detector.WandPoints)
            spell = matcher.RecognizeSpell(resized)
            if spell is not None:
                cv2.imwrite("trace.jpg", trace)
                spell.Cast()


detector.Reset(cam.frameHeight, cam.frameWidth)
run()
