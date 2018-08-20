#encoding:UTF-8

import os
import pickle
import numpy as np

f1 = 'classify.pkl'
f0 = 'classify1.pkl'

def main():
    with open(f0, 'rb') as f:
        a0 = pickle.load(f)
    with open(f1, 'rb') as f:
        a1 = pickle.load(f)
    
    for i in a1.keys():
        if i in a0:
            if np.all(a0[i]==a1[i]):
                #print(i, '####equal!')
                print('\n')
            else:
                print(i, '****not equel!')
        else:
            print(i, '~~~~not in!')


if __name__ == '__main__':
    main()