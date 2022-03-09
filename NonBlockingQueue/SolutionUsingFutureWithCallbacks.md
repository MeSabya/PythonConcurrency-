```python
from threading import Thread
from threading import RLock
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
        self.lock = RLock()

    def dequeue(self):

        result = None
        future = None

        with self.lock:
            curr_size = len(self.q)

            if curr_size != 0:
                result = self.q.pop(0)

                # remember to resolve a pending future for
                # a put request
                if len(self.q_waiting_puts) != 0:
                    self.q_waiting_puts.pop(0).set_result(True)

            else:
                # queue is empty so create a future for a get
                # request
                future = Future()
                self.q_waiting_gets.append(future)

        return result, future

    def enqueue(self, item):

        future = None
        with self.lock:
            curr_size = len(self.q)

            # queue is full so create a future for a put
            # request
            if curr_size == self.max_size:
                future = Future()
                self.q_waiting_puts.append(future)

            else:
                self.q.append(item)

                # remember to resolve a pending future for
                # a get request
                if len(self.q_waiting_gets) != 0:
                    future_get = self.q_waiting_gets.pop(0)
                    future_get.set_result(self.q.pop(0))

        return future


def retry_dequeue(future):
    item = future.result()
    print("\nretry_dequeue executed by thread {0} and {1} consumed on a retry".format(current_thread().getName(), item), flush=True)


def consumer_thread(q):
    while 1:
        item, future = q.dequeue()

        if item is None:
            future.add_done_callback(retry_dequeue)

        else:
            print("\n{0} consumed item {1}".format(current_thread().getName(), item), flush=True)

        # slow down the consumer
        time.sleep(1)


def retry_enqueue(future):
    print("\nCallback invoked by thread {0}".format(current_thread().getName()))
    item = future.item
    q = future.q
    new_future = q.enqueue(item)

    if new_future is not None:
        new_future.item = item
        new_future.q = q
        new_future.add_done_callback(retry_enqueue)
    else:
        print("\n{0} successfully added on a retry".format(item))


def producer_thread(q):
    item = 1
    while 1:
        future = q.enqueue(item)
        if future is not None:
            future.item = item
            future.q = q
            future.add_done_callback(retry_enqueue)

        item += 1

        # slow down the producer
        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    no_block_q = NonBlockingQueue(5)

    consumerThread1 = Thread(target=consumer_thread, name="consumer", args=(no_block_q,), daemon=True)
    producerThread1 = Thread(target=producer_thread, name="producer", args=(no_block_q,), daemon=True)

    consumerThread1.start()
    producerThread1.start()

    time.sleep(15)
    print("\nMain thread exiting")

```
