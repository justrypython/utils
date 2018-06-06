#encoding:UTF-8

import os
import cv2
import numpy as np
from PIL import Image


img_path = 'e:/justrypython/utils/data/images/20180322185157.png'
#img_path = '/justrypython/utils/data/images/20180321103024.png'


img = Image.open(img_path)

file_out = "test-fixed.png"

img.save('e:/justrypython/utils/data/images/20180322185157_good.png')

def main():
    with open(img_path, "rb") as f:
        rawImage = f.read()
    rawImage = np.fromstring(rawImage, dtype='uint8')
    npImage = np.array(rawImage)
    img = cv2.imdecode(npImage, cv2.IMREAD_UNCHANGED)
    cv2.imshow('img', img)
    cv2.waitKey()
    print('end')
    
if __name__ == '__main__':
    main()