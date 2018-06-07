#encoding:UTF-8
#author:justry

import os
import sys
import numpy as np
import unittest

import get_character_size

class GetStringSize(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_0(self):
        a = '对一维数组进行直方图统计，其参数列表如下：'
        b = get_character_size.get_character_size(a)
        self.assertEqual(b, 42)
    
    def test_1(self):
        a = 'imshow一维数组进行直方图统计，其参数列表如下：'
        b = get_character_size.get_character_size(a)
        self.assertEqual(b, 46)
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(GetStringSize('test_0'))
    suite.addTest(GetStringSize('test_1'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')