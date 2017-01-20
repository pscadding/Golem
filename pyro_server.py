# saved as greeting-server.py
import Pyro4
import RPi.GPIO as GPIO
import time
import queue
import threading


def worker():
    while True:
        items = motor_queue.get()
        if items is None:
            break
        items[0](items[1:])
        motor_queue.task_done()

motor_queue = queue.PriorityQueue()
threads = []
for i in range(1):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

@Pyro4.expose
class GolemController(object):

    def __init__(self):
        print("in init")

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Set the GPIO Pin mode
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(8, GPIO.OUT)
        GPIO.setup(9, GPIO.OUT)
        GPIO.setup(10, GPIO.OUT)

        # Turn all motors off
        GPIO.output(7, 0)
        GPIO.output(8, 0)
        GPIO.output(9, 0)
        GPIO.output(10, 0)

    def _stop(self):
        GPIO.output(9, 0)
        GPIO.output(10, 0)
        GPIO.output(7, 0)
        GPIO.output(8, 0)

    def _move_backwards(self, period=0.5):
        # Turn the right motor forwards
        GPIO.output(9, 1)
        GPIO.output(10, 0)

        # Turn the left motor forwards
        GPIO.output(7, 0)
        GPIO.output(8, 1)

        time.sleep(period)

        self.stop()

    def _move_fowards(self, period=0.5):
        # Turn the right motor forwards
        GPIO.output(9, 0)
        GPIO.output(10, 1)

        # Turn the left motor forwards
        GPIO.output(7, 1)
        GPIO.output(8, 0)

        time.sleep(period)

        self.stop()

    def move_forwards(self,period=0.5):
        motor_queue.put([self._move_fowards])
        motor_queue.join()


Pyro4.Daemon.serveSimple({GolemController(): "golem.controller"},
                         host = '192.168.0.66',
                         ns=True)