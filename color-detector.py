import cv2
import numpy as np
import os

from utils import *


def empty(arg):
    pass

# CREATE TRACKBAR WINDOW
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv2.createTrackbar("Saturation Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Saturation Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Value Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Value Max", "TrackBars", 255, 255, empty)

# H - (95, 118) | S - (152, 255) | V - (0, 255)

for shirt in os.listdir(BLUE_SHIRTS_PATH):
    print(shirt)

while True:
    #################### READ IMAGES

    shirts, shirts_HSV = np.array([]), np.array([])
    for shirt in os.listdir(BLUE_SHIRTS_PATH):
        if any(ext in shirt for ext in ["jpg", "jpeg", "png"]):
            shirt_img = cv2.imread(f"{BLUE_SHIRTS_PATH}/{shirt}")
            shirt_img = cv2.resize(shirt_img, (IMG_WIDTH, IMG_HEIGHT))
            shirts = np.expand_dims(shirt_img, axis=0) if shirts.size == 0 else np.append(shirts, np.expand_dims(shirt_img, axis=0), axis=0)

            shirt_img_HSV = cv2.cvtColor(shirt_img, cv2.COLOR_BGR2HSV)
            shirts_HSV = np.expand_dims(shirt_img_HSV, axis=0) if shirts_HSV.size == 0 else np.append(shirts_HSV, np.expand_dims(shirt_img_HSV, axis=0), axis=0)

    if shirts.shape[0] % IMGS_PER_ROW != 0:
        for i in range(IMGS_PER_ROW - (shirts.shape[0] % IMGS_PER_ROW)):
            shirts = np.append(shirts, np.expand_dims(np.zeros(shape=shirts[0].shape), axis=0), axis=0)
            shirts_HSV = np.append(shirts_HSV, np.expand_dims(np.zeros(shape=shirts_HSV[0].shape), axis=0), axis=0)

    #################### STACK IMAGES

    all_shirts_img, all_shirts_img_HSV = np.array([]), np.array([])

    for idx in range(0, shirts.shape[0], IMGS_PER_ROW):
        rlim = idx + IMGS_PER_ROW if idx + IMGS_PER_ROW < shirts.shape[0] else shirts.shape[0]
        new_row = np.hstack(shirts[idx:rlim])
        new_row_HSV = np.hstack(shirts_HSV[idx:rlim])

        if all_shirts_img.size == 0:
            all_shirts_img = new_row
            all_shirts_img_HSV = new_row_HSV
        else:
            all_shirts_img = np.vstack((all_shirts_img, new_row))
            all_shirts_img_HSV = np.vstack((all_shirts_img_HSV, new_row_HSV))

    #################### GEET MIN/MAX VALUES FROM THE TRACKBAR WINDOW

    # With these ranges of the Hue, Saturation and Value we can use these values to filter out the image so that we get the blue color in that range
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Saturation Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Saturation Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Value Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Value Max", "TrackBars")

    #################### CREATE MASK

    mask = cv2.inRange(all_shirts_img_HSV, lowerb=np.array([h_min, s_min, v_min]), upperb=np.array([h_max, s_max, v_max]))

    # Get the original color from the original imgs. that corresponds to the mask white region
    imgResult = cv2.bitwise_and(all_shirts_img, all_shirts_img, mask=mask)

    #################### SHOW IMAGES

    # cv2.imshow("Blue shirts (Original)", all_shirts_img)
    # cv2.imshow("Blue shirts (HSV)", all_shirts_img_HSV)
    cv2.imshow("Mask", mask)
    cv2.imshow("Filtered blue shirts", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to stop the video
        break
