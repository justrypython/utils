#encoding:UTF-8

import os
import numpy as np
from PyQt5.QtCore import *

from shape import Shape

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def get_area(poly):
    points = np.array([[i.x(), i.y()] for i in poly.points])
    x = points[:, 0]
    y = points[:, 1]
    return PolyArea(x, y)

def PolygonSorted(shapes):
    areas = [get_area(i) for i in shapes]
    ret = sorted(zip(shapes,areas), key=lambda x:x[-1])
    return [i[0] for i in ret]