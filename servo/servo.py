import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(6) # Initialization


delay = 2
try:
  while True:
    p.ChangeDutyCycle(5)
    time.sleep(delay)

    #p.ChangeDutyCycle(12)
    #time.sleep(delay)
    print("end")
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
