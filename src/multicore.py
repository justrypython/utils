#encoding:UTF-8
#!/usr/bin/python
#author:justry

import os
import time
import multiprocessing

def job(q):
    ret = 0
    for i in range(100000000):
        ret = i + i**2 + i**3
    q.put(ret)
    
def multicore():
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=job, args=(q, ))
    p1.start()
    #p1.join()
    res1 = q.get()
    print('multicore', res1)
    
if __name__ == '__main__':
    st = time.time()
    multicore()
    ed = time.time()
    print('multicore time: ', ed - st)