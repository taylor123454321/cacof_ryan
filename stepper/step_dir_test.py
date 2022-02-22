"""Program to test step/dir stepper driver"""
"""Servo library import"""
import pigpio
import time

"""Init for GPIO for servo/tilt"""
print("Init GPIO start")
servoPIN = 27  # pin 13 on RPI
pi = pigpio.pi()
pi.set_mode(servoPIN, pigpio.INPUT)
print("Init GPIO finished")

pi.write(servoPIN, 1)
time.sleep(0.5)
pi.write(servoPIN, 0)
time.sleep(0.5)
pi.write(servoPIN, 1)
time.sleep(0.5)
pi.write(servoPIN, 0)
time.sleep(0.5)
pi.write(servoPIN, 1)
time.sleep(0.5)
pi.write(servoPIN, 0)
time.sleep(0.5)
pi.write(servoPIN, 1)
time.sleep(0.5)



