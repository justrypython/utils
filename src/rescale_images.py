#encoding:UTF-8

"""
缩放图像，丰富训练集
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

path = 'E:/justrypython/utils/data/numbers/'
dst_path = 'E:/justrypython/utils/results/numbers/'


def read_txt(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = [i.replace('\n', '').split(',') for i in lines]
        lines = np.array(lines)
        lines = lines[:, :8].astype(np.int32)
    return lines

def save_array_to_txt(arr, filepath):
    with open(filepath, 'w') as f:
        lines = '\n'.join([','.join(i.astype(np.str)) for i in arr])
        f.write(lines)
        
def resize_poly(xy, args):
    return (xy[0]*args[0], xy[1]*args[1])

def main():
    paths = [i for i in os.listdir(path) if '.jpg' in i]
    for i in paths:
        img = cv2.imread(path+i)
        y, x = img.shape[:2]
        for j, factor in enumerate([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]):
            y_factor = factor-0.05+0.1*np.random.random()
            newimg = cv2.resize(img, (int(x*factor), int(y*y_factor)))
            polys = read_txt(path+i.replace('.jpg', '.txt'))
            polys = polys.reshape((-1, 4, 2))
            newpolys = np.apply_along_axis(resize_poly, -1, polys, args=(factor, y_factor))
            newpolys = newpolys.reshape((-1, 8)).astype(np.int)
            a = np.ones((newpolys.shape[0], 9), dtype=np.int)
            a[:, :8] = newpolys
            save_array_to_txt(a, dst_path+'number_%d_'%j+i.replace('.jpg', '.txt'))
            cv2.imwrite(dst_path+'number_%d_'%j+i, newimg)
          
            
if __name__ == '__main__':
    main()