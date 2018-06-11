#encoding:UTF-8
#author:justry

import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import functools
from PIL import Image, ImageDraw, ImageFont

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = "%s/fonts/" % CURRENT_DIR

def move_average(l, n=10):
    ret = np.cumsum(l, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def get_background_color(img, n=10):
    bg_color = []
    h, w = img.shape[:2]
    thresh = int(h*0.15)
    for i in range(img.shape[-1]):
        axis0 = img[:thresh, :, i]
        axis1 = img[-thresh:, :, i]
        axis = np.concatenate([axis0, axis1])
        hist = np.histogram(axis, bins=256)
        ms = move_average(hist[0], n)
        color = np.where(ms==np.max(ms))[0][0]+5
        bg_color.append(color)
    return bg_color

def get_background(img, n=10):
    bg_color = get_background_color(img, n)
    bg = np.zeros(img.shape, dtype=np.uint8)
    bg[:, :] = bg_color
    return bg

def put_chinese(img, result):
    # change the color
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    # pil image
    pil_im = Image.fromarray(img)
    #font = ImageFont.truetype(os.path.join(FONT_PATH, 'simhei.ttf'), 20, encoding='utf-8')
    font_size = functools.partial(
        ImageFont.truetype,
        font=os.path.join(FONT_PATH, 'simhei.ttf'),
        encoding='utf-8'
    )
    for i, j in result[0]:
        if i:
            #draw.text((int(j[0][0]), int(j[0][1])-20), i, (0, 0, 255), font=font_size(size=20))
            w, h, angle = get_wha(j)
            sub_img = get_transform_perspective(img, j)
            bg_color = get_background_color(sub_img)
            bg_color[-1] = 256
            #fill the background
            #write the txt
            txt = Image.new('RGBA', (w, h))
            draw = ImageDraw.Draw(txt)
            chr_size = get_character_size(i)
            size = int(min(h, w*2.0/chr_size))
            draw.rectangle(((0, 0), (w, h)), fill=tuple(bg_color))
            draw.text((0, 0), i, (0, 0, 0), font=font_size(size=size))
            w_ = txt.rotate(angle, expand=1)
            pil_im.paste(w_, (int(j[0][0]), int(j[1][1])), w_)
    img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGBA2BGR)
    return img

def get_wha(polys):
    polys = np.array(polys)
    angle = math.degrees(math.atan2(polys[0, 1]-polys[1, 1],
                                    polys[1, 0]-polys[0, 0]))
    return (int(np.sqrt(np.sum(np.square(polys[0] - polys[1])))),
            int(np.sqrt(np.sum(np.square(polys[1] - polys[2])))),
            angle)
    
def get_character_size(s):
    try:
        row_l=len(s)
        utf8_l=len(s.encode('utf-8'))
        return (utf8_l-row_l)/2+row_l
    except:
        return None
    return None

def get_transform_perspective(img, box):
    w = box[1][0] - box[0][0]
    h = box[3][1] - box[0][1]
    box = np.float32([(box[0][0], box[0][1]), (box[1][0], box[1][1]),
                      (box[3][0], box[3][1]), (box[2][0], box[2][1])])
    dst = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    size_x, size_y, channel = img.shape
    w, h = dst[3]
    M = cv2.getPerspectiveTransform(box, dst)  # rect  dst
    warped = cv2.warpPerspective(img, M, (w, h))
    return warped