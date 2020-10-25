import cv2
import numpy as np

from utils import *


def findBlueShirtInImage(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # GENERATE MASK
    mask = cv2.inRange(imgHSV, lowerb=np.array(lowerb), upperb=np.array(upperb))
    # cv2.imshow(k, mask)

    # MASK PREPROCESSING
    maskBlur = cv2.GaussianBlur(mask, ksize=(7, 7), sigmaX=1)
    maskCanny = cv2.Canny(maskBlur, threshold1=150, threshold2=150)

    # GET BOUNDING BOX FOR THE COLOR
    x, y, width, height = getBoundingBox(mask=maskCanny)

    # DRAW A RECTANGLE AROUND THE RETURNED POINT
    if x > 0 and y > 0:
        cv2.rectangle(img, pt1=(x, y), pt2=(x + width, y + height), color=(255, 0, 255), thickness=2)

'''
If found, returns the parameters of a bounding box surrounding the corners points corresponding to the color area
'''
def getBoundingBox(mask):
    contours, hierarchy = cv2.findContours(mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > AREA_THRESHOLD:
            # Approximate how many corner points each contour has
            perimeter = cv2.arcLength(cnt, closed=True)
            approx = cv2.approxPolyDP(cnt, epsilon=0.02*perimeter, closed=True)

            return cv2.boundingRect(approx)

    return 0, 0, 0, 0

# READ IMAGE
img = cv2.imread(f"{BLUE_SHIRTS_PATH}/9.jpeg")
img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

findBlueShirtInImage(img)

cv2.imshow(winname="Image", mat=img)
cv2.waitKey(0)  # 0 --> Infinite delay
