# Problem Statement:

>This is a classical synchronization problem proposed by Dijkstra.

>Imagine you have five philosophers sitting on a roundtable. The philosopher's do only two kinds of activities. One: they contemplate, and two: they eat. However, they have only five forks between themselves to eat their food with. Each philosopher requires both the fork to his left and the fork to his right to eat his food.
>The arrangement of the philosophers and the forks are shown in the diagram.
>Design a solution where each philosopher gets a chance to eat his food without causing a deadlock

![image](https://user-images.githubusercontent.com/33947539/151494535-01b84ed3-8350-4e8b-86e9-7980b3e93820.png)

## Solution
For no deadlock to occur at all and have all the philosophers be able to eat, we would need ten forks, two for each philosopher. With five forks available, at most, only two philosophers will be able to eat while letting a third hungry philosopher hold onto the fifth fork and wait for another one to become available before he can eat.

Think of each fork as a resource that needs to be owned by one of the philosophers sitting on either side.

Let's try to model the problem in code before we even attempt to find a solution. Each fork represents a resource that two of the philosophers on either side can attempt to acquire. This intuitively suggests using a semaphore with a permit value of 1 to represent a fork. Each philosopher can then be thought of as a thread that tries to acquire the forks to the left and right of it. Given this, let's see how our class would look like:

```python
class DiningPhilosopherProblem:

    def __init__(self):
        self.forks = [None] * 5
        self.forks[0] = Semaphore(1)
        self.forks[1] = Semaphore(1)
        self.forks[2] = Semaphore(1)
        self.forks[3] = Semaphore(1)
        self.forks[4] = Semaphore(1)

    def life_cycle_of_a_philosopher(self, id):
        while True:
            self.contemplate()
            self.eat(id)

    def contemplate(self):
        sleep_for = random.randint(100, 500) / 1000
        time.sleep(sleep_for)

    def eat(self, id):
        pass
 ```
 
That was easy enough. Now think about the eat method. When a philosopher wants to eat, he needs the fork to the left and right of him. So:

```
Philosopher A(0) needs forks 4 and 0

Philosopher B(1) needs forks 0 and 1

Philosopher C(2) needs forks 1 and 2

Philosopher D(3) needs forks 2 and 3

Philosopher E(4) needs forks 3 and 4
``` 

This means each thread (philosopher) will also need to tell us what ID it is before we can attempt to lock the appropriate forks for him. That is why you see the eat() method takes in an ID parameter.

We can programmatically express the requirement for each philosopher to hold the right and left forks as follows:

```python
forks[id]
forks[(id+4) % 5]
```

### Deadlock Code

```python
class DiningPhilosopherProblem:

    def __init__(self):
        self.forks = [None] * 5
        self.forks[0] = Semaphore(1)
        self.forks[1] = Semaphore(1)
        self.forks[2] = Semaphore(1)
        self.forks[3] = Semaphore(1)
        self.forks[4] = Semaphore(1)

    def life_cycle_of_a_philosopher(self, id):
        while self.exit is False:
            self.contemplate()
            self.eat(id)

    def contemplate(self):
        sleep_for = random.randint(800, 1200) / 1000
        time.sleep(sleep_for)

    def eat(self, id):

        # acquire the left fork first
        self.forks[id].acquire()

        # acquire the right fork second
        self.forks[(id + 1) % 5].acquire()

        # eat to your heart's content
        print("Philosopher {0} is eating".format(id))

        # release forks for others to use
        self.forks[id].release()
        self.forks[(id + 1) % 5].release()
```

### How the above can lead to Deadlock 

If you run the above code, it'll eventually end up in a deadlock at some point. Realize if all the philosophers simultaneously grab their right fork, none would be able to eat.

### Fix of the above
A very simple fix is to allow only four philosophers at any given point in time to even try to acquire forks. Convince yourself that with five forks and four philosophers, deadlock is impossible, since at any point even if each philosopher grabs one fork, there will still be one fork left that can be acquired by one of the philosophers to eat. Implementing this solution requires us to introduce another semaphore with a permit of 4 which guards the logic for lifting/grabbing of the forks by the philosophers. The code appears below.

```python
from threading import Thread
from threading import Semaphore
import random
import time


class DiningPhilosopherProblem:

    def __init__(self):
        self.forks = [None] * 5
        self.forks[0] = Semaphore(1)
        self.forks[1] = Semaphore(1)
        self.forks[2] = Semaphore(1)
        self.forks[3] = Semaphore(1)
        self.forks[4] = Semaphore(1)

        self.max_diners = Semaphore(4)

        self.exit = False

    def life_cycle_of_a_philosopher(self, id):
        while self.exit is False:
            self.contemplate()
            self.eat(id)

    def contemplate(self):
        sleep_for = random.randint(800, 1200) / 1000
        time.sleep(sleep_for)

    def eat(self, id):
        # maxDiners allows only 4 philosophers to
        # attempt picking up forks.
        self.max_diners.acquire()

        # acquire the left fork first
        self.forks[id].acquire()

        # acquire the right fork second
        self.forks[(id + 4) % 5].acquire()

        # eat to your heart's content
        print("Philosopher {0} is eating".format(id))

        # release forks for others to use
        self.forks[id].release()
        self.forks[(id + 4) % 5].release()

        self.max_diners.release()


if __name__ == "__main__":

    problem = DiningPhilosopherProblem()

    philosophers = list()

    for id in range(0, 5):
        philosophers.append(Thread(target=problem.life_cycle_of_a_philosopher, args=(id,)))

    for philosopher in philosophers:
        philosopher.start()

    time.sleep(6)
    problem.exit = True

    for philosopher in philosophers:
        philosopher.join()
```        

