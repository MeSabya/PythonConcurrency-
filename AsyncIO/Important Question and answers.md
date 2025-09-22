## In asyncio, what is the difference between:

```python
asyncio.run(main())
loop.run_until_complete(main())
```
When would you prefer one over the other?
What happens if you call asyncio.run() from inside an already running loop?

<details>

### 1. asyncio.run(main())

- Introduced in Python 3.7 as the high-level entry point for asyncio programs.

What it does under the hood:

- Creates a new event loop.
- Runs your coroutine (main()) until completion.
- Closes the loop when done.
- Cleans up pending tasks and cancels background coroutines.
- It is intended as the "main entry point" of your async program, usually at the top-level script.

👉 Example:

```python
import asyncio

async def main():
    print("Hello asyncio.run")

asyncio.run(main())
```

### 2. loop.run_until_complete(main())

- Lower-level API, available since the early versions of asyncio.
- Requires you to manually create or get an event loop.
- Does not close the loop automatically; you need to manage loop lifecycle yourself.

More flexible when you want:

- Reuse the loop.
- Run multiple coroutines sequentially.
- Integrate with other event-loop frameworks (Twisted, uvloop, GUI loops).

👉 Example:

```python
import asyncio

async def main():
    print("Hello run_until_complete")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()  # you must close it yourself
```

### What happens if you call asyncio.run() from inside an already running loop?

⚠️ This is important:

- asyncio.run() creates a new event loop.
- But Python does not allow nested event loops.
- If you call it while another loop is already running (e.g., inside Jupyter Notebook, or from within an async function), you get:
- RuntimeError: asyncio.run() cannot be called from a running event loop

</details>

## Why loop.run_until_complete() exists ? Why it is needed?

<details>
### 1. Embedding asyncio in environments that already have an event loop
- Some applications already run an event loop (e.g., GUI frameworks like Qt, Tkinter, or event-driven libraries).
- If you use asyncio.run(), it tries to create and manage its own loop, which conflicts with the existing loop.

### 2. Running multiple coroutines step by step

With run_until_complete() you can reuse the same loop across multiple runs.

This allows sequential execution of coroutines without tearing down and recreating loops each time.

👉 Example:

```python
import asyncio

async def task(n):
    await asyncio.sleep(1)
    return f"done {n}"

loop = asyncio.get_event_loop()
print(loop.run_until_complete(task(1)))
print(loop.run_until_complete(task(2)))
```
### 3. Inside frameworks or libraries

If you’re writing a library, you don’t want to call asyncio.run() because it:

- Creates a new loop
- Closes it when done

That would conflict with the application’s loop.

</details>

## What’s the difference between:

```python
await coro()
task = asyncio.create_task(coro())
```

When should you wrap in create_task?
What happens if a create_task is never awaited?

<details>

### await coro()

- Runs the coroutine to completion, right now.
- The caller is suspended until coro() finishes.
- The result (or exception) is returned directly.
- 👉 Think: “call this coroutine and wait for its answer.”

```python
async def foo():
    await asyncio.sleep(1)
    return "foo done"

async def main():
    result = await foo()   # pauses here until foo() finishes
    print(result)
```

prints "foo done" after 1s

### task = asyncio.create_task(coro())

- Schedules coro() to run in the background, concurrently with whatever else the event loop is doing.
- Returns a Task object immediately — you can await it later or cancel it.
- The task starts running right away, even if you don’t await it immediately.
- 👉 Think: “kick this coroutine off in the background.”

```python
async def foo():
    await asyncio.sleep(1)
    return "foo done"

async def main():
    task = asyncio.create_task(foo())  # foo starts running now
    print("main continues immediately")
    result = await task                # wait for foo when we need it
    print(result)

# prints:
# main continues immediately
# foo done
```

</details>

## Cancellation Propagation

Suppose you cancel a task via task.cancel().
How does cancellation propagate to awaited sub-coroutines?
What exception is raised inside the coroutine?
How can you make sure cleanup code (e.g., closing DB connections) runs?

## Concurrency Limits

How do you limit concurrency of async tasks (e.g., at most N HTTP requests at a time)?
Discuss patterns: asyncio.Semaphore, worker pools, asyncio.BoundedSemaphore.

<details>

### Using asyncio.Semaphore

- A Semaphore maintains a counter representing “available slots”.
- You acquire before starting a task, and release when done.
- Only up to N tasks can acquire the semaphore at the same time.

Example:

```python
import asyncio
import random

async def fetch(url, sem):
    async with sem:  # acquire semaphore
        print(f"Fetching {url}")
        await asyncio.sleep(random.random() * 2)  # simulate I/O
        print(f"Done {url}")

async def main():
    urls = [f"url{i}" for i in range(10)]
    sem = asyncio.Semaphore(3)  # allow at most 3 concurrent fetches
    tasks = [asyncio.create_task(fetch(url, sem)) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### Worker pool pattern

Instead of semaphores, another pattern is a worker pool:

Create a fixed number of worker coroutines (N workers).

Each worker consumes tasks from a shared asyncio.Queue.

Ensures at most N tasks run concurrently.

Example:

```python
import asyncio
import random

async def worker(name, queue):
    while True:
        url = await queue.get()
        if url is None:
            break  # sentinel to exit
        print(f"{name} fetching {url}")
        await asyncio.sleep(random.random() * 2)
        print(f"{name} done {url}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    urls = [f"url{i}" for i in range(10)]
    for url in urls:
        await queue.put(url)
    
    # start 3 workers
    workers = [asyncio.create_task(worker(f"worker{i}", queue)) for i in range(3)]
    
    await queue.join()  # wait until all tasks are processed
    
    # send sentinel None to stop workers
    for _ in workers:
        await queue.put(None)
    await asyncio.gather(*workers)

asyncio.run(main())
```

</details>

## Mixing Threads & Asyncio

How do you safely call a blocking function (e.g., CPU-heavy compression) inside asyncio?

Compare:

```python
await loop.run_in_executor(None, blocking_func)
asyncio.to_thread(blocking_func)
```

<details>

### Using asyncio.to_thread (Python 3.9+)

Convenience wrapper around run_in_executor for threads.

```python
import asyncio
import time

def cpu_heavy(x):
    time.sleep(2)
    return x * 2

async def main():
    result = await asyncio.to_thread(cpu_heavy, 10)
    print(result)

asyncio.run(main())

```

</details>
