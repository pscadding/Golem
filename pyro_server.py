# saved as greeting-server.py
import Pyro4
import RPi.GPIO as GPIO
import time

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
        GPIO.cleanup()

        self.move_foward()

    def move_foward(self, period=0.5):
        # Turn the right motor forwards
        GPIO.output(9, 0)
        GPIO.output(10, 1)

        # Turn the left motor forwards
        GPIO.output(7, 1)
        GPIO.output(8, 0)

        time.sleep(period)

        GPIO.cleanup()


Pyro4.Daemon.serveSimple({GolemController: "golem.controller"},
                         host = '192.168.0.66',
                         ns=True)