#encoding:UTF-8

import os

path = 'E:/justrypython/utils/data/primes/'


def main():
    files = [i for i in os.listdir(path) if '.txt' in i and i != 'primes.txt']
    with open(path+'primes.txt', 'w', encoding='utf-8') as f:
        for i in files:
            txt = open(path+i, encoding='utf-8')
            lines = txt.readlines()
            txt.close()
            lines = [j for j in lines if j != '\n']
            lines = [j.split() for j in lines]
            lines = [' '.join(j) for j in lines]
            lines = '\n'.join(lines)
            f.write(lines)

if __name__ == '__main__':
    main()