#coding:utf-8
from threading import Thread
from multiprocessing import Process, Queue
from time import sleep
import signal

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def signal_handler(signal, frame):
    global interrupted
    interrupted = True
    
signal.signal(signal.SIGINT, signal_handler)

interrupted = False

@async
def time_1s():
    cnt = 0
    while True:
        print('%ds...'%cnt)
        cnt += 1
        sleep(1)

@async
def A():
    sleep(10)
    print ("a function")

def B():
    print ("b function")
    
class C(object):
    def __init__(self):
        self.p1 = 1
        self.p2 = 100
        self.queue = Queue()
    
    @async
    def d(self):
        sleep(8)
        print('\nd method')
        print('\t%d'%self.p1)
        #print('\t%d'%self.p2)
        self.queue.put(self.p1)
        self.p1 += 1
    
    @async    
    def e(self):
        sleep(5)
        print('\ne method')
        print('\t%d'%self.p1)
        print('\t%d'%self.p2)
        self.p2 += 1
        
    @async
    def f(self):
        while True:
            a = self.queue.get()
            print('####%e'%a)
            self.d()

time_1s()
#A()
#B()

c = C()
c.f()
c.d()
#c.e()
#print('-'*30)
#c.d()
#c.e()
#print('-'*30)
#c.d()
#c.e()
#print('-'*30)
#c.d()
#c.e()

import numpy as np
import tensorflow as tf