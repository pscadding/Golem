import RPi.GPIO as GPIO
import time

time.sleep(2)

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set the GPIO Pin mode
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

# Turn all motors off
GPIO.output(7,0)
GPIO.output(8,0)
GPIO.output(9,0)
GPIO.output(10,0)

# Turn the right motor forwards
GPIO.output(9,0)
GPIO.output(10,1)

# Turn the left motor forwards
GPIO.output(7,1)
GPIO.output(8,0)

time.sleep(0.5)

GPIO.cleanup()