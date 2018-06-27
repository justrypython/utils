#encoding:UTF-8
#!/usr/bin/python
#author:justry

import os
import json
import time
import string
import multiprocessing

class ProccessEnqueuer(object):
    
    def __init__(self, paths, max_queue_size=5):
        self.paths = paths
        self.wait_time = 0.5
        self._threads = []
        self._stop_event = multiprocessing.Event()
        self.queue = multiprocessing.Queue(maxsize=max_queue_size)
        
    def start(self, workers=5):
        try:
            for i in range(workers):
                thread = multiprocessing.Process(target=get_word_dict, args=(self.paths.pop(), self.queue, i, ))
                thread.daemon = True
                self._threads.append(thread)
                thread.start()
        except:
            self.stop()
            raise

    def is_running(self):
        return self._stop_event is not None and not self._stop_event.is_set()
    
    def stop(self):
        if self.is_running():
            self._stop_event.set()
        for thread in self._threads:
            if thread.is_alive():
                thread.terminate()
        if self.queue is not None:
            self.queue.close()
        
        self._threads = []
        self._stop_event = None
        self.queue = None
    
    def get(self):
        while self.is_running():
            if not self.queue.empty():
                inputs = self.queue.get()
                if inputs is not None:
                    yield inputs
            else:
                time.sleep(self.wait_time)

def main():
    dir_path = 'e:/justrypython/utils/data/english/'
    ret = {}
    file_paths = []
    for root, _, files in os.walk(dir_path):
        for i in files:
            file_paths.append(dir_path+i)
    processes = ProccessEnqueuer(file_paths)
    processes.start()
    for i in processes.get():
        print('lenght: ', len(i))
    #s = ''
    #for i, j in ret.items():
        #if j > 1000:
            #s += '%s %d\n'%(i, j)
    #with open('engwordlist.txt', 'w', encoding='utf-8') as f:
        #f.write(s)

def get_word_dict(filepath, q, id_):
    if id_ == 0:
        import wingdbstub
        wingdbstub.Ensure()
        wingdbstub.debugger
    ret = {}
    line_cnt = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for k, i in enumerate(lines):
        line_cnt += 1
        i = i.replace('\n', '')
        for j in string.punctuation:
            i = i.replace(j, '').lower()
        for j in i.split():
            if j.isalpha():
                cnt = ret.get(j, 0)
                cnt += 1
                ret[j] = cnt
        if line_cnt%10000==0:
            print(line_cnt)
    if id_ == 0:
        wingdbstub.debugger.Stop()
    return ret
    

if __name__ == '__main__':
    main()