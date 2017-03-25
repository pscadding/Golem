import Pyro4
import sys
import os
import RPi.GPIO as GPIO
import time
import g_threading as thread

sys.path.append( os.path.dirname(os.path.dirname(__file__)))
from common.wheel_matrix import WheelsMatrix, WheelMatrix

@Pyro4.expose
class GolemController(object):
    mrf = 10
    mrb = 9
    mlf = 7
    mlb = 8

    frequency = 50

    common_matrices = {
        "forwards_fast": WheelsMatrix(100,0,100,0),
        "forwards_normal": WheelsMatrix(60, 0, 60, 0),
        "forwards_slow": WheelsMatrix(20, 0, 20, 0),
        "backwards_fast": WheelsMatrix(0, 100, 0, 100),
        "backwards_normal": WheelsMatrix(0, 60, 0, 60),
        "backwards_slow": WheelsMatrix(0, 20, 0, 20),
    }

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        t = WheelsMatrix(100,0,100,0)
        print(t)

        # Set the GPIO Pin mode
        GPIO.setup(self.mrf, GPIO.OUT)
        GPIO.setup(self.mrb, GPIO.OUT)
        GPIO.setup(self.mlf, GPIO.OUT)
        GPIO.setup(self.mlb, GPIO.OUT)

        self.pwmMRF = GPIO.PWM(self.mrf, self.frequency)
        self.pwmMRB = GPIO.PWM(self.mrb, self.frequency)
        self.pwmMLF = GPIO.PWM(self.mlf, self.frequency)
        self.pwmMLB = GPIO.PWM(self.mlb, self.frequency)


        self.pwmMRF.start(0)
        self.pwmMRB.start(0)
        self.pwmMLF.start(0)
        self.pwmMLB.start(0)

        # Turn all motors off
        self._stop()

    @property
    def stop_matrix(self):
        return WheelsMatrix(0,0,0,0)

    def _stop(self):
        self._move(self.stop_matrix)

    def _move(self, matrix):
        self.pwmMRF.ChangeDutyCycle(matrix.right_wheel.forwards)
        self.pwmMRB.ChangeDutyCycle(matrix.right_wheel.backwards)
        self.pwmMLF.ChangeDutyCycle(matrix.left_wheel.forwards)
        self.pwmMLB.ChangeDutyCycle(matrix.left_wheel.backwards)

    def _move_period(self,matrix, period):
        self._move(matrix)
        time.sleep(period)
        self._move(self.stop_matrix)

    def move(self,rf,rb,lf,lb):
        self._move(WheelsMatrix(rf,rb,lf,lb))

    def move_backwards(self,period=0.5,speed="fast"):
        m = self.common_matrices['backwards_' + speed]
        thread.motor_queue.put([self._move_period, m, period])

    def move_forwards(self,period=0.5,speed="fast"):
        m = self.common_matrices['forwards_'+speed]
        thread.motor_queue.put([self._move_period, m, period])

    def move_left(self,period=0.5,speed="fast"):
        m = self.common_matrices['forwards_' + speed]
        thread.motor_queue.put([self._move_period, m, period])

    def move_right(self,period=0.5,speed="fast"):
        m = self.common_matrices['forwards_' + speed]
        thread.motor_queue.put([self._move_period, m, period])

    def stop(self):
        thread.motor_queue.put([self._stop])

Pyro4.Daemon.serveSimple({GolemController(): "golem.controller"},
                         host = '192.168.0.66',
                         ns=True)