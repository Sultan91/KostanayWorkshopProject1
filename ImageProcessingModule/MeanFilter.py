import cv2
import numpy as np


def mean_filter(img_gray, step=10):
    height = img_gray.shape[0]
    width = img_gray.shape[1]
    smoothed_img = np.ndarray(shape=(height, width, 1))
    for i in range(0, height, 1):
        for j in range(0, width, 1):
            temp = sum(img_gray[i:i+step, j:j+step].flatten()) / step**2
            smoothed_img[i:i+step, j:j+step] = temp
    return smoothed_img
