#encoding:UTF-8
#author:justry

import os
import time
import cv2
import functools
import numpy as np
from multiprocessing import Pool
import tensorflow as tf
from ks_nature_scene_ocr.line_recog.infer import line_recog_v1

def run(recognizer, img, gpu_id=0):
    if len(img.shape) >= 3:
        img = np.dot(img[...,:3], [0.299, 0.587, 0.114])
        img = img.astype(np.uint8)
    with tf.device('/gpu:%d' % gpu_id):
        ret = recognizer.infer_line([img], gpu_id)
    return ret

if __name__ == '__main__':
    model_path_ch = "/data/anaconda3/lib/python3.6/site-packages/ks_nature_scene_ocr/models/line_recog/ocr_168_engv1.ckpt-110000"
    recognizer = line_recog_v1.LineRecog(model_path_ch)
    run_img = functools.partial(run, recognizer)
    testFL = []
    for i in range(1, 6, 1):
        img = cv2.imread('line_%d.png'%i)
        testFL.append(img)
    print('one by one:')
    s = time.time()
    for fn in testFL:
        run(recognizer, fn)
    
    e1 = time.time()
    print('one by one time, ', e1 - s)
    
    print('concurrent')
    pool = Pool(1)
    rl = pool.map(run_img, testFL)
    pool.close()
    pool.join()
    e2 = time.time()
    print('concurrent time, ', e2 - e1)
    print(rl)