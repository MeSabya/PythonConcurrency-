'''
1. How to rate limit ? The bucket size is the rate limit. 
2. How to add tokens at a constant rate ? using sleep 
3. How to rate limit clients ?  
'''

from threading import Thread, Condition, current_thread
import time

class TokenBucketFilter:
    def __init__(self, rate_limit) -> None:
        self.rate_limit = rate_limit
        self.cond = Condition()
        self.queue = []
        self.ONE_SECOND = int(1)
        producer_thread = Thread(target = self.daemon_thread)
        producer_thread.setDaemon(True)
        producer_thread.start()
    
    def daemon_thread(self):
        while True:
            self.cond.acquire()
            while len(self.queue) > self.rate_limit:
                self.cond.wait()
            self.queue.append(1)
            self.cond.notify()
            self.cond.release()
            time.sleep(self.ONE_SECOND)
    def get_token(self):
        self.cond.acquire()
        while len(self.queue) == 0:
            self.cond.wait()
        self.queue.pop()
        self.cond.notify()
        self.cond.release()
        print("Granting " + current_thread().getName() + " token at " + str(time.time()))

if __name__ == "__main__":
    threads_list = [];
    bucket = TokenBucketFilter(10)
    
    for x in range(10):
        workerthread =  Thread(target=bucket.get_token)
        workerthread.name = "Thread_" + str(x+1)
        threads_list.append(workerthread)
        
    
    for t in threads_list:
        t.start()
        
    for t in threads_list:
        t.join()
        
