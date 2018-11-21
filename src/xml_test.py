#encoding:UTF-8

import os
import numpy as np
import xml.etree.ElementTree as ET

src_path = r'E:/标注工作/词霸四六级结果/'
dst_path = r'E:/标注工作/词霸四六级结果TXT/'

def main():
    xmls = [i for i in os.listdir(src_path) if '.xml' in i]
    for i in xmls:
        tree = ET.ElementTree(file=src_path+i)
        root = tree.getroot()
        content = ''
        for j in root:
            if len(j) < 5:
                continue
            coords = j[4]
            assert coords[0].tag == 'xmin'
            assert coords[1].tag == 'ymin'
            assert coords[2].tag == 'xmax'
            assert coords[3].tag == 'ymax'
            xmin = coords[0].text
            ymin = coords[1].text
            xmax = coords[2].text
            ymax = coords[3].text
            content += ','.join([xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax])
            content += ',text\n'
        with open(dst_path+i.replace('.xml', '.txt'), 'w') as f:
            f.write(content)
    print('end')

if __name__ == '__main__':
    main()