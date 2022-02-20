"""Program to turn turret in search of a hot object and then to track"""
print("Imports started")
import time
import board

"""Stepper motor library import"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit 

"""Servo library import"""
import pigpio

"""OpenCV library import"""
import cv2
import numpy as np


"""Import for DBUS"""
# Take in a single optional integral argument
import sys

DBUS_NAME = "org.cacophony.thermalrecorder"
DBUS_PATH = "/org/cacophony/thermalrecorder"
# Create a reference to the RandomData object on the  session bus
from gi.repository import GLib

import dbus
import dbus.mainloop.glib

print("Imports finished")

error_angle = 0

MIN_PW = 1100
MID_PW = 1300
MAX_PW = 1500

status = 0  # 0 is if no pest found, 1 if pest is found
region_global = [0]*4 # Array for centroid of pest


"""Init for GPIO for servo/tilt"""
print("Init GPIO start")
servoPIN = 17  # pin 11 on RPI
pi = pigpio.pi()
pulsewidth = MID_PW
pi.set_servo_pulsewidth(servoPIN, pulsewidth)
print("Init GPIO finished")

"""OpenCV init camera"""
# Create a VideoCapture object
print("Init camera start")
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if cap.isOpened() == False:
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

print("Init camera finished")

"""DBUS init"""
print("Init dbus start")
def handler(sender=None):
    print("got signal from %r" % sender)


def catchall_tracking_signals_handler(what, confidence, region, tracking):
    print(
        "Received a trackng signal," + what,
        confidence,
        "% at ",
        region,
        " tracking?",
        tracking,
    )
    status = tracking
    region_global = region
    
    
    
global object
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
loop = GLib.MainLoop()
try:
    bus = dbus.SystemBus()
    object = bus.get_object(DBUS_NAME, DBUS_PATH)
except dbus.exceptions.DBusException as e:
    print("Failed to initialize D-Bus object: '%s'" % str(e))
    sys.exit(2)

bus.add_signal_receiver(
    catchall_tracking_signals_handler,
    dbus_interface=DBUS_NAME,
    signal_name="Tracking",
    )
print("Init dbus finishsed")


def stepper_spin(steps, direct):  # Function to control stepper motor
    kit = MotorKit(i2c=board.I2C())  # Init stepper
    if direct <= 0:
        for i in range(steps):
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
            # time.sleep(0.01)
    else:
        for i in range(steps):
            kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
            # time.sleep(0.01)
    # time.sleep(4)
    kit.stepper1.release()  # Close stepper or else it makes noise


def init():
    # Spin stepper
    print("Attempting stepper init spin")
    stepper_spin(50, 0)
    # Tilt servo
    time.sleep(2)
    print("Attempting servo init tilt")
    pi.set_servo_pulsewidth(servoPIN, MID_PW)
    time.sleep(2)
    pi.set_servo_pulsewidth(servoPIN, MIN_PW)
    time.sleep(2)
    pi.set_servo_pulsewidth(servoPIN, MAX_PW)
    time.sleep(2)
    pi.set_servo_pulsewidth(servoPIN, MID_PW)
    time.sleep(2)


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
    max = 8
    center = 5.5
    min = 4.5
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

    if (center + error) > max or (center + error) < min:
        error = 0
        print("OUT OF BOUNDS TILT")

    if abs(error) > 0.2:
        p.ChangeDutyCycle(center + error)
        time.sleep(0.1)
    else:
        print("Too small to tilt")


def rotate_idle():
    search_step = 400  # 10 terns = half rotation, 2 turns = 11s
    direction = 0  # Camera overlap
    stepper_spin(search_step, direction)


def calculate_error(region):
    # region = [x1,y1,x2,y2]
    error_hor = 20
    # error_vert = 0

    return error_hor  # , error_vert


def record_video(out):
    ret, frame = cap.read()
    if ret:
        # Write the frame into the file 'output.avi'
        out.write(frame)
        print("Recording video")


def get_video_output(out=None):
    #Specify the path and name of the video file as well as the encoding, fps and resolution
    if out:
        out.release()
    return cv2.VideoWriter('test ' + str(time.strftime('%d_%m_%Y_%H_%M_%S')) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))


try:
    init()
    new_video_out_object = 0
    out = get_video_output()

    while 1:
        print(status)
        #status = 0

        if status == 0:
            #rotate_idle()
            new_video_out_object_needed = 1
            print("Rotating idle, looking for target")
        else:  # Pest has been found, aim at target and record video
            #error_hor_angle, error_vert_angle = calculate_horizontal_error(region_global)
            # error_vert_angle = 0
            #rotate_to_target(error_hor_angle)
            # tilt(error_vert_angle)
            if new_video_out_object_needed == 1:
                out = get_video_output(out)
                new_video_out_object_needed = 0
            record_video(out)
            print("Target found")
except KeyboardInterrupt:
    pi.stop()
    cap.release()
    out.release()
    # kit.stepper1.release()