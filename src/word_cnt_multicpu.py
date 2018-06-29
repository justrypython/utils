#encoding:UTF-8
#!/usr/bin/python
#author:justry

import os
import json
import time
import string
import multiprocessing

class ProccessEnqueuer(object):
    
    def __init__(self, paths, workers=5, max_queue_size=15):
        self.paths = paths
        self.wait_time = 2
        self.workers = workers
        self._threads = {i:None for i in range(workers)}
        self._stop_event = multiprocessing.Event()
        self.queue = multiprocessing.Queue(maxsize=max_queue_size)
        self.ret = []
        self._load_cnt = 0
        
    def start(self, workers=5):
        try:
            while len(self.paths):
                #import wingdbstub
                #wingdbstub.Ensure()
                #wingdbstub.debugger.StartDebug()
                self._get_ret()
                for i in self._threads.keys():
                    if self._threads[i] is None and len(self.paths):
                        thread = multiprocessing.Process(target=get_word_dict, args=(self.paths.pop(), self.queue, i, ))
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
    dir_path = '/media/zhaoke/b0685ee4-63e3-4691-ae02-feceacff6996/data/english/'
    ret = {}
    file_paths = []
    for root, _, files in os.walk(dir_path):
        for i in files:
            file_paths.append(dir_path+i)
    times = {}
    for workers in [10, 5, 2, 1]:
        ret = {}
        st = time.time()
        processes = ProccessEnqueuer(file_paths[:12], workers)
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

def get_word_dict(filepath, q, id_):
    #if id_ == 0:
        #import wingdbstub
        #wingdbstub.Ensure()
        #wingdbstub.debugger.StartDebug()
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
    print(id_, ' done!')
    q.put((ret, id_))
    #if id_ == 0:
        #wingdbstub.debugger.Stop()
    return True
    

if __name__ == '__main__':
    main()