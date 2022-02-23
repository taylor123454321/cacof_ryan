"""Program to test step/dir stepper driver"""
"""Servo library import"""
import pigpio
import time

"""Init for GPIO for servo/tilt"""
print("Init GPIO start")
stepPIN = 27  # pin 13 on RPI
pi = pigpio.pi()
pi.set_mode(stepPIN, pigpio.INPUT)
print("Init GPIO finished")

pin_operator = 0
for i in range(100):
    if pin_operator == 1:
        pi.write(stepPIN, 1)
        print("High")
    else:
        pi.write(stepPIN, 0)
        print("Low")
    pin_operator = pin_operator * -1
    time.sleep(0.5)




