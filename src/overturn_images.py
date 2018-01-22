#encoding:UTF-8

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


path = '/media/zhaoke/b0685ee4-63e3-4691-ae02-feceacff6996/data/'
dst_path = '/media/zhaoke/b0685ee4-63e3-4691-ae02-feceacff6996/rctw17_overturn_east/'

def overturn_lr(x):
    def _overturn_lr(*args):
        return x-args[0][0], args[0][1]
    return _overturn_lr

def overturn_ud(y):
    def _overturn_ud(*args):
        return args[0][0], y-args[0][1]
    return _overturn_ud
    

def main():
    paths = [i for i in os.listdir(path) if '.jpg' in i]
    #lr
    for i in paths[:100]:
        img = cv2.imread(path+i)
        y, x = img.shape[:2]
        overturn_func = overturn_lr(x)
        img = img[:, ::-1]
        try:
            f = open(path+i.replace('.jpg', '.txt'))
            lines = f.readlines()
            f.close()
            lines = [j.replace('\n', '').replace('\r', '').split(',') for j in lines]
            lines = np.array(lines).astype(np.int)
            polys = lines[:, :8]
            labels = lines[:, -1:]
            polys = polys.reshape([-1, 4, 2])
            polys = np.apply_along_axis(overturn_func, -1, polys)
            polys = polys[:, [1, 0, 3, 2]]
            polys = polys.reshape((-1, 8))
            polys = np.concatenate([polys, labels], axis=-1)
            polys = polys.astype(np.str)
            polys = '\n'.join([','.join(j) for j in polys])
        except:
            print(i)
            continue
        cv2.imwrite(dst_path+'lr/lr_'+i, img)
        f = open(dst_path+'lr/lr_'+i.replace('.jpg', '.txt'), 'w')
        f.write(polys)
        f.close()
    #ud
    for i in paths[:100]:
        img = cv2.imread(path+i)
        y, x = img.shape[:2]
        overturn_func = overturn_ud(y)
        img = img[::-1]
        try:
            f = open(path+i.replace('.jpg', '.txt'))
            lines = f.readlines()
            f.close()
            lines = [j.replace('\n', '').replace('\r', '').split(',') for j in lines]
            lines = np.array(lines).astype(np.int)
            polys = lines[:, :8]
            labels = lines[:, -1:]
            polys = polys.reshape([-1, 4, 2])
            polys = np.apply_along_axis(overturn_func, -1, polys)
            polys = polys[:, [3, 2, 1, 0]]
            polys = polys.reshape((-1, 8))
            polys = np.concatenate([polys, labels], axis=-1)
            polys = polys.astype(np.str)
            polys = '\n'.join([','.join(j) for j in polys])
        except:
            print(i)
            continue
        cv2.imwrite(dst_path+'ud/ud_'+i, img)
        f = open(dst_path+'ud/ud_'+i.replace('.jpg', '.txt'), 'w')
        f.write(polys)
        f.close()

if __name__ == '__main__':
    main()