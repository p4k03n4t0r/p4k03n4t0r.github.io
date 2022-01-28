import random
import time
import multiprocessing
from multiprocessing.managers import BaseManager

# ulimit -n
MAX_PROCESS_COUNT = 10


# class MySharedClass:
#     def __init__(self):
#         self.d = {}

#     def add_id(self, id):
#         self.d[id] = id

#     def get(self):
#         return self.d


# def Manager():
#     m = BaseManager()
#     m.start()
#     return m


# BaseManager.register("Naam", MySharedClass)
# manager = Manager()
# print(manager.address)
# shared_value = manager.Naam()
# shared_value = multiprocessing.Value(type(MySharedClass))
SHARED_VALUE = multiprocessing.Array("i", 100)


def do_something(wq):
    if wq.empty():
        return None
    id = wq.get()
    # RETURN_DICT[id] = id
    # SHARED_VALUE.add_id(id)
    SHARED_VALUE[id] = id


start = time.perf_counter()

work_queue = multiprocessing.Queue()
for work in range(0, 100):
    work_queue.put(work)

# manager = multiprocessing.Manager()
# RETURN_DICT = manager.dict()
# print(manager.address)


processes = []
while not work_queue.empty() or len(processes) > 0:
    while len(processes) < MAX_PROCESS_COUNT and not work_queue.empty():
        process = multiprocessing.Process(
            target=do_something,
            args=(work_queue,),
        )
        processes.append(process)
        process.start()

    finished_list = list(filter(lambda p: p.exitcode != None, processes))
    for process in finished_list:
        r = process.join()
        processes.remove(process)

stop = time.perf_counter()
print(list(SHARED_VALUE))

# print(RETURN_DICT.values())
# print(len(RETURN_DICT.values()))

print(f"Took: {stop - start}s")
