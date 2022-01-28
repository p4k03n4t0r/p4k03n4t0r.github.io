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
