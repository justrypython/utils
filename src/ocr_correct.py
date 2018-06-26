#encoding:UTF-8
#author:justry

import os
import numpy as np

convert_dict = {'0':'o',
                'o':'0',
                'O':'0',
                '1':'l',
                'l':'1'}

def ocr_correct(s):
    return s

def isalpha(letter):
    return letter.isalpha()

def isdigit(letter):
    return letter.isdigit()

def and_(a, b):
    return a and b

def or_(a, b):
    return a or b

def convert(i, s, func, l, boolean):
    if i == 0:
        if func(s[1]):
            l.append(i)
    elif i == len(s)-1:
        if func(s[-2]):
            l.append(i)
    elif boolean(func(s[i-1]), func(s[i+1])):
        l.append(i)

def o_0(s):
    pos = [i for i, j in enumerate(s) if j in '0oOl1']
    convert_list = []
    for i in pos:
        if s[i] in 'oOl':
            # letter o or O or l
            convert(i, s, isdigit, convert_list, and_)
        else:
            # digit 0, 1
            convert(i, s, isalpha, convert_list, or_)
    s = [i for i in s]
    for i in convert_list:
        s[i] = convert_dict[s[i]]
    return ''.join(s)

def has_end_char(s):
    return '.' in s or '!' in s or '?' in s or ';' in s

def uppercase_lowercase(s):
    s = [i for i in s.split(' ') if i != '']
    end_char_list = [has_end_char(i) for i in s]
    convert_list = []
    for i, j in enumerate(s):
        if i == 0:
            s[i] = s[i][0].upper() + s[i][1:].lower()
        else:
            if end_char_list[i-1]:
                s[i] = s[i][0].upper() + s[i][1:].lower()
            else:
                s[i] = s[i].lower()
    return ' '.join(s)

if __name__ == '__main__':
    file_path = '/home/zhaoke/justrypython/utils/data/test/9781601988157-summary14.result'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i in lines:
        i = o_0(i)
        i = uppercase_lowercase(i)
        print(i)