import queue
import threading

def worker():
    while True:
        items = motor_queue.get()
        if items is None:
            break
        items[0](*items[1:])
        motor_queue.task_done()

motor_queue = queue.Queue()
threads = []
for i in range(1):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)