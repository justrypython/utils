#encoding:UTF-8
#author:justry

import os
import numpy as np
import unittest
import ocr_correct

class OCRCorrectTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_o_0_0(self):
        s0 = "only your heart could save me, too"
        s1 = "0nly your heart could save me, to0"
        s_ = ocr_correct.o_0(s1)
        self.assertEqual(s_, s0)
    
    def test_o_0_1(self):
        s0 = "only your heart could save me, too"
        s1 = "only your heart c0u1d save me, too"
        s_ = ocr_correct.o_0(s1)
        self.assertEqual(s_, s0)
    
    def test_o_0_2(self):
        s0 = "only your heart could save me, too"
        s1 = "on1y your heart could save me, too"
        s_ = ocr_correct.o_0(s1)
        self.assertEqual(s_, s0)
    
    def test_o_0_3(self):
        s0 = "only your heart could save me, to0"
        s1 = "on1y your heart cou1d save me, t00"
        s_ = ocr_correct.o_0(s1)
        self.assertEqual(s_, s0)
    
    def test_uppercase_lowercase_0(self):
        s0 = "Only your. Only you, only you ! Only you? Only your heart could save me, too"
        s1 = "only your. only you, only you ! only you? only your heart could save me, too"
        s_ = ocr_correct.uppercase_lowercase(s1)
        self.assertEqual(s_, s0)
    
    def test_uppercase_lowercase_1(self):
        s0 = "Only your. Only you, only you ! Only you? Only your heart could save me, too"
        s1 = "only yOUr. only you, only you ! oNly you? only your heart couLd save me, too"
        s_ = ocr_correct.uppercase_lowercase(s1)
        self.assertEqual(s_, s0)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(OCRCorrectTest('test_o_0_0'))
    suite.addTest(OCRCorrectTest('test_o_0_1'))
    suite.addTest(OCRCorrectTest('test_o_0_2'))
    suite.addTest(OCRCorrectTest('test_o_0_3'))
    suite.addTest(OCRCorrectTest('test_uppercase_lowercase_0'))
    suite.addTest(OCRCorrectTest('test_uppercase_lowercase_1'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')