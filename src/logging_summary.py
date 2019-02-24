#encoding:UTF-8
#author:justry

import os
import numpy as np

def summary(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    detect = []
    recognize = []
    total = []
    for i in lines:
        if 'web_service.post return success, time:' in i:
            index = i[-10:].find(':')
            total.append(i[1-10+index:-1])
        elif 'nature_scene_ocr.recognize line recognizer time:' in i:
            index = i[-10:].find(':')
            recognize.append(i[1-10+index:-1])
        elif 'nature_scene_ocr.recognize get boxes time:' in i:
            index = i[-10:].find(':')
            detect.append(i[1-10+index:-1])
    return (np.array(detect).astype(np.float), 
            np.array(recognize).astype(np.float), 
            np.array(total).astype(np.float))

if __name__ == '__main__':
    path = 'multigpu_results/logging.log'
    #path = 'singlegpu_results/logging.log'
    #path = "singlegpu_multiprocess_results/logging.log"
    detect, recognize, total = summary(path)
    print('detect time is ', np.average(detect))
    print('recognize time is ', np.average(recognize))
    print('total time is ', np.average(total))