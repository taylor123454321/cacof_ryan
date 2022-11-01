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

pi.set_mode(BIN1PIN, pigpio.OUTPUT)
pi.set_mode(BIN2PIN, pigpio.OUTPUT)

'''12 PWM channel 0 All models but A and B
13 PWM channel 1 All models but A and B
18 PWM channel 0 All models
19 PWM channel 1 All models but A and B'''

#pi.hardware_PWM(18, 800, 250000) # 800Hz 25% dutycycle

#pi.set_servo_pulsewidth(BPWMPIN, 0)
#DC_PWM = GPIO.PWM(BPWMPIN, 50)
# PWM with 50Hz
#DC_PWM.start(6) # Initialisation


def rotate_set(direction, duty):
  print("Rotating... ")
  if direction == 0:
    print("Right")
    pi.write(BIN1PIN, 1)
    pi.write(BIN2PIN, 0)
    pi.hardware_PWM(18, 800, duty*100000)
  elif direction == 1:
    print("Left")
    pi.write(BIN1PIN, 0)
    pi.write(BIN2PIN, 1)
    pi.hardware_PWM(18, 800, duty*100000)
  else:
    print("Stopped")
    pi.write(BIN1PIN, 0)
    pi.write(BIN2PIN, 0)
    pi.hardware_PWM(18, 800, 0)



delay = 2
try:
  while True:
    rotate_set(0, 30)
    time.sleep(delay)

    rotate_set(0, 60)
    time.sleep(delay)

    rotate_set(2, 0)
    time.sleep(delay)
    print("end")
except KeyboardInterrupt:
  DC_PWM.stop()
  GPIO.cleanup()
  print("EXIT")



