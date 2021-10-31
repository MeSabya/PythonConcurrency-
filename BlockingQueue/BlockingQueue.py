from threading import Thread
from threading import Condition, current_thread
import time
import random

class BlockingQueue:
    def __init__(self, max_size):
        self.q = []
        self.curr_size = 0
        self.MAX_SIZE = max_size
        self.condn = Condition()

    def enqueue(self, item):
        self.condn.acquire()
        while self.curr_size == self.MAX_SIZE:
            self.condn.wait()

        self.q.append(item)
        self.curr_size +=1
        self.condn.notifyAll()
        print("\ncurrent size of queue {0}".format(self.curr_size), flush=True)
        self.condn.release()

    def dequeue(self):
        self.condn.acquire()
        while self.curr_size == 0:
            self.condn.wait()
        item = self.q.pop(0)
        self.curr_size -= 1
        self.condn.notifyAll()
        self.condn.release()

        return item

def consumer_thread(q):
    while 1:
        item = q.dequeue()
        print("\n{0} consumed item {1}".format(current_thread().getName(), item), flush=True)
        time.sleep(random.randint(1, 3))

def producer_thread(q, val):
    item = val
    while 1:
        q.enqueue(item)
        item += 1
        time.sleep(0.1)
if __name__ == "__main__":
    blocking_q = BlockingQueue(5)

    consumerThread1 = Thread(target=consumer_thread, name="consumer-1", args=(blocking_q,), daemon=True)
    consumerThread2 = Thread(target=consumer_thread, name="consumer-2", args=(blocking_q,), daemon=True)
    producerThread1 = Thread(target=producer_thread, name="producer-1", args=(blocking_q, 1), daemon=True)
    producerThread2 = Thread(target=producer_thread, name="producer-2", args=(blocking_q, 100), daemon=True)

    consumerThread1.start()
    consumerThread2.start()
    producerThread1.start()
    producerThread2.start()

    time.sleep(15)
    print("Main thread exiting")



