from threading import Condition, Thread, current_thread
import time 

class TokenBucketFilterFactory:
    @staticmethod
    def makeTokenBucketFilter(capacity):
        tbf = MultiThreadedTokenBucketFilter(capacity)
        tbf.initDaemonThread()
        return tbf
    

class MultiThreadedTokenBucketFilter:
    def __init__(self, maxTokens):
        self.MAX_TOKENS = maxTokens
        self.possibleTokens = 0
        self.condn = Condition()
        self.ONE_SECOND = 1
    
    def initDaemonThread(self):
        dt = Thread(target = self.daemonThread)
        dt.setDaemon(True)
        dt.start()
    
    def daemonThread(self):
        while True:
            self.condn.acquire()
            if self.possibleTokens < self.MAX_TOKENS:
                self.possibleTokens = self.possibleTokens + 1
            
            self.condn.notify()
            self.condn.release()
            
            time.sleep(self.ONE_SECOND)
    
    def getToken(self):
        self.condn.acquire()
        while self.possibleTokens ==0:
            self.condn.wait()
        
        self.possibleTokens = self.possibleTokens-1
        self.condn.release()

        print("Granting " + current_thread().getName() + " token at " + str(time.time()))
    

if __name__=="__main__":
    threads_list = []
    bucket = TokenBucketFilterFactory.makeTokenBucketFilter(10)
    for x in range(10):
        workerthread =  Thread(target=bucket.getToken)
        workerthread.name = "Thread_" + str(x+1);
        threads_list.append(workerthread)
        
    
    for t in threads_list:
        t.start()
        
    for t in threads_list:
        t.join()
    
    
    
        
        
    
        