```python
from threading import Thread
from threading import Lock
from threading import current_thread
from concurrent.futures import Future
import time
import random


class NonBlockingQueue:

    def __init__(self, max_size):
        self.max_size = max_size
        self.q = []
        self.lock = Lock()

    def dequeue(self):

        with self.lock:
            curr_size = len(self.q)

            if curr_size != 0:
                return self.q.pop(0)

            else:
                return False

    def enqueue(self, item):

        with self.lock:
            curr_size = len(self.q)

            if curr_size == self.max_size:
                return False

            else:
                self.q.append(item)
                return True


def consumer_thread(q):
    while 1:
        item = q.dequeue()

        if item == False:
            print("Consumer couldn't dequeue an item")
        else:
            print("\n{0} consumed item {1}".format(current_thread().getName(), item), flush=True)

        time.sleep(random.randint(1, 3))


def producer_thread(q):
    item = 1

    while 1:
        result = q.enqueue(item)
        if result is True:
            print("\n {0} produced item".format(current_thread().getName()), flush=True)
            item += 1


if __name__ == "__main__":
    no_block_q = NonBlockingQueue(5)
    
    consumerThread1 = Thread(target=consumer_thread, name="consumer", args=(no_block_q,), daemon=True)
    producerThread1 = Thread(target=producer_thread, name="producer", args=(no_block_q,), daemon=True)

    consumerThread1.start()
    producerThread1.start()

    time.sleep(15)
    print("Main thread exiting")
```
