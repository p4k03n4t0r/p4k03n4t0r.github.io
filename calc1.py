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
