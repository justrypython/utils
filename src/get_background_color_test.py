#encoding:UTF-8
#author:justry

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import unittest
import get_background_color

class GetBackGroundColorTest(unittest.TestCase):
    
    def setUp(self):
        self.img = cv2.imread('20180516174219.jpg')
    
    def tearDown(self):
        pass
    
    def test_0(self):
        a = self.img[:, :, 0]
        b = np.histogram(a, bins=256)
        ms0 = get_background_color.move_average(b[0])
        ms1 = get_background_color.move_average(b[0], n=20)
        fig = plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(ms0)
        plt.subplot(2, 1, 2)
        plt.plot(ms1)
        plt.show()
        print('end')
    
    def test_get_background_color(self):
        bg_color = get_background_color.get_background_color(self.img)
        newimg = np.zeros(self.img.shape, dtype=np.uint8)
        newimg[:, :] = bg_color
        fig = plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(self.img)
        plt.subplot(1, 2, 2)
        plt.imshow(newimg)
        plt.show()
        print('end')
        
    def test_move_average(self):
        a = np.arange(20)
        ms = get_background_color.move_average(a)
        self.assertListEqual(ms.tolist(), 
                             np.array([4.5, 5.5,   6.5,   7.5,   8.5,
                                       9.5,  10.5,  11.5,  12.5, 13.5,
                                       14.5]).tolist())
    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(GetBackGroundColorTest('test_0'))
    suite.addTest(GetBackGroundColorTest('test_get_background_color'))
    suite.addTest(GetBackGroundColorTest('test_move_average'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')