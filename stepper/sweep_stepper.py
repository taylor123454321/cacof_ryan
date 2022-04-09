"""Program to test step/dir stepper driver"""
"""Servo library import"""
import pigpio
import time

"""Init for GPIO for stepper"""
print("Init GPIO start")
pi = pigpio.pi()

"""Init for PIGPIO for stepper driver"""
stepPIN = 27  # pin 13 on RPI
dirPIN = 22  # pin 15 on RPI
enablePIN = 23  # pin 16 on RPI
pi.set_mode(stepPIN, pigpio.INPUT)
pi.set_mode(dirPIN, pigpio.INPUT)
pi.set_mode(enablePIN, pigpio.INPUT)
print("Init GPIO finished")


def stepper_step(steps):
    bit = 0
    pi.write(enablePIN, 0)  # Enable stepper driver
    for i in range(steps):
        pi.write(stepPIN, bit)
        bit = 1 - bit  # Swap value from 1 to 0 to 1 etc
        time.sleep(0.01)  # 0.001 = 2RPM or 35s cycle time


def stepper_spin(steps, direct):  # Function to control stepper motor
    # print("stepper_spin. steps = ", steps, "dir = ", direct)
    if direct <= 0:
        pi.write(dirPIN, 0)  # CCW
        stepper_step(steps)
    else:
        pi.write(dirPIN, 1)  # CW
        stepper_step(steps)


try:
    time.sleep(4)  # Initial delay for camera to start
    pi.write(enablePIN, 0)  # Enable stepper driver
    steps_for_sweep = 3000  # Enough steps for 30 degrees
    sweep_end_time = 2  # Time at the end of sweep
    #max_time = 60*30
    #start_time = time.time()
    while 1:
        stepper_spin(steps_for_sweep, 0)
        time.sleep(sweep_end_time)
        stepper_spin(steps_for_sweep, 1)
        time.sleep(sweep_end_time)
        print("Stepped")
        '''move_time = time.time() - start_time
        if move_time > max_time:
            print("End of time")
            break'''
except KeyboardInterrupt:
    pi.write(stepPIN, 0)
    pi.write(enablePIN, 1)
    pi.stop()


