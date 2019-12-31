import numpy as np

# Color order in opnecv: BGR


def genGrayScale(image):
    height, width, depth = np.shape(image)
    grey_img = np.ndarray(shape=(height, width, 1))
    for py in range(0, height):
        for px in range(0, width):
            tot_brightness = 0.2989 * image[py][px][2] + 0.5870*image[py][px][1] + 0.1140*image[py][px][0]
            #tot_brightness = (image[py][px][0] + image[py][px][1] + image[py][px][2])/3
            grey_img[py][px][0] = tot_brightness
    return grey_img
