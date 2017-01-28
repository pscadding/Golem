# saved as greeting-server.py
import Pyro4
import enum
import RPi.GPIO as GPIO
import time
import g_threading as thread

class Instruction (enum.Enum):
    forwards = 1
    backwards = 2
    left = 3
    right = 4

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
        self._stop()

    def _stop(self):
        GPIO.output(9, 0)
        GPIO.output(10, 0)
        GPIO.output(7, 0)
        GPIO.output(8, 0)

    def _move(self, period, speed, instruction):
        if speed == "fast":
            self._move_direction(instruction)
            time.sleep(period)
        else:
            alt_speed = 0.01 if speed == "normal" else 0.03
            start_time = time.time()
            alt = False
            while time.time() - start_time < period:
                if alt:
                    self._move_direction(instruction)
                    time.sleep(0.01)
                else:
                    self._stop()
                    time.sleep(alt_speed)
                alt = not alt
        thread.motor_queue.put([self._stop])


    def _move_direction(self, instruction):
        if instruction == Instruction.backwards:
            # Turn the right motor backwards
            GPIO.output(9, 0)
            GPIO.output(10, 1)

            # Turn the left motor backwards
            GPIO.output(7, 1)
            GPIO.output(8, 0)

        elif instruction == Instruction.forwards:
            # Turn the right motor forwards
            GPIO.output(9, 0)
            GPIO.output(10, 1)

            # Turn the left motor forwards
            GPIO.output(7, 1)
            GPIO.output(8, 0)

        elif instruction == Instruction.left:
            # Turn the right motor forwards
            GPIO.output(9, 0)
            GPIO.output(10, 1)

        elif instruction == Instruction.right:
            # Turn the left motor forwards
            GPIO.output(7, 1)
            GPIO.output(8, 0)


    def move_backwards(self,period=0.5,speed="fast"):
        thread.motor_queue.put([self._move,period,speed,Instruction.backwards])

    def move_forwards(self,period=0.5,speed="fast"):
        thread.motor_queue.put([self._move,period,speed,Instruction.forwards])

    def move_left(self,period=0.5,speed="fast"):
        thread.motor_queue.put([self._move,period,speed,Instruction.left])

    def move_right(self,period=0.5,speed="fast"):
        thread.motor_queue.put([self._move,period,speed,Instruction.right])

    def stop(self):
        thread.motor_queue.put([self._stop])

Pyro4.Daemon.serveSimple({GolemController(): "golem.controller"},
                         host = '192.168.0.66',
                         ns=True)