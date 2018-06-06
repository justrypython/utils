#encoding:UTF-8

import os
import random
import numpy as np
import matplotlib.pyplot as plt


def get_ratio(pos):
    pos = np.array(pos).reshape((-1, 1))
    def _get_ratio(*args):
        pos_list = pos
        ratios = args[0]
        ratios[ratios>=0] = 1
        ratios[ratios<0] = -1
        ratios *= -1
        ratios = np.tile(ratios, (len(pos_list), 1))
        return 1 + ratios * pos
    return _get_ratio

def mm(pos, ratio, init_m=10000, t=1000):
    randn = np.random.random((len(ratio), t))
    randn -= np.array(ratio).reshape((len(ratio), 1))
    func = get_ratio(pos)
    ratios = np.apply_along_axis(func, 0, randn)
    ratios = np.cumprod(ratios, axis=-1)
    return init_m * ratios

def mm1(pos=0.01, ratio=0.53, init_m=10000, t=1000):
    result = [init_m]
    p = 1 + pos
    n = 1 - pos
    m = init_m
    for i in range(t):
        randn = np.random.random()
        if randn >= ratio:
            m *= n
        else:
            m *= p
        result.append(m)
    return result

def mm2(pos=[0.01, 0.02, 0.04, 0.08], ratio=0.53, init_m=10000, t=1000):
    result = [[init_m] * len(pos)]
    p = 1 + np.array(pos)
    n = 1 - np.array(pos)
    m = np.array([init_m] * len(pos))
    for i in range(t):
        randn = np.random.random()
        if randn >= ratio:
            m = m * n
        else:
            m = m * p
        result.append(m)
    return result

def showmm():
    results1 = mm([0.01, 0.02, 0.04, 0.08], [0.52])
    results1 = np.squeeze(results1)
    plt.plot(results1[0], 'r')
    plt.plot(results1[1], 'b')
    plt.plot(results1[2], 'g')
    plt.plot(results1[3], 'y')
    plt.show()
    
def showmm1():
    while True:
        results1 = mm1(0.01)
        results2 = mm1(0.02)
        results3 = mm1(0.04)
        results4 = mm1(0.08)
        plt.plot(results1, 'r')
        plt.plot(results2, 'b')
        plt.plot(results3, 'g')
        plt.plot(results4, 'y')
        plt.show()
    
def showmm2():
    while True:
        results = np.array(mm2())
        plt.plot(results[:, 0], 'r')
        plt.plot(results[:, 1], 'b')
        plt.plot(results[:, 2], 'g')
        plt.plot(results[:, 3], 'y')
        plt.show()
    
def showmm2_1(ratio, times):
    result = []
    print('for ratio %.2f %d times'%(ratio, times))
    for i in range(1000):
        results = np.array(mm2(np.arange(0.001, 0.3, 0.001), ratio=ratio, t=times))
        result.append(results[-1])
    result = np.log(np.array(result)/10000)
    #plt.plot(result[:, 0], 'r')
    #plt.plot(result[:, 1], 'b')
    #plt.plot(result[:, 2], 'g')
    #plt.plot(result[:, 3], 'y')
    #plt.show()
    #plt.plot(result.mean(axis=0), 'r')
    #plt.plot(result.std(axis=0), 'g')
    #plt.show()
    a = np.argmax(result.mean(axis=0))
    b = np.argmax(result.mean(axis=0)-result.std(axis=0))
    print('the max mean is at %f, and max mean is %f'%(0.001*(a+1), np.max(result.mean(axis=0))))
    print('the max diff is at %f, and max diff is %f'%(0.001*(b+1), np.max(result.mean(axis=0)-result.std(axis=0))))
    print('end')
    
def showmm2_2():
    for ratio in np.arange(0.50, 0.6, 0.01):
        #showmm2_1(ratio, 100)
        #showmm2_1(ratio, 200)
        #showmm2_1(ratio, 400)
        showmm2_1(ratio, 1000)
        showmm2_1(ratio, 2000)
        print('#'*70)
        
def showmm2_3():
    while True:
        result = []
        results = np.array(mm2([0.01, 0.02, 0.04, 0.057, 0.08], ratio=0.53, t=2000))
        result.append(results[-1])
        result = np.log(np.array(result)/10000) 
        plt.plot(results[:, 0], 'r')
        plt.plot(results[:, 1], 'b')
        plt.plot(results[:, 2], 'g')
        plt.plot(results[:, 3], 'y')
        plt.plot(results[:, 4], 'm')
        plt.show()
        print(result)
        
def main():
    #showmm2_2()
    showmm2_3()

if __name__ == '__main__':
    main()