import queue
import threading
import time

def do_work(item):
    print("doing work",item)
    time.sleep(1)

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()

q = queue.PriorityQueue()

threads = []
for i in range(4):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in range(20):
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(4):
    q.put(None)
for t in threads:
    t.join()