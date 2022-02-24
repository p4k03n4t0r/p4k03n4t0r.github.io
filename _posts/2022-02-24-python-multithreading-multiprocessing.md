---
layout: post
title:  "Python Multithreading and Multiprocessing"
date:   2022-02-24
tags: []
---

_During technical interviews for a job I have often been asked what multithreading is. I could often explain what it does, but explaining how it works was a different piece of cake. When doing Python I even found out there's besides multithreading also multiprocessing, now I was completely lost. It took me some time to understand what made them different and also how and when to apply them. Still there's much more to learn about it, but right now I think I understand the basics of it. 

## What are threads and processes?

Although programming languages may look very different, under the hood they often use similar components. This is also the case for the use of threads and processes. Actually every program that is run in Linux, for example a Java JAR, Python script or even a simple `ls`, is a process. This is easy to find out using [ps](https://man7.org/linux/man-pages/man1/ps.1.html):

```zsh
➜  cat main.py
import time
time.sleep(1000)
➜  python3 main.py 
# Meanwhile in a different terminal
➜  ps -aux | grep python3
paul      8104  0.0  0.0  15824  8964 pts/4    S+   19:37   0:00 python3 main.py
```

Each process consists of one or more threads, where all threads share the same resources like memory. Let's take a look at the thread(s) of the above application:

```zsh
➜  python3 main.py 
# Meanwhile in a different terminal
➜  ps -aux | grep python3
paul      8972  0.2  0.0  15824  8956 pts/4    S+   20:06   0:00 python3 main.py
➜  ps -T -p 8972
  PID  SPID TTY          TIME CMD
 8972  8972 pts/4    00:00:00 python3
```

The Python process contains a single thread, which is expected since we don't create any new threads besides the main thread within the program. 


## Multithreading in Python

While programming languages are often powerful, there's a lot of scenarios where a single threaded program won't work. For example when you want to create a webserver you want to process multiple requests at the same time. It won't be possible to process a request while also listening for new requests. For this use case multithreading would be ideal, where one thread can listen for new requests while the handling of received requests can be done in their own thread. Although the process can only execute a single instruction of each thread at the same time, by switching quickly between the different threads it can still run all of them. On the outside it looks like the process runs the threads at the same time. 

Let's look at a simple multithreading example in Python:
```zsh
➜  cat main.py
from threading import Thread
from time import sleep

threads = []
for i in range(0, 4):
    threads.append(Thread(target=sleep, args=(1000,)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
➜  python3 main.py
# Meanwhile in a different terminal
➜  ps -aux | grep python3
paul      9259  0.1  0.0 311008 11012 pts/5    Sl+  20:17   0:00 python3 main.py
➜  ps -T -p 9259
  PID  SPID TTY          TIME CMD
 9259  9259 pts/5    00:00:00 python3
 9259  9260 pts/5    00:00:00 python3
 9259  9261 pts/5    00:00:00 python3
 9259  9262 pts/5    00:00:00 python3
 9259  9263 pts/5    00:00:00 python3
```

The program spawns four new threads, which can do their own work while they are not being blocked by each other. One interesting thing to note is that with spawning four threads, the process consists of five threads. Don't forget the main thread that started it all!

Multithreading is often used to speed up performance in Python, let's give it a try:

```python
from threading import Thread
from time import perf_counter
import sys

if len(sys.argv) > 1 and sys.argv[1] == "multithreading":
    multithreading = True
else:
    multithreading = False
print(f"Multithreading enabled: {multithreading}")
LOOPS = int(sys.argv[2])
WORK = int(sys.argv[3])

def work():
    c = 0
    for i in range(0, WORK):
        c = c + 1

start = perf_counter()

if multithreading:
    threads = []
    for i in range(0, LOOPS):
        threads.append(Thread(target=work))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
else:
    for i in range(0, LOOPS):
        work()

stop = perf_counter()

print(f"Elapsed {stop-start}s")
```

```zsh
➜  python3 main.py singlethread 100 1000000       
Multithreading enabled: False
Elapsed 2.2430462000011175s
➜  python3 main.py multithreading 100 1000000
Multithreading enabled: True
Elapsed 2.294595200000913s
```

This is interesting! The promise was that multithreading would make the program faster, but in this case it still takes about the same time to run. So why is this? The answer is the Python GIL: [Global Interpreter Lock](https://realpython.com/python-gil/). The GIL only allows a single thread within the Python process to execute an instruction. This means that although there are multiple threads, they'll have to wait till they get 'control' to run an instruction. In the above program the same amount of instructions is executed for both programs, with the only difference being that the multithreaded process can run different work (threads) at the same time instead of one by one.

Still multithreading is not something bad and with the above example it would still be possible to create a non-blocking webserver, which wouldn't be possible in a single thread Python program. In a lot of other languages, like Java, the multithreading approach in the above example would be faster. For Python a process can only run on a single CPU core, while a Java process can run on multiple CPU cores. This allows it to actually run threads in parallel, because each core can execute instructions indepedent of each other.

## Multiprocessing in Python

Although there are [talks about removing the GIL](https://lukasz.langa.pl/5d044f91-49c1-4170-aed1-62b6763e6ad0/), it's not something which can be easily changed within Python. Luckily there's still another way to speed up things in Python. Before taking a look at this, it's necessary to dive a bit deeper in processes first. In Linux, processes are all actually part of a tree. This can be sees by looking at the Python process spawned earlier:
 
```zsh
➜  python3 main.py 
# Meanwhile in a different terminal
➜  ps -aux --forest
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0    900   504 ?        Sl   19:14   0:00 /init
root         9  0.0  0.0    892    80 ?        Ss   19:14   0:00 /init
root        10  0.0  0.0    892    80 ?        S    19:14   0:00  \_ /init
paul        11  0.0  0.0  16556  8184 pts/0    Ss   19:14   0:01      \_ -zsh
paul     12760  0.0  0.0  10856  3316 pts/0    R+   21:26   0:00          \_ ps -aux --forest
root      8400  0.0  0.0    900    88 ?        Ss   19:43   0:00 /init
root      8401  0.0  0.0    900    88 ?        S    19:43   0:00  \_ /init
paul      8402  0.0  0.0  16672  8496 pts/5    Ss   19:43   0:00      \_ -zsh
paul     12632  0.0  0.0  15824  8968 pts/5    S+   21:25   0:00          \_ python3 main.py
```

The Python process is listed under the shell `zsh`, which is listed under the `/init` process. Besides this also the process `ps -aux` can be found, which is run to get the output. In Linux the root of all processes is the `/init` process, which is started with PID 1. Since I'm on running on WSL2 the tree might look a bit different from an actual Linux distro, but the tree structure is still visible. Linux uses the the [fork](https://man7.org/linux/man-pages/man2/fork.2.html) syscall to spawn new child processes, so you can actually say Linux uses multiprocessing to work. 

Since Python is not made for multithreading, it's best to use multiprocessing for parallelizing work. The orchestration is thus forwarded from the programming language to the operation system instead. This looks as follows:

```zsh
➜  cat main.py
from multiprocessing import Process
from time import sleep

processes = []
for i in range(0, 4):
    process = Process(target=sleep, args=(1000,))
    processes.append(process)
    process.start()

for process in processes:
    process.join()
➜  python3 main.py
# Meanwhile in a different terminal
➜  ps -aux --forest | grep python
paul     13883  0.0  0.0  17392 10836 pts/5    S+   21:44   0:00          \_ python3 main.py
paul     13884  0.0  0.0  17392  9036 pts/5    S+   21:44   0:00              \_ python3 main.py
paul     13885  0.0  0.0  17392  9036 pts/5    S+   21:44   0:00              \_ python3 main.py
paul     13886  0.0  0.0  17392  9036 pts/5    S+   21:44   0:00              \_ python3 main.py
paul     13887  0.0  0.0  17392  9036 pts/5    S+   21:44   0:00              \_ python3 main.py
```

Under the hood [the main process will use fork](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods) to spawn child processes. Since this system has multiple CPU cores, the process can be processed in real parallel. This should be able to beat the single threaded program:

```python
from multiprocessing import Process
from time import perf_counter
import sys

if len(sys.argv) > 1 and sys.argv[1] == "multiprocessing":
    multiprocessing = True
else:
    multiprocessing = False
print(f"Multiprocessing enabled: {multiprocessing}")
LOOPS = int(sys.argv[2])
WORK = int(sys.argv[3])

def work():
    c = 0
    for i in range(0, WORK):
        c = c + 1

start = perf_counter()

if multiprocessing:
    processes = []
    for i in range(0, LOOPS):
        process = Process(
            target=work,
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
else:
    for i in range(0, LOOPS):
        work()

stop = perf_counter()

print(f"Elapsed {stop-start}s")
```

```zsh
➜  python3 main.py singleprocess 100 1000000  
Multiprocessing enabled: False
Elapsed 2.273627000000488s
➜  python3 main.py multiprocessing 100 1000000
Multiprocessing enabled: True
Elapsed 0.44913179999821295s
```

Yes, that's much faster since we can use multiple cores. To check the amount of cores that can be utilized, `lscpu` can be run. Technically this means that the more CPU cores there are, the more work can be done in parallel. Although probably something else would become the bottleneck like the sockets or open file descriptors. Java can also do multiprocessing, but [this is not recommended](https://stackoverflow.com/questions/8001966/how-to-do-multiprocessing-in-java-and-what-speed-gains-to-expect). The reason is that every time a new process is created a new instance of the JVM has to be created, which takes a considerable time. 


## Considerations

Although running work in parallel would seem to always be faster, there's a few things to consider. For Python it's not necessary to start a new JVM instance in a new process, there's still some overhead when a new process is created. The more work is done, the more negligible this is. This can be seen by reducing the work to do per process in the above example:

```zsh
➜  python3 main.py singleprocess 1000 100   
Multiprocessing enabled: False
Elapsed 0.0017119000003731344s
➜  python3 main.py multiprocessing 1000 100
Multiprocessing enabled: True
Elapsed 0.4021673000006558s
```

Using multiprocessing it takes much longer due to the overhead of having to start a new process. 

Another thing to take into consideration is whether the parallel work has to have knowledge of each other. For example within the program a shared object must be updated and read by each thread/process. In this case multithreading is actually much easier than multiprocessing, since threads within the same process share the same memory. In Python the `global` keyword can be used to create a shared variable between threads.

## Pitfalls

The above examples are simple and might make multithreading and multiprocessing look easy, but from my experience things get complex quite quickly. There are some pitfalls to be aware off when working with these techniques. 

Within multithreading there is shared memory between threads, meaning different threads can write to the same variable in memory. This could lead to  programs acting different than expected. The GIL is actually also not threadsafe. An example can be found [here](https://verdagon.dev/blog/python-data-races). It shows a simple program shows how multiple threads write to the same variable, resulting in them overwriting the result of another thread. 

I thought multiprocessing is faster and more scalable than multithreading, so why wouldn't I always use this even for small programs? I quickly found out that sharing variables between processes is tricky. Since there is no shared memory between processes, the variable must be shared in another way. For this there are two options in the `multiprocessing` library, but they both have their downsides:

* [Shared ctypes objects](https://docs.python.org/3/library/multiprocessing.html#shared-ctypes-objects): _this returns a ctypes object allocated from shared memoryprocesses_. Unfortunately this is only limited to a single value or array of basic [ctypes](https://docs.python.org/3/library/ctypes.html#fundamental-data-types) (bool, byte, char, short, int, long, float, double).
* [Managers](https://docs.python.org/3/library/multiprocessing.html#managers): _provide a way to create data which can be shared between different processes, including sharing over a network between processes running on different machines. A manager object controls a server process which manages shared objects. Other processes can access the shared objects by using proxies._ The `Manager` class makes it easy to share any type of object you want between processes. It can even share it with other processes on the same or a different machine. This sounds too good to be true, and it is partially. In short the `Manager` costs a lot of overhead. It uses a socket to which it sends/retrieves data, which is considerably longer than writing/reading shared memory. 

## Conclusion

With this post I hope I covered the basics of multithreading and multiprocessing and showed some examples in Python to try it out yourself (which I would recommend). I wouldn't use multithreading in Python, since it's limited to a single CPU core and thus not scalable. Although sharing memory is easier than multiprocessing, the single CPU core is a hard limit while multiprocessing can still scale. So the uses cases for multithreading in Python are very limited and often not worth the effort. Still multiprocessing is not a silver bullet and if it's necessary to do a lot of reads/writes to shared objects I'm not sure or Python at all is the best fit. I myself did use multiprocessing successfully for different things, like scraping on the internet. I set it up in such a way that I didn't fully use all my CPU cores and could have scaled up the program more, but I hit the limit of my internet connection. 