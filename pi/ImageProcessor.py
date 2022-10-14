import cv2
import numpy as np


def Preprocess(image):
    copy = image.copy()
    copy = cv2.GaussianBlur(copy, (5, 5), 0)
    copy = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(copy)
    ret, mask = cv2.threshold(copy, maxVal * 0.9, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations=1)
    return dilation


def SquareCropToSymbol(image, keypoints):
    copy = image.copy()

    # find extreme keypoints
    minX = int(min(keypoints, key=lambda kp: kp.pt[0]).pt[0])
    maxX = int(max(keypoints, key=lambda kp: kp.pt[0]).pt[0])
    minY = int(min(keypoints, key=lambda kp: kp.pt[1]).pt[1])
    maxY = int(max(keypoints, key=lambda kp: kp.pt[1]).pt[1])

    # crop symbol
    resized = copy[minY:maxY, minX:maxX]

    # find side length of square image
    height = maxY - minY
    width = maxX - minX
    side = max(height, width) + 50
    yoff = int(abs(height - side) / 2)
    xoff = int(abs(width - side) / 2)

    squareSymbol = np.zeros((side, side), np.uint8)
    squareSymbol[yoff:yoff + height, xoff:xoff + width] = resized
    return squareSymbol
