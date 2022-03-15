#!/usr/bin/env python3
print("Imports started")
# Take in a single optional integral argument
import sys

DBUS_NAME = "org.cacophony.thermalrecorder"
DBUS_PATH = "/org/cacophony/thermalrecorder"
# Create a reference to the RandomData object on the  session bus
from gi.repository import GLib

import dbus
import dbus.mainloop.glib
import time
import threading
import board

"""Servo/stepper library import"""
import pigpio

"""OpenCV library import"""
# import cv2
import numpy as np

print("Imports finished")

error_angle = 0

MIN_PW = 1100
MID_PW = 1300
MAX_PW = 1500

status = 0  # 0 is if no pest found, 1 if pest is found
region_global = [0]*4  # Array for centroid of pest


"""Init for PIGPIO for servo/tilt"""
print("Init GPIO start")
servoPIN = 17  # pin 11 on RPI
pi = pigpio.pi()
pulsewidth = MID_PW
pi.set_servo_pulsewidth(servoPIN, pulsewidth)

"""Init for PIGPIO for stepper driver"""
stepPIN = 27  # pin 13 on RPI
dirPIN = 22  # pin 15 on RPI
enablePIN = 23  # pin 16 on RPI
pi.set_mode(stepPIN, pigpio.INPUT)
pi.set_mode(dirPIN, pigpio.INPUT)
pi.set_mode(enablePIN, pigpio.INPUT)


print("Init PIGPIO finished")


def catchall_tracking_signals_handler(what, confidence, region, track):
    '''print(
        "What = " + what,
        confidence,
        "% at ",
        region[0], region[1], region[2], region[3],
        " track = ",
        track,
    )'''
    what = str(what)
    # print("string type = ", type(what))
    global status
    global region_global
    if what != 'false-positives':
        print(what, confidence)
        status = track
        region_global = region
    else:
        status = 0
        region_global = [0]*4

    if track == 0:
        status = 0
        region_global = [0]*4


class TrackingService:  # helper class to run dbus in background
    def __init__(self, callback):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.callback = callback
        self.loop = GLib.MainLoop()
        self.t = threading.Thread(
            target=self.run_server,
        )
        self.t.start()

    def quit(self):
        self.loop.quit()

    def run_server(self):
        try:
            bus = dbus.SystemBus()
            object = bus.get_object(DBUS_NAME, DBUS_PATH)
        except dbus.exceptions.DBusException as e:
            print("Failed to initialize D-Bus object: '%s'" % str(e))
            sys.exit(2)

        bus.add_signal_receiver(
            self.callback,
            dbus_interface=DBUS_NAME,
            signal_name="Tracking",
        )
        self.loop.run()


def stepper_step(steps):
    bit = 0
    for i in range(steps):
        pi.write(stepPIN, bit)
        bit = 1 - bit  # Swap value from 1 to 0 to 1 etc
        time.sleep(0.001)  # 0.001 = 2RPM or 35s cycle time


def stepper_spin(steps, direct):  # Function to control stepper motor
    print("stepper_spin. steps = ", steps, "dir = ", direct)
    if direct <= 0:
        pi.write(dirPIN, 0)  # CCW
        stepper_step(steps)
    else:
        pi.write(dirPIN, 1)  # CW
        stepper_step(steps)


def init():
    # Spin stepper
    time_delay = 1
    pi.write(enablePIN, 0)
    print("Attempting stepper init spin")
    stepper_spin(500, 0)
    time.sleep(time_delay)
    stepper_spin(500, 1)
    pi.write(enablePIN, 1)
    # time.sleep(time_delay)
    # Tilt servo
    time.sleep(time_delay)
    print("Attempting servo init tilt")
    pi.set_servo_pulsewidth(servoPIN, MID_PW)
    time.sleep(time_delay)
    pi.set_servo_pulsewidth(servoPIN, MIN_PW)
    time.sleep(time_delay)
    pi.set_servo_pulsewidth(servoPIN, MAX_PW)
    time.sleep(time_delay)
    pi.set_servo_pulsewidth(servoPIN, MID_PW)
    time.sleep(time_delay)


def rotate_to_target(error, error_last):
    k_proportional = 20
    """k_derivative = 1
    time_step = 0.5
    delta_error = error_last - error"""
    if error >= 0:  # if error is positive
        direction = 0  # CCW
    else:           # if error is negative
        direction = 1  # CW

    error = abs(error)
    error = k_proportional * error
    error = round(error)

    if error > 5:
        stepper_spin(error, direction)
    """else:
        print("Too small to rotate")"""


def tilt_to_target(error):
    k_proportional = 4  # 0.1 PWM to 10 pixels guess

    error = k_proportional * error

    """if error > 1:
        error = 1
        print("Error clipped high, {error}")
    elif error < -1:
        error = -1
        print("Error clipped low, {error}")"""

    if (MID_PW + error) > MAX_PW or (MID_PW + error) < MIN_PW:
        error = 0
        print("TILT OUT OF BOUNDS")

    if abs(error) > 5:
        pi.set_servo_pulsewidth(servoPIN, MID_PW + error)
        # time.sleep(0.1)
    else:
        print("Too small to tilt")


def rotate_idle():
    search_step = 400
    direction = 0
    stepper_spin(search_step, direction)
    pi.set_servo_pulsewidth(servoPIN, MID_PW)


def calculate_error(region):
    # region = [x1,y1,x2,y2]
    half_frame_width = 80  # 160 wide
    half_frame_height = 60  # 120 high
    print("avg = ", (region[0] + region[2])/2)
    error_hor = (half_frame_width - ((region[0] + region[2])/2))*1  # higher is right brackets
    # error_hor right is +, left is -
    error_vert = (half_frame_height - ((region[1] + region[3])/2))*1  # higher is up brackets
    # error_vert up is +, down is -
    print("hor = ", error_hor, "vert = ", error_vert)
    return error_hor, error_vert


if __name__ == "__main__":
    tracking = TrackingService(catchall_tracking_signals_handler)
    # just to keep program alive
    # replace with your code
    count = 1
    while tracking.t.is_alive():

        try:
            init()
            # new_video_out_object_needed = 0
            # out = get_video_output()
            count = 0
            # total_time = time.time()
            # start_time = time.time()
            pi.write(enablePIN, 0)  # Enable stepper driver
            status = 0
            error_hor_angle = 0
            error_hor_angle_last = 0
            error_vert_angle = 0

            while 1:
                # print(status, count)
                # status = 0
                count += 1
                """if count == 30:
                    status = 1
                    print(status)
                elif count == 500:
                    status = 0
                    print(status)
                elif count == 530:
                    status = 1
                    print(status)
                elif count == 700:
                    status = 0
                    print(status)"""

                if status == 0:
                    # rotate_idle()
                    # new_video_out_object_needed = 1
                    print("Rotating idle, looking for target")
                    time.sleep(1)
                else:  # Pest has been found, aim at target and record video
                    # print("Target found")
                    error_hor_angle, error_vert_angle = calculate_error(region_global)
                    rotate_to_target(error_hor_angle, error_hor_angle_last)
                    error_hor_angle_last = error_hor_angle
                    tilt_to_target(error_vert_angle)
                    time.sleep(0.5)
                    '''if new_video_out_object_needed == 1:
                        #out = get_video_output(out)
                        new_video_out_object_needed = 0
                        #start_time = time.time()
                    #record_video(out)
                    print("Target found")

                    total_time = time.time() - start_time
                    if total_time >= 30:
                        new_video_out_object_needed = 1
                        start_time = time.time()
                        print("Max USB video time reached\nSet new video flag")'''
        except KeyboardInterrupt:
            pi.write(stepPIN, 0)
            pi.write(enablePIN, 1)
            pi.stop()
            tracking.quit()
            # cap.release()
            # out.release()
