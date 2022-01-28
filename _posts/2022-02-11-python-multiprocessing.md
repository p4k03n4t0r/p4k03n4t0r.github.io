---
layout: post
title:  "Python Multiprocessing"
date:   2022-02-11
tags: []
---

_Intro_

## Multiprocessing vs multithreading

Not the same: 
multithreading: single process with multiple threads (Java)
multiprocessing: multiple processes spread out over CPU's (Python multiprocessing)

## Benchmark

Multiple use cases possible.
I wanted to leverage multiprocessing when I had to do a lot of git clones of bigger repo's. Takes a lot of time to do 1 by 1, but multiprocessing should make this easier.

To keep things comparable between different solutions, I just do a sleep for a certain amount of time. This also has the advantage that it can be tweaked easily to see the result of it for different solutions.

For the first test I'll do 10.000 times a sleep of 0.1 seconds, which should take a bit more than 1 hour and 40 minutes. The script looks as follows:
```python
import time

work_list = [0.1] * 10000

def do_something(w):
    time.sleep(w)

start = time.perf_counter()

primes = []
for work in work_list:
    do_something(work)

stop = time.perf_counter()

print(f"Took: {stop - start}s")
```

This takes 16 minutes and 40 seconds.

## Let's speed it up

Let's speed things up using multiprocessing:
```python
import time
import multiprocessing

work_list = [0.1] * 10000

def do_something(w):
    time.sleep(w)

start = time.perf_counter()

processes = []
for work in work_list:
    process = multiprocessing.Process(
        target=do_something,
        args=(work,),
    )
    processes.append(process)
    process.start()

for process in processes:
    process.join()

stop = time.perf_counter()

print(f"Took: {stop - start}s")
```

But when running this:
```zsh
➜  python3 calc1.py
Traceback (most recent call last):
  File "calc1.py", line 20, in <module>
  File "/usr/lib/python3.8/multiprocessing/process.py", line 121, in start
  File "/usr/lib/python3.8/multiprocessing/context.py", line 224, in _Popen
  File "/usr/lib/python3.8/multiprocessing/context.py", line 277, in _Popen
  File "/usr/lib/python3.8/multiprocessing/popen_fork.py", line 19, in __init__
  File "/usr/lib/python3.8/multiprocessing/popen_fork.py", line 69, in _launch
OSError: [Errno 24] Too many open files
```

Caused by file descriptor limit:
```
➜  ulimit -n
1024
```

Of course this can be increased, but at a certain point this will be a bottleneck. 

## Working with batches

Let's work in batches so we stay within the file descriptor limit:

```python
import time
import multiprocessing

# Should stay below result of 'ulimit -n'
MAX_PROCESS_COUNT = 1000

work_list = [0.1] * 10000

def do_something(w):
    time.sleep(w)

start = time.perf_counter()

processes = []

for i in range(0, len(work_list), MAX_PROCESS_COUNT):
    processes = []
    for j in range(0, MAX_PROCESS_COUNT):
        j = j + i

        if j >= len(work_list):
            continue

        process = multiprocessing.Process(
            target=do_something,
            args=(work_list[j],),
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

stop = time.perf_counter()

print(f"Took: {stop - start}s")
```

```zsh
➜  python3 calc2.py
Took: 8.508022800000617s
```
This takes just 8.5 seconds! That's a lot faster than the benchmark, actually 0.85% of the original time.

## Life is unpredictable

With the two previous scripts we did 10.000 sleeps of each 0.1 second. In the real world the work you want to do using multiprocessing can be very different. One time the function takes 0.1 second to execute, but another time it takes a few seconds. This is not ideal for the batch approach, because it's not using the CPU to it's fullest. 

Let's change the `work_list` array and also shuffle the content to prevent patterns:
```python
work_list = [0.1, 0.1, 0.1, 0.1, 5] * 2000
random.shuffle(work_list)
```

This will take a bit over 46 minutes and 40 seconds for the benchmark. The batch approach can also be updated using this:
```
➜  python3 calc2_2.py
Took: 60.810322900000756s
```

TODO: explain what happens

## Queue for the rescue

Always be busy
If a process finishes new work can be picked up from a queue:

```

```