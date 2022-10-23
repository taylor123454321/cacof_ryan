"""Program to test DC motor"""
#"""Servo library import"""
import pigpio
import time


#stepPIN = 27  # pin 13 on RPI GPIO27
#servoPIN = 17	GPIO17, pin 11

"""Init for GPIO for servo/tilt"""
print("Init GPIO start")
pi = pigpio.pi()



BIN1PIN = 19 # pin 35
BIN2PIN = 20 # pin 38
BPWMPIN = 21 # pin 40

pi.set_mode(BIN1PIN, pigpio.INPUT)
pi.set_mode(BIN2PIN, pigpio.INPUT)


pi.set_servo_pulsewidth(BPWMPIN, 0)

DC_PWM = GPIO.PWM(BPWMPIN, 50) 
# PWM with 50Hz
DC_PWM.start(6) # Initialisation


def rotate_set(direction, duty):
  if direction == 0:
    pi.write(BIN1PIN, 1)
    pi.write(BIN2PIN, 0)
    pi.set_servo_pulsewidth(BPWMPIN, duty)
  elif direction == 1:
    pi.write(BIN1PIN, 1)
    pi.write(BIN2PIN, 0)
    pi.set_servo_pulsewidth(BPWMPIN, duty)
  else:
    pi.write(BIN1PIN, 0)
    pi.write(BIN2PIN, 0)
    pi.set_servo_pulsewidth(BPWMPIN, 0)



delay = 2
try:
  while True:
    rotate_set(0, 30)
    time.sleep(delay)

    rotate_set(0, 60)
    time.sleep(delay)
    print("end")
except KeyboardInterrupt:
  DC_PWM.stop()
  GPIO.cleanup()



