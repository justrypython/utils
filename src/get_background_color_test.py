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
        self.img = cv2.imread('20180607111256.png')
    
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
    
    def test_1(self):
        a = self.img[:, :, 1]
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
    
    def test_2(self):
        a = self.img[:, :, 2]
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
    
    def test_get_background(self):
        bg = get_background_color.get_background(self.img)
        fig = plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(self.img)
        plt.subplot(1, 2, 2)
        plt.imshow(bg)
        plt.show()
        print('end')
        
    def test_put_chinese(self):
        result = [[('空前绝后', 
                    [[157.5866928294657, 192.0986359632039], 
                     [253.13630347788555, 110.31564606882323], 
                     [270.38329652607734, 138.72315700822767], 
                     [174.8336864055262, 220.50614540027138]])]]
        img = get_background_color.put_chinese(self.img, result)
        fig = plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(self.img)
        plt.subplot(1, 2, 2)
        plt.imshow(img)
        plt.show()
        print('end')
        
    def test_get_wha(self):
        result = [[('空前绝后', 
                    [[157.5866928294657, 192.0986359632039], 
                     [253.13630347788555, 110.31564606882323], 
                     [270.38329652607734, 138.72315700822767], 
                     [174.8336864055262, 220.50614540027138]])]]
        polys = result[0][0][1]
        w_, h_, angle_ = get_background_color.get_wha(polys)
        polys = np.array(polys)
        w = polys[0]-polys[1]
        w = np.square(w)
        w = np.sum(w)
        w = np.sqrt(w)
        h = polys[1]-polys[2]
        h = np.square(h)
        h = np.sum(h)
        h = np.sqrt(h)        
        self.assertEqual(w_, int(w))
        self.assertEqual(h_, int(h))
        
    def test_get_transform_perspective(self):
        result = [[('空前绝后', 
                    [[157.5866928294657, 192.0986359632039], 
                     [253.13630347788555, 110.31564606882323], 
                     [270.38329652607734, 138.72315700822767], 
                     [174.8336864055262, 220.50614540027138]])]]
        polys = result[0][0][1]
        img = get_background_color.get_transform_perspective(self.img, polys)
        plt.imshow(img)
        plt.show()
        
    def test_move_average(self):
        a = np.arange(20)
        ms = get_background_color.move_average(a)
        self.assertListEqual(ms.tolist(), 
                             np.array([4.5, 5.5,   6.5,   7.5,   8.5,
                                       9.5,  10.5,  11.5,  12.5, 13.5,
                                       14.5]).tolist())
    

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(GetBackGroundColorTest('test_0'))
    #suite.addTest(GetBackGroundColorTest('test_1'))
    #suite.addTest(GetBackGroundColorTest('test_2'))
    #suite.addTest(GetBackGroundColorTest('test_get_background_color'))
    #suite.addTest(GetBackGroundColorTest('test_get_background'))
    #suite.addTest(GetBackGroundColorTest('test_move_average'))
    suite.addTest(GetBackGroundColorTest('test_put_chinese'))
    suite.addTest(GetBackGroundColorTest('test_get_wha'))
    #suite.addTest(GetBackGroundColorTest('test_get_transform_perspective'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')