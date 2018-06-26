#encoding:UTF-8
#author:justry

import os
import numpy as np
import unittest
import auto_correct

class AutoCorrectTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_0(self):
        pass
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(AutoCorrectTest('test_0'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')