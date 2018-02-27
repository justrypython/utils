#encoding:UTF-8

import os
import re

def duplicate(l, n):
    for i in range(n):
        for item in l:
            os.system('cp %s %s_%d%s'%(item, item[:-4], i, item[-4:]))

def main():
    # '0000'
    path = 'data/'
    images = [path+i for i in os.listdir(path)]
    pattern = re.compile('^0000')
    l = []
    for i in images:
        if '/0000' in i:
            l.append(i)
    duplicate(l, 4)
    
    l = [i for i in images if 'digit' in i]
    duplicate(l, 5)
    
    l = [i for i in images if 'english' in i]
    duplicate(l, 2)
    
    l = [i for i in images if 'fapiao' in i]
    duplicate(l, 10)
    
    l = [i for i in images if 'pdf' in i]
    duplicate(l, 6)
    
    l = [i for i in images if 'small' in i]
    duplicate(l, 4)


if __name__ == '__main__':
    main()