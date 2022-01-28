import random
import time
import multiprocessing

# ulimit -n
MAX_PROCESS_COUNT = 1000

work_list = [0.1, 0.1, 0.1, 0.1, 5] * 2000
random.shuffle(work_list)


def do_something(w):
    time.sleep(w)


start = time.perf_counter()

work_queue = multiprocessing.Queue()
for work in work_list:
    work_queue.put(work)

processes = []
while not work_queue.empty() or len(processes) > 0:
    while len(processes) < MAX_PROCESS_COUNT and not work_queue.empty():
        process = multiprocessing.Process(
            target=do_something,
            args=(work_queue.get(),),
        )
        processes.append(process)
        process.start()

    finished_list = list(filter(lambda p: p.exitcode != None, processes))
    for process in finished_list:
        process.join()
        processes.remove(process)

stop = time.perf_counter()

print(f"Took: {stop - start}s")
