#encoding:UTF-8
#author:justry

import os
import time
import numpy as np
from multiprocessing import Pool

def run(fn):
    time.sleep(1)
    return fn * fn

if __name__ == '__main__':
    testFL = [1, 2, 3, 4, 5, 6]
    print('one by one:')
    s = time.time()
    for fn in testFL:
        run(fn)
    
    e1 = time.time()
    print('one by one time, ', e1 - s)
    
    print('concurrent')
    pool = Pool(5)
    rl = pool.map(run, testFL)
    pool.close()
    pool.join()
    e2 = time.time()
    print('concurrent time, ', e2 - e1)
    print(rl)