### Does it matter if we use notify() or notifyAll() method in our implementation?

In both the enqueue() and dequeue() methods we use the notifyAll() method instead of the notify() method. 
The reason behind the choice is very crucial to understand. Consider a situation with two producer threads and 
one consumer thread all working with a queue of size one. It's possible that when an item is added to the queue by one of 
the producer threads, the other two threads are blocked waiting on the condition variable. If the producer thread after adding an item invokes notify() 
it is possible that the other producer thread is chosen by the system to resume execution. The woken-up producer thread would find the queue full and go 
back to waiting on the condition variable, causing a deadlock. Invoking notifyAll() assures that the consumer thread also gets a chance to wake up and resume execution.
