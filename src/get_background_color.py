#encoding:UTF-8
#author:justry

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def move_average(l, n=10):
    ret = np.cumsum(l, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def get_background_color(img, n=10):
    bg_color = []
    for i in range(img.shape[-1]):
        axis = img[:, :, i]
        hist = np.histogram(axis, bins=256)
        ms = move_average(hist[0], n)
        color = np.where(ms==np.max(ms))[0][0]
        bg_color.append(color)
    return bg_color

def get_background(img, n=10):
    bg_color = get_background_color(img, n)
    bg = np.zeros(img.shape, dtype=np.uint8)
    bg[:, :] = bg_color
    return bg