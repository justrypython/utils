#encoding:UTF-8

import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import unittest
from get_dominant_color import get_dominant_color

class GetDominantColorTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_0(self):
        for i in os.listdir():
            if '.png' in i:
                self.img = cv2.imread(i)
                self.img = self.img[int(self.img.shape[0]/2):]
                self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)
                self.img = Image.fromarray(self.img)
                background_color = get_dominant_color(self.img)
                img = np.asarray(self.img)
                background = np.zeros(img.shape)
                background = background.astype(np.uint8)
                if len(background_color) == 4:
                    background[:, :] = background_color
                else:
                    background[:, :] = list(background_color) + [255]
                fig = plt.figure()
                
                plt.subplot(1, 2, 1)
                plt.imshow(img)
                
                plt.subplot(1, 2, 2)
                plt.imshow(background)
                
                plt.show()
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(GetDominantColorTest('test_0'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')