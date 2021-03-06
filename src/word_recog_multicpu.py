#encoding:UTF-8
#!/usr/bin/python
#author:justry

import os
import json
import time
import string
import pickle
import numpy as np
import multiprocessing
from ks_nature_scene_ocr.line_recog.infer import line_recog_v1

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class ProccessEnqueuer(object):
    
    def __init__(self, image_boxes, bounding_boxes, workers=1, max_queue_size=15):
        self.image_boxes = image_boxes
        self.bounding_boxes = bounding_boxes
        self.wait_time = 2
        self.workers = workers
        self._threads = {i:None for i in range(workers)}
        self._stop_event = multiprocessing.Event()
        self.queue = multiprocessing.Queue(maxsize=max_queue_size)
        self.ret = []
        self._load_cnt = 0
        model_path_ch = "/data/anaconda3/lib/python3.6/site-packages/ks_nature_scene_ocr/models/line_recog/ocr_168_engv1.ckpt-110000"
        self.recognizer = line_recog_v1.LineRecog(model_path_ch)
        
    def start(self, workers=5):
        try:
            while len(self.image_boxes):
                #import wingdbstub
                #wingdbstub.Ensure()
                #wingdbstub.debugger.StartDebug()
                self._get_ret()
                for i in self._threads.keys():
                    if self._threads[i] is None and len(self.image_boxes):
                        thread = multiprocessing.Process(target=get_word_dict, args=(self.recognizer,
                                                                                     self.image_boxes.pop(),
                                                                                     self.bounding_boxes.pop(),
                                                                                     self.queue, i, ))
                        thread.daemon = True
                        self._threads[i] = thread
                        thread.start()
                #wingdbstub.debugger.StopDebug()
            self._get_ret()
            self.stop()
        except:
            self.stop()
            raise

    def _get_ret(self):
        while not self.queue.empty():
            inputs = self.queue.get()
            if inputs is not None:
                self._load_cnt += 1
                print('load %d'%self._load_cnt)
                self.terminate(inputs[1])
                self.ret.append(inputs[0])

    def is_running(self):
        return self._stop_event is not None and not self._stop_event.is_set()
    
    def stop(self):
        if self.is_running():
            self._stop_event.set()
        for thread in self._threads.values():
            if thread is not None and thread.is_alive():
                thread.terminate()
        if self.queue is not None:
            self.queue.close()
        
        self._threads = {i:None for i in range(self.workers)}
        self._stop_event = None
        self.queue = None
        
    def terminate(self, id_):
        thread = self._threads[id_]
        if thread is not None:
            thread.terminate()
            self._threads[id_] = None

def combineRet(dicts):
    ret = {}
    for i in dicts:
        for j, k in i.items():
            cnt = ret.get(j, 0)
            ret[j] = cnt + k
    return ret

def main():
    with open('image_boxes.pickle', 'rb') as handle:
        image_boxes = pickle.load(handle)
    with open('bounding_boxes.pickle', 'rb') as handle:
        bounding_boxes = pickle.load(handle)
    bounding_boxes = [i for i in bounding_boxes]
    times = {}
    for workers in [10, 5, 2, 1]:
        ret = {}
        st = time.time()
        processes = ProccessEnqueuer(image_boxes, bounding_boxes, workers)
        processes.start()
        et = time.time()
        times[workers] = et - st
        ret = processes.ret
        ret = combineRet(ret)
        with open(str(workers), 'w') as f:
            json.dump(ret, f)
    with open('times', 'w') as f:
        json.dump(times, f)
    #s = ''
    #for i, j in ret.items():
        #if j > 1000:
            #s += '%s %d\n'%(i, j)
    #with open('engwordlist.txt', 'w', encoding='utf-8') as f:
        #f.write(s)

def get_word_dict(recognizer, img_box, bounding_box, q, id_):
    if id_ == 0:
        import wingdbstub
        wingdbstub.Ensure()
        wingdbstub.debugger.StartDebug()
    if len(img_box.shape) >= 3:
        img_box = np.dot(img_box[...,:3], [0.299, 0.587, 0.114])
        img_box = img_box.astype(np.uint8)
    result = recognizer.infer_line([img_box])
    print(id_, ' done!')
    q.put((result, bounding_box, id_))
    if id_ == 0:
        wingdbstub.debugger.Stop()
    return True
    

if __name__ == '__main__':
    main()