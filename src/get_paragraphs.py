#encoding:UTF-8
#author:justry

import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import functools
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
from scipy.ndimage.interpolation import rotate

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = "%s/fonts/" % CURRENT_DIR

class Line(object):
    def __init__(self, label, coord):
        self.label = label
        self.coord = np.array(coord)
        self.w, self.h = self.get_wh(coord)
        self.end_flag = False
        self.hash_ = hash(self.coord.tostring())
        
    def get_wh(self, coord):
        box = minimum_bounding_rectangle(np.array(coord))
        p0p1 = np.sqrt(np.sum(np.square(box[0] - box[1])))
        p2p1 = np.sqrt(np.sum(np.square(box[2] - box[1])))
        return (p0p1, p2p1) if p0p1 > p2p1 else (p2p1, p0p1)
    
    def distance(self, other):
        return np.sqrt(np.sum(np.square(self.coord[-1] - other.coord[0])))
    
    def coparagraph(self, other, h_factor=0.15, w_factor=2, dis_factor=2.5):
        if self.end_flag:
            return False
        h_ = self.h / other.h
        w_ = self.w - other.w
        start = self.coord[-1, 0] - other.coord[0, 0]
        end_ = self.coord[2, 0] - other.coord[1, 0]
        if '.' == self.label[-1] or '。' == self.label[-1]:
            return False
        if h_ > 1+h_factor or h_ < 1-h_factor:
            return False
        if end_ < -w_factor * self.h:
            return False
        if w_ > w_factor * self.h:
            other.end_flag = True
        dis = self.distance(other)
        if dis > dis_factor * self.h:
            return False
        return True
    
    def find_nearest(self, others):
        ret = others[0]
        nearest = 1e9
        for other in others: 
            dis = self.distance(other)
            if nearest > dis:
                nearest = dis
                ret = other
        return ret

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

def get_rectangle_from_boxes(boxes):
    points = np.reshape(np.array(boxes), (-1, 2))
    return minimum_bounding_rectangle(points)


def minimum_bounding_rectangle(points):
    """
    Find the smallest bounding rectangle for a set of points.
    Returns a set of points representing the corners of the bounding box.

    :param points: an nx2 matrix of coordinates
    :rval: an nx2 matrix of coordinates
    """
    pi2 = np.pi/2.

    # get the convex hull for the points
    hull_points = points[ConvexHull(points).vertices]

    # calculate edge angles
    edges = np.zeros((len(hull_points)-1, 2))
    edges = hull_points[1:] - hull_points[:-1]

    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])

    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    # find rotation matrices
    # XXX both work
    rotations = np.vstack([
        np.cos(angles),
        np.cos(angles-pi2),
        np.cos(angles+pi2),
        np.cos(angles)]).T
    rotations = rotations.reshape((-1, 2, 2))

    # apply rotations to the hull
    rot_points = np.dot(rotations, hull_points.T)

    # find the bounding points
    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    # find the box with the best area
    areas = (max_x - min_x) * (max_y - min_y)
    best_idx = np.argmin(areas)

    # return the best box
    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((4, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)
    
    adds = np.apply_along_axis(lambda x:np.sum(x), -1, rval)
    index = np.where(adds==np.min(adds))[0][0]
    rval = np.concatenate([rval, rval])
    rval = rval[index:index+4]
    
    ret = rval
    if rval[1, 0] < rval[3, 0]:
        ret = np.zeros_like(rval)
        ret[0] = rval[0]
        ret[1] = rval[3]
        ret[2] = rval[2]
        ret[3] = rval[1]
    ret[ret<0] = 0
    
    return ret

def sorted_result(result):
    y = [i[-1][0][-1] for i in result]
    ret = sorted(zip(result, y), key=lambda x:x[-1])
    return [i[0] for i in ret]

def get_paragraphs(result):
    result = sorted_result(result)
    result = [Line(*i) for i in result]
    paras = []
    lines = []
    while len(result):
        end_flag = False
        current_line = result.pop(0)
        lines.append(current_line)
        while not end_flag:
            if len(result) == 0:
                end_flag = True
                paras.append(lines)
                lines = []
                break
            nearest_line = current_line.find_nearest(result)
            if current_line.coparagraph(nearest_line):
                lines.append(nearest_line)
                result.remove(nearest_line)
                current_line = nearest_line
            else:
                end_flag = True
                paras.append(lines)
                lines = []
    return paras

def put_chinese(img, result, translate=False):
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
    h_raw, w_raw = img.shape[:2]
    for i, j in result[0]:
        if i:
            j = np.clip(j, [0, 0], [w_raw, h_raw])
            chr_size_zh = get_character_size(i)
            if translate:
                i = get_trans(i)
            #i = get_trans(i)
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
            if chr_size*1.0/chr_size_zh < 2 or chr_size_zh <= 2:
                size = int(min(h, w*1.9/chr_size))
                draw.rectangle(((0, 0), (w, h)), fill=tuple(bg_color))
                draw.text((0, 0), i, (0, 0, 0), font=font_size(size=size))
            else:
                size = int(min(h/2.0, w*3.8/chr_size))
                draw.rectangle(((0, 0), (w, h)), fill=tuple(bg_color))
                s = i.split(' ')
                mid = len(s)//2
                draw.text((0, 0), ' '.join(s[:mid]), (0, 0, 0), font=font_size(size=size))
                draw.text((0, size), ' '.join(s[mid:]), (0, 0, 0), font=font_size(size=size))
            w_ = txt.rotate(angle, expand=1)
            pil_im.paste(w_, (int(j[0][0]), int(j[1][1])), w_)
    img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGBA2BGR)
    return img

def put_para_chinese(img, result, translate=False, is_ch=True):
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
    for para in result:
        max_char_length = max([get_character_size(i[0]) for i in para])
        boxes = [i[1] for i in para]
        line_ws = []
        line_hs = []
        line_angles = []
        for i in para:
            line_w, line_h, line_angle = get_wha(i[1])
            line_ws.append(line_w)
            line_hs.append(line_h)
            line_angles.append(line_angle)
        para_box = get_rectangle_from_boxes(boxes)
        para_w, para_h, para_angle = get_wha(para_box)
        size = int(min(np.mean(line_hs), para_w*1.9/max_char_length))
        if translate:
            if is_ch:
                strings = ''.join([i[0] for i in para])
            else:
                strings = ' '.join([i[0] for i in para])
            strings = get_trans(strings)
            if is_ch:
                strings = strings.replace(" ' ", "'").replace(" ,", ",")
                strings = divide_sentence(strings, 2*int(para_w/size), not is_ch)
            else:
                strings = divide_sentence(strings, int(para_w/size), not is_ch)
        else:
            strings = [i[0] for i in para]
        if is_ch and translate:
            step = int(0.9*para_h / len(strings))
        else:
            step = int(para_h / len(strings))
        para_txt = Image.new('RGBA', (para_w, para_h))
        para_draw = ImageDraw.Draw(para_txt)
        sub_img = get_transform_perspective(img, para_box)
        bg_color = get_background_color(sub_img)
        bg_color[-1] = 256
        para_draw.rectangle(((0, 0), (para_w, para_h)), fill=tuple(bg_color))
        cnt = 0
        for i in strings:
            para_draw.text((0, cnt*step), i, (0, 0, 0), font=font_size(size=size))
            cnt += 1
        w_ = para_txt.rotate(para_angle, expand=1)
        pil_im.paste(w_, (int(para_box[0][0]), int(para_box[1][1])), w_)
    img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGBA2BGR)
    return img

def divide_sentence(s, line_cnt, is_ch=True):
    ret = []
    if is_ch:
        length = get_character_size(s)
        #line_l = length//line_cnt
        line_content = ''
        line_length = 0
        for i in s:
            line_content += i
            line_length = get_character_size(line_content)
            if line_length >= line_cnt:
                ret.append(line_content)
                line_content = ''
                line_length = 0
        if line_content:
            ret.append(line_content)
    else:
        length = get_character_size(s)
        #line_l = length//line_cnt
        line_content = []
        line_length = 0
        for i in s.split(' '):
            line_content.append(i)
            line_length = get_character_size(' '.join(line_content))
            if line_length >= line_cnt:
                ret.append(' '.join(line_content))
                line_content = []
                line_length = 0
        if len(line_content):
            ret.append(' '.join(line_content))
    return ret