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
