import multiprocessing
import time

def task(pid):
    # do something
    return pid
def main():
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()
    cpus = multiprocessing.cpu_count()
    results = []
    for i in range(0, 100):
        result = pool.apply_async(task, args=(i,))
        results.append(result)
    #pool.close()
    #pool.join()
    for result in results:
        print(result.get())
        
    time.sleep(10)
    for i in range(100, 200):
        result = pool.apply_async(task, args=(i,))
        results.append(result)
    
    for result in results:
        print(result.get())
        
if __name__ == '__main__':
    main()