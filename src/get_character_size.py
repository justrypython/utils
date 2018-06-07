#encoding:UTF-8
#author:justry

import os
import sys
import numpy as np

def get_character_size(s):
    try:
        row_l=len(s)
        utf8_l=len(s.encode('utf-8'))
        return (utf8_l-row_l)/2+row_l
    except:
        return None
    return None