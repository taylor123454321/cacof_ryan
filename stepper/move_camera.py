"""Program to turn turret in serach of a hot object and then to track"""
import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO

"""Init for stepper motor"""
kit = MotorKit(i2c=board.I2C())
error_angle = 0

"""Init for GPIO for servo/tilt"""
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz


def init():
    #Spin stepper
    print("Attempting stepper init spin")
    for i in range(50):
        kit.stepper1.onestep(direction, style=stepper.MICROSTEP)
        time.sleep(0.01)
    #Tilt servo
    print("Attempting servo init tilt")
    p.start(6)  # Initialization
    time.sleep(0.5)
    p.start(4)
    time.sleep(0.5)
    p.start(8)
    time.sleep(0.5)
    p.start(6)
    time.sleep(0.5)


def rotate(error):
    if error <= 0:
        direction = stepper.BACKWARD
    else:
        direction = stepper.FORWARD

    error = abs(error)
    if error > 10:
        error = 10
    print(error)

    if error > 2:
        for i in range(error):
            kit.stepper1.onestep(direction, style=stepper.MICROSTEP)
            time.sleep(0.01)
    else:
        print("Too small to rotate")


def tilt(error):
    MAX = 7
    CENTER = 5
    MIN = 3
    pixel_to_PWM_ratio = 10 #0.1 PWM to 10 pixels guess

    print("Tilt error unaltered")
    print(error)
    error = pixel_to_PWM_ratio*error
    print("Tilt error altered")
    print(error)

    if error > 1:
        error = 1
        print("Error clipped high")
        print(error)
    elif error < -1:
        error = -1
        print("Error clipped low")
        print(error)

    if (CENTER + error) > MAX or (CENTER + error) < MIN:
        error = 0
        print("OUT OF BOUNDS TILT")

    if abs(error) > 0.2:
        p.ChangeDutyCycle(CENTER + error)
        time.sleep(0.1)
    else:
        print("Too small to tilt")


def rotate_idle():
    search_step = 20
    for i in range(search_step):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
        time.sleep(0.01)
    time.sleep(0.2)
    print("Searching")


def check_found():
    check_d_bus = 0
    return check_d_bus, 25, 8


try:
    init()
    while 1:
        status, error_hor_angle, error_vert_angle = check_found()

        if status == 0:
            rotate_idle()
        else:
            rotate(error_hor_angle)
            tilt(error_vert_angle)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    kit.stepper1.release()