# Rate Limiting Using Token Bucket Filter
## This problem and solution is from: https://www.educative.io/courses/python-concurrency-for-senior-engineering-interviews/JYRYE86v1Gl
### Probelm Description: 
Imagine you have a bucket that gets filled with tokens at the rate of 1 token per second. The bucket can hold a maximum of N tokens. Implement a thread-safe class that lets threads get a token when one is available. If no token is available, then the token-requesting threads should block.

The class should expose an API called get_token() that various threads can call to get a token.

### Solution:
It is certain that token generation is done at a fixed interval i:e in every 1sec. 
There should a thread to generate the token in every one second (Producer part), there should be threads which will consume tokens.
We need to remember the current number of tokens held by the token bucket filter object. We'll add an additional method daemonThread() 
that will be executed by the thread that adds a token every second to the bucket.

All the above logic is implemented in : RateLimitingUsingTokenBucketFilter.py file

#### Problem with the implementation defined in **RateLimitingUsingTokenBucketFilter.py** file:
The problem with the above solution is that we start our thread in the constructor. Generally, it is inadvisable 
***To start a thread in a constructor as the child thread can be passed the self variable which the child thread can use before the object pointed to by the passed-in 
self is fully constructed.***

There are two ways to overcome this problem, the naive but correct solution is to start the daemon thread outside of the MultithreadedTokenBucketFilter object. 
However, the con of this approach is that the management of the daemon thread spills outside the class. Ideally, we want the class to encapsulate all the operations 
related with the management of the token bucket filter and only expose the public API to the consumers of our class, as per good object orientated design. 
This situation is a great for using the Simple Factory design pattern. 
We'll create a factory class which produces token bucket filter objects and also starts the daemon thread only when the object is full constructed.

Implementation done in : **RateLimitingUsingTokenBucketFilterUsingFactory.py** 

