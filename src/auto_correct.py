#encoding:UTF-8
#author:justry

import os
import numpy as np
from autocorrect import spell
from ocr_correct import o_0, uppercase_lowercase

if __name__ == '__main__':
    file_path = '/home/zhaoke/justrypython/utils/data/test/9781601988157-summary14.result'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i in lines:
        i = o_0(i)
        i = uppercase_lowercase(i)
        ret = []
        for j in i.split():
            ret.append(spell(j))
        print(i)
        print(' '.join(ret))
        print('#'*70)