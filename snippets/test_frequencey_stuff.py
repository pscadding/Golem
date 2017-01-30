import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

mrf = 10
mrb = 9
mlf = 7
mlb = 8

f = 50
dc = 100
s = 0

GPIO.setup(mrf, GPIO.OUT)
GPIO.setup(mrb, GPIO.OUT)
GPIO.setup(mlf, GPIO.OUT)
GPIO.setup(mlb, GPIO.OUT)


pwmMRF = GPIO.PWM(mrf, f)
pwmMRB = GPIO.PWM(mrb, f)
pwmMLF = GPIO.PWM(mlf, f)
pwmMLB = GPIO.PWM(mlb, f)

pwmMRF.start(s)
pwmMRB.start(s)
pwmMLF.start(s)
pwmMLB.start(s)



def move(matrix):
    pwmMRF.ChangeDutyCycle(matrix[0])
    pwmMRB.ChangeDutyCycle(matrix[1])
    pwmMLF.ChangeDutyCycle(matrix[2])
    pwmMLB.ChangeDutyCycle(matrix[3])



move([80,0,80,0])

time.sleep(3)

move([0,0,0,0])