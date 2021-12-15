# Thread Safe Deferred Callback
## Probelm Description 
Design and implement a thread-safe class that allows registration of callback methods that are executed after a user specified time interval in seconds has elapsed.

## Solution
Let us try to understand the problem without thinking about concurrency. Let's say our class exposes an API called add_action() that'll take a parameter action, 
which will get executed after user specified seconds. 
Anyone calling this API should be able to specify after how many seconds should our class invoke the passed-in action.

- One possible solution is to have an execution thread that maintains a priority queue (min-heap) of actions ordered by the time remaining to execute each of the actions. 
- The execution thread can sleep for the duration equal to the time duration before the earliest action in the min-heap becomes due for execution.

- Consumer threads can come and add their desired actions in the min-heap within the critical section. 
- The caveat here is that the execution thread will need to be woken up to recalculate the minimum duration it would sleep for before an action is due for execution. 
- An action with an earlier due timestamp might have been added while the executor thread was sleeping on a duration calculated for an action due later than the one just added.

***Now let's come to the meat of our solution which is to design the execution thread's workflow.*** 

The thread will run the start() method and enter into a perpetual loop. The flow should be as follows:

- Initially the queue will be empty and the execution thread should just wait indefinitely on the condition variable to be notified.

- When the first callback arrives, we note how many seconds after its arrival does it need to be invoked and wait() on the condition variable for that many seconds. 
  This time we use a variant of the wait method that takes in the numbers of seconds to wait.

- Now two things are possible at this point. No new actions arrive, in which case the executor thread completes waiting and 
  polls the queue for tasks that should be executed and starts executing them.

- Or that another action arrives, in which case the consumer thread would signal the condition variable to wake up the execution thread and 
  have it re-evaluate the duration it can sleep for before the earliest callback becomes due.

Four actions are submitted for deferred execution. 
A to be executed after 3 seconds, B to be executed after 2 seconds, C to be executed after 1 second and finally D to be executed after 7 seconds. 
The output shows the execution of the actions in the order C, B, A and D.
