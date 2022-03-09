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
        self.q_waiting_puts = []
        self.q_waiting_gets = []
        self.lock = Lock()

    def dequeue(self):

        result = None
        future = None

        with self.lock:
            curr_size = len(self.q)

            if curr_size != 0:
                result = self.q.pop()

                if len(self.q_waiting_puts) > 0:
                    self.q_waiting_puts.pop().set_result(True)

            else:
                future = Future()
                self.q_waiting_gets.append(future)

        return result, future

    def enqueue(self, item):

        future = None
        with self.lock:
            curr_size = len(self.q)

            if curr_size == self.max_size:
                future = Future()
                self.q_waiting_puts.append(future)

            else:
                self.q.append(item)

                if len(self.q_waiting_gets) != 0:
                    future_get = self.q_waiting_gets.pop()
                    future_get.set_result(True)

        return future


def consumer_thread(q):
    while 1:
        item, future = q.dequeue()

        if item is None:
            print("Consumer received a future but we are ignoring it")
        else:
            print("\n{0} consumed item {1}".format(current_thread().getName(), item), flush=True)

        # slow down consumer thread
        time.sleep(random.randint(1, 3))


def producer_thread(q):
    item = 1
    while 1:
        future = q.enqueue(item)
        if future is not None:
            while future.done() == False:
                print("waiting for future to resolve")
                time.sleep(0.1)
        else:
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
