"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

for i in range(1):
    kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
    time.sleep(0.01)
    
kit.stepper1.release()