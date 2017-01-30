# saved as greeting-server.py
import Pyro4
import RPi.GPIO as GPIO
import time
import g_threading as thread

@Pyro4.expose
class WheelMatrix(object):
    __forwards = 0
    __backwards = 1
    _matrix = [0,0]

    def __init__(self, f, b):
        self._matrix = [0,0]
        self.forwards = f
        self.backwards = b

    @property
    def forwards(self):
        return self._matrix[self.__forwards]

    @forwards.setter
    def forwards(self, value):
        self.__set_wheel(value, self.__forwards)

    @property
    def backwards(self):
        return self._matrix[self.__backwards]

    @backwards.setter
    def backwards(self, value):
        self.__set_wheel(value, self.__backwards)

    def __set_wheel(self,value,index):
        assert type(value) is int
        assert value >= 0
        assert value <= 100
        self._matrix[index] = value

@Pyro4.expose
class WheelsMatrix(object):

    _leftWheelIndex = 0
    _rightWheelIndex = 1
    _matrix = [[0,0],[0,0]]

    def __init__(self, rf,rb,lf,lb):
        self._matrix = [[0,0],[0,0]]
        self.left_wheel = WheelMatrix(lf,lb)
        self.right_wheel = WheelMatrix(rf,rb)

    def __str__(self):
        return "<WheelsMatrix [[{0},{1}],[{2},{3}]]>".format(self.left_wheel.forwards,
                                                            self.left_wheel.backwards,
                                                            self.right_wheel.forwards,
                                                            self.right_wheel.backwards)

    def __repr__(self):
        return self.__str__()

    @property
    def left_wheel(self):
        return self._matrix[self._leftWheelIndex]

    @left_wheel.setter
    def left_wheel(self,value):
        self.__set_wheel(value, self._leftWheelIndex)

    @property
    def right_wheel(self):
        return self._matrix[self._rightWheelIndex]

    @right_wheel.setter
    def right_wheel(self, value):
        self.__set_wheel(value,self._rightWheelIndex)

    def __set_wheel(self,value,index):
        if type(value) is not WheelMatrix:
            assert type(value) is list
            assert len(value) == 2
            value = WheelMatrix(*value)
        self._matrix[index] = value

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