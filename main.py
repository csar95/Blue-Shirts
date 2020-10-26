import cv2
import numpy as np
import os

from utils import *


def isBlueShirt(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # GENERATE MASK
    mask = cv2.inRange(imgHSV, lowerb=np.array(lowerb), upperb=np.array(upperb))

    # MASK PREPROCESSING
    maskBlur = cv2.GaussianBlur(mask, ksize=(7, 7), sigmaX=1)
    maskCanny = cv2.Canny(maskBlur, threshold1=150, threshold2=150)

    # GET BOUNDING BOX FOR THE COLOR
    return getBoundingBox(img, mask=maskCanny)

'''
This function detects blue areas on the input image. It sums all areas larger than 1000 and returns True when the sum is
over a predefined threshold  
'''
def getBoundingBox(img, mask):
    total_area = 0
    contours, hierarchy = cv2.findContours(mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 1000:
            total_area += area

            # Approximate how many corner points each contour has
            perimeter = cv2.arcLength(cnt, closed=True)
            approx = cv2.approxPolyDP(cnt, epsilon=0.02*perimeter, closed=True)
            x, y, width, height = cv2.boundingRect(approx)

            # Draw a rectangle around the detected area
            cv2.rectangle(img, pt1=(x, y), pt2=(x + width, y + height), color=(255, 0, 255), thickness=2)
            cv2.putText(img, str(area), org=(x, y + 20), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(255, 0, 0), thickness=1)

    return total_area > AREA_THRESHOLD


print_clr("Removing files from output folder if there's any...", MAGENTA)

for file in os.listdir(OUTPUT_PATH):
    os.remove(f"{OUTPUT_PATH}/{file}")

print_clr("Reading files from unlabeled shirts directory...", MAGENTA)

for idx, shirt in enumerate(os.listdir(UNLABELED_SHIRTS_PATH)):
    if any(ext in shirt for ext in FILE_EXTENSIONS):
        img = cv2.imread(f"{UNLABELED_SHIRTS_PATH}/{shirt}")
        imgResize = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

        if isBlueShirt(imgResize):
            cv2.imwrite(f"{OUTPUT_PATH}/{shirt}", imgResize)
            print(f"{len(os.listdir(OUTPUT_PATH))} / {idx +1}")
