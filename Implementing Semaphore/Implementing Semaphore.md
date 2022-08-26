# Implementing Semaphore

Python does provide its own implementation of Semaphore and BoundedSemaphore, however, we want to implement a semaphore with a slight twist.

Briefly, a semaphore is a construct that allows some threads to access a fixed set of resources in parallel. Always think of a semaphore as having a fixed number of permits to give out. Once all the permits are given out, requesting threads, need to wait for a permit to be returned before proceeding forward.

Your task is to implement a semaphore which takes in its constructor the maximum number of permits allowed and is also initialized with the same number of permits. Additionally, if all the permits have been given out, the semaphore blocks threads attempting to acquire it.

# Solution
Given the above definition we can now start to think of what functions our Semaphore class will need to expose. We need a function to "gain the permit" and a function to "return the permit".

acquire() function to simulate gaining a permit

release() function to simulate releasing a permit

The constructor accepts an integer parameter defining the number of permits available with the semaphore. Internally we need to store a count which keeps track of the permits given out so far.

The skeleton for our Semaphore class looks something like this so far.

```python
class CountSemaphore():

    def __init__(self, permits):
        self.max_permits = permits
        self.given_out = 0

    def acquire(self):
        pass

    def release(self):
        pass
```

## Final solution

```python
from threading import Condition
from threading import Thread
import time


class CountSemaphore():

    def __init__(self, permits):
        self.max_permits = permits
        self.given_out = 0
        self.cond_var = Condition()

    def acquire(self):
        self.cond_var.acquire()
        while self.given_out == self.max_permits:
            self.cond_var.wait()

        self.given_out += 1
        self.cond_var.notifyAll()
        self.cond_var.release()

    def release(self):

        self.cond_var.acquire()

        while self.given_out == 0:
            self.cond_var.wait()

        self.given_out -= 1
        self.cond_var.notifyAll()
        self.cond_var.release()


def task1(sem):
    # consume the first permit
    sem.acquire()

    print("acquiring")
    sem.acquire()

    print("acquiring")
    sem.acquire()

    print("acquiring")
    sem.acquire()


def task2(sem):
    time.sleep(2)
    print("releasing")
    sem.release()

    time.sleep(2)
    print("releasing")
    sem.release()

    time.sleep(2)
    print("releasing")
    sem.release()


if __name__ == "__main__":
    sem = CountSemaphore(1)

    t1 = Thread(target=task1, args=(sem,))
    t2 = Thread(target=task2, args=(sem,))

    t1.start()
    time.sleep(1);
    t2.start()

    t1.join()
    t2.join()
```

