#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import codecs
import sys
import numpy as np
from shapely.geometry import Polygon

FILE_EXT = '.txt'
ENCODE_METHOD = 'utf-8'


def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def get_area(poly):
    points = np.array(poly)
    x = points[:, 0]
    y = points[:, 1]
    return PolyArea(x, y)

def PolygonSorted(regions):
    boxes = [[i['upperleft'], i['upperright'], i['lowerright'], i['lowerleft']] for i in regions]
    areas = [get_area(i) for i in boxes]
    ret = sorted(zip(regions,areas), key=lambda x:x[-1])
    return [i[0] for i in ret]

def boxIsInBox(a, b, thresh=0.7):
    a_area = get_area(a)
    intersect_area = Polygon(a).intersection(Polygon(b)).area
    return intersect_area / a_area >= thresh

def getParaBox(target, regions):
    target_box = [target['upperleft'], 
                  target['upperright'],
                  target['lowerright'],
                  target['lowerleft']]
    ret = None
    for i in regions:
        if ret is not None:
            break
        else:
            box = [i['upperleft'], 
                   i['upperright'],
                   i['lowerright'],
                   i['lowerleft']]
            if boxIsInBox(target_box, box):
                ret = i
    return ret or target

class EastWriter:

    def __init__(self, foldername, filename, imgSize,databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.regionlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def addRegion(self, upperleft, upperright, lowerright, lowerleft, name, difficult):
        region = {'upperleft': upperleft, 'upperright': upperright, 'lowerright': lowerright, 'lowerleft': lowerleft}
        region['name'] = name
        region['difficult'] = difficult
        self.regionlist.append(region)

    def save(self, targetFile=None):
        out_file = None
        if targetFile is None:
            out_file = open(self.filename + FILE_EXT, 'w', encoding='utf-8')
        else:
            if not targetFile.endswith(".txt"):
                targetFile = targetFile + ".txt"
            out_file = open(targetFile, 'w', encoding='utf-8')
        self.regionlist = PolygonSorted(self.regionlist)
        paraboxs = []
        for i in range(len(self.regionlist)):
            region = self.regionlist[i]
            if region in paraboxs:
                continue
            else:
                parabox = getParaBox(region, self.regionlist[i:][::-1])
                paraboxs.append(parabox)
                out_file.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16}\n".format
                               (int(region["upperleft"][0]), int(region["upperleft"][1]),
                                int(region["upperright"][0]), int(region["upperright"][1]),
                                int(region["lowerright"][0]), int(region["lowerright"][1]),
                                int(region["lowerleft"][0]), int(region["lowerleft"][1]),
                                int(parabox["upperleft"][0]), int(parabox["upperleft"][1]),
                                int(parabox["upperright"][0]), int(parabox["upperright"][1]),
                                int(parabox["lowerright"][0]), int(parabox["lowerright"][1]),
                                int(parabox["lowerleft"][0]), int(parabox["lowerleft"][1]),
                                region['name']))
        out_file.close()


class EastReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath
        self.verified = False
        try:
            self.parse()
        except:
            pass

    def getShapes(self):
        return self.shapes

    def parse(self):
        assert self.filepath.endswith(FILE_EXT), "Unsupport file format"

        with open(self.filepath, encoding='utf-8') as f:
            paras = []
            for line in f.readlines():
                if '\ufeff' in line:
                    line = line.replace('\ufeff', '')
                vertices = line.split(",")
                if len(vertices) < 8:
                    continue
                points = [[int(vertices[0]), int(vertices[1])],
                          [int(vertices[2]), int(vertices[3])],
                          [int(vertices[4]), int(vertices[5])],
                          [int(vertices[6]), int(vertices[7])]]
                if len(vertices) == 8:
                    self.shapes.append((' ', points, None, None, False))
                elif len(vertices) > 8 and len(vertices) <= 16:
                    label = vertices[8:]
                    self.shapes.append((','.join(label), points, None, None, False))
                else:
                    para = [[int(vertices[8]), int(vertices[9])],
                            [int(vertices[10]), int(vertices[11])],
                            [int(vertices[12]), int(vertices[13])],
                            [int(vertices[14]), int(vertices[15])]]
                    label = vertices[16:]
                    self.shapes.append((','.join(label), points, None, None, False))
                    if para not in paras and not np.all(np.array(points)==np.array(para)):
                        paras.append(para)
                        self.shapes.append(('paragraph', para, None, None, False))
        return True