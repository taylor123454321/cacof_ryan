"""Program to turn turret in serach of a hot object and then to track"""
import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO

error_angle = 0

"""Init for GPIO for servo/tilt"""
servoPIN = 17  # pin 11 on RPI
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz

def stepper_spin(steps, direct): """Function to control stepper motor"""
    kit = MotorKit(i2c=board.I2C()) #Init stepper
    if direct <= 0:
        for i in range(steps):
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
            # time.sleep(0.01)
    else:
        for i in range(steps):
            kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
            # time.sleep(0.01)
    # time.sleep(4)
    kit.stepper1.release() #Close stepper or else it makes noise


def init():
    # Spin stepper
    print("Attempting stepper init spin")
    stepper_spin(50,0)
    # Tilt servo
    """time.sleep(2)
    print("Attempting servo init tilt")
    p.start(6.5)  # Initialization
    time.sleep(2)
    p.start(6)
    time.sleep(2)
    p.start(7)
    time.sleep(2)
    p.start(6.5)
    time.sleep(2)"""


def rotate_to_target(error):
    if error <= 0:  # forward
        direction = 0
    else:
        direction = 1  # backwards

    error = abs(error)
    if error > 10:
        error = 10
    print("Rotate error = {error}")

    if error > 2:
        stepper_spin(error, direction)
    else:
        print("Too small to rotate")


def tilt(error):
    MAX = 8
    CENTER = 5.5
    MIN = 4.5
    pixel_to_PWM_ratio = 10  # 0.1 PWM to 10 pixels guess

    print("Tilt error unaltered")
    print(error)
    error = pixel_to_PWM_ratio * error
    print("Tilt error altered")
    print(error)

    if error > 1:
        error = 1
        print("Error clipped high, {error}")
    elif error < -1:
        error = -1
        print("Error clipped low, {error}")

    if (CENTER + error) > MAX or (CENTER + error) < MIN:
        error = 0
        print("OUT OF BOUNDS TILT")

    if abs(error) > 0.2:
        p.ChangeDutyCycle(CENTER + error)
        time.sleep(0.1)
    else:
        print("Too small to tilt")


def rotate_idle():
    search_step = 400
    direction = 0
    stepper_spin(search_step, direction)


def check_found():
    check_d_bus = 0
    time.sleep(4)
    print("Searching, Read DBUS")
    return check_d_bus, 25, 8


try:
    init()
    while 1:
        status, error_hor_angle, error_vert_angle = check_found()

        if status == 0:
            rotate_idle()
        else:
            rotate_to_target(error_hor_angle)
            tilt(error_vert_angle)
except KeyboardInterrupt:
    p.start(6.5)
    p.stop()
    GPIO.cleanup()
    # kit.stepper1.release()
