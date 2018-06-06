#encoding:UTF-8
#author:justry

import os
import numpy as np
import unittest

class GetBackGroundColorTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(GetBackGroundColorTest(''))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')