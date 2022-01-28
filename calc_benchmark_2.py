import time
import random

numbers = [0.1, 0.1, 0.1, 0.1, 1] * 2000
random.shuffle(numbers)


def do_something(n):
    time.sleep(n)


start = time.perf_counter()

primes = []
for number in numbers:
    do_something(number)

stop = time.perf_counter()

print(f"Took: {stop - start}s")
