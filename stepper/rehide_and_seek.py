#!/usr/bin/env python3

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

"""Init for PIGPIO for servo/tilt"""
print("Init GPIO start")
#servoPIN = 17  # pin 11 on RPI
pi = pigpio.pi()
"""pulsewidth = MID_PW
pi.set_servo_pulsewidth(servoPIN, pulsewidth)"""

"""Init for PIGPIO for stepper driver"""
stepPIN = 27  # pin 13 on RPI
dirPIN = 22  # pin 15 on RPI
enablePIN = 23  # pin 16 on RPI
pi.set_mode(stepPIN, pigpio.INPUT)
pi.set_mode(dirPIN, pigpio.INPUT)
pi.set_mode(enablePIN, pigpio.INPUT)


print("Init PIGPIO finished")


def catchall_tracking_signals_handler(what, confidence, region, tracking):
    print(
        "What = " + what,
        confidence,
        "% at ",
        region,
        " tracking?",
        tracking,
    )



# helper class to run dbus in background
class TrackingService:
    def __init__(self,callback):
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
        time.sleep(0.005)  # 0.001 = 2RPM or 35s cycle time


def stepper_spin(steps, direct):  # Function to control stepper motor
    if direct <= 0:
        pi.write(dirPIN, 0)  # CCW
        stepper_step(steps)
    else:
        pi.write(dirPIN, 1)  # CW
        stepper_step(steps)


def rotate_idle():
    search_step = 400
    direction = 0
    stepper_spin(search_step, direction)


if __name__ == "__main__":
    tracking = TrackingService(catchall_tracking_signals_handler)
    # just to keep program alive
    # replace with your code
    count = 1
    while tracking.t.is_alive():

        try:
            #init()
            # new_video_out_object_needed = 0
            # out = get_video_output()
            count = 0
            # total_time = time.time()
            # start_time = time.time()
            pi.write(enablePIN, 0)  # Enable stepper driver
            status = 0

            while 1:
                print(status, count)
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
                    rotate_idle()
                    #new_video_out_object_needed = 1
                    print("Rotating idle, looking for target")
                """else:  # Pest has been found, aim at target and record video
                    # error_hor_angle, error_vert_angle = calculate_horizontal_error(region_global)
                    # error_vert_angle = 0
                    # rotate_to_target(error_hor_angle)
                    # tilt(error_vert_angle)
                    if new_video_out_object_needed == 1:
                        #out = get_video_output(out)
                        new_video_out_object_needed = 0
                        #start_time = time.time()
                    #record_video(out)
                    print("Target found")

                    total_time = time.time() - start_time
                    if total_time >= 30:
                        new_video_out_object_needed = 1
                        start_time = time.time()
                        print("Max USB video time reached\nSet new video flag")"""
        except KeyboardInterrupt:
            pi.write(stepPIN, 0)
            pi.write(enablePIN, 1)
            pi.stop()
            tracking.quit()
            # cap.release()
            # out.release()
