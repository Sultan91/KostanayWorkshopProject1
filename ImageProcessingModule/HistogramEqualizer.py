import cv2
import numpy as np
from matplotlib import pyplot as plt


def color_correction(img):
    b, g, r = cv2.split(img)
    colors = [b, g, r]
    hist_b = np.histogram(b.flatten(), 256, [0, 256])
    hist_g = np.histogram(g.flatten(), 256, [0, 256])
    hist_r = np.histogram(r.flatten(), 256, [0, 256])
    hists = [hist_b, hist_g, hist_r]
    #plt.bar(range(len(hist_r[0])), hist_g[0])
    #plt.show()
    new_img = []
    for i in range(len(hists)):
        cumul_sum = np.cumsum(hists[i][0])
        #nm = (hists[i][0] - min(hists[i][0])) / (max(hists[i][0]) - min(hists[i][0])) * 255
        normalized = (cumul_sum - min(cumul_sum)) / (max(cumul_sum) - min(cumul_sum)) * 255
        normalized = normalized.astype('uint8')
        new_img.append(normalized[colors[i]])
        #new_img.append(nm[colors[i]])
    img_out = cv2.merge((new_img[0], new_img[1], new_img[2]))
    return img_out