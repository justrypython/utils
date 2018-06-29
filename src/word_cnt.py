#encoding:UTF-8
#!/usr/bin/python
#author:justry

import os
import json
import string

def main():
    #file_path = 'e:/justrypython/utils/data/500w.txt'
    dir_path = '/media/zhaoke/b0685ee4-63e3-4691-ae02-feceacff6996/data/english/'
    word_path = "e:/justrypython/ks_scan_ocr/ks_scan_ocr/src/emendate_chars/engwordlist.txt"
    ret = {}
    file_paths = []
    for root, _, files in os.walk(dir_path):
        for i in files:
            file_paths.append(dir_path+i)
    line_cnt = 0
    for i in file_paths:
        with open(i, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for k, i in enumerate(lines):
            line_cnt += 1
            i = i.replace('\n', '')
            for j in string.punctuation:
                i = i.replace(j, '').lower()
            for j in i.split():
                if j.isalpha():
                    cnt = ret.get(j, 0)
                    cnt += 1
                    ret[j] = cnt
            if line_cnt%10000==0:
                print(line_cnt)
    #with open(word_path, 'r') as f:
        #lines = f.readlines()
    #lines = [i.replace('\n', '') for i in lines]
    #s = ''
    #for i in lines:
        #if i not in ret:
            #s += '%s %d\n'%(i, 1)
        #else:
            #s += '%s %d\n'%(i, ret[i])
    s = ''
    for i, j in ret.items():
        if j > 200:
            s += '%s %d\n'%(i, j)
    with open('engwordlist.txt', 'w', encoding='utf-8') as f:
        f.write(s)
    

if __name__ == '__main__':
    main()