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


def Negate(image):
    copy = image.copy()
    return cv2.bitwise_not(copy)


def GetSkeleton(img):
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)
    # Get a Cross Shaped Kernel
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    # Repeat steps 2-4
    while True:
        # Step 2: Open the image
        open = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
        # Step 3: Substract open from the original image
        temp = cv2.subtract(img, open)
        # Step 4: Erode the original image and refine the skeleton
        eroded = cv2.erode(img, element)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        # Step 5: If there are no white pixels left ie.. the image has been completely eroded, quit the loop
        if cv2.countNonZero(img) == 0:
            break

    return skel


def ConnectLines(bin_image):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
    img1 = cv2.morphologyEx(bin_image, cv2.MORPH_DILATE, kernel)

    contours1 = cv2.findContours(img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = contours1[0]
    cl = []

    for i in range(len(cnts)):
        min_dist = max(img1.shape[0], img1.shape[1])

        cl = []

        ci = cnts[i]
        ci_left = tuple(ci[ci[:, :, 0].argmin()][0])
        ci_right = tuple(ci[ci[:, :, 0].argmax()][0])
        ci_top = tuple(ci[ci[:, :, 1].argmin()][0])
        ci_bottom = tuple(ci[ci[:, :, 1].argmax()][0])
        ci_list = [ci_bottom, ci_left, ci_right, ci_top]

        for j in range(i + 1, len(cnts)):
            cj = cnts[j]
            cj_left = tuple(cj[cj[:, :, 0].argmin()][0])
            cj_right = tuple(cj[cj[:, :, 0].argmax()][0])
            cj_top = tuple(cj[cj[:, :, 1].argmin()][0])
            cj_bottom = tuple(cj[cj[:, :, 1].argmax()][0])
            cj_list = [cj_bottom, cj_left, cj_right, cj_top]

            for pt1 in ci_list:
                for pt2 in cj_list:
                    dist = int(
                        np.linalg.norm(np.array(pt1) - np.array(pt2)))  # dist = sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
                    if dist < min_dist:
                        min_dist = dist
                        cl = []
                        cl.append([pt1, pt2, min_dist])
        if len(cl) > 0:
            cv2.line(img1, cl[0][0], cl[0][1], (255, 255, 255), thickness=7)
    return img1
