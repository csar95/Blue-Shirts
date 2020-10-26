import cv2
import numpy as np
import os

from utils import *


#################### READ IMAGES
shirts, shirts_HSV = np.array([]), np.array([])
for shirt in os.listdir(BLUE_SHIRTS_PATH):
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

cv2.imshow("Blue shirts", all_shirts_img)
cv2.imshow("Blue shirts HSV", all_shirts_img_HSV)
cv2.waitKey(0)
