#!/usr/bin/env python3

# Take in a single optional integral argument
import sys
import time
"""Servo library import"""
import pigpio

DBUS_NAME = "org.cacophony.thermalrecorder"
DBUS_PATH = "/org/cacophony/thermalrecorder"
# Create a reference to the RandomData object on the  session bus
from gi.repository import GLib

import dbus
import dbus.mainloop.glib

print("Init GPIO start")
pi = pigpio.pi()
"""Init for PIGPIO for stepper driver"""
stepPIN = 27  # pin 13 on RPI
dirPIN = 22  # pin 15 on RPI
enablePIN = 23  # pin 16 on RPI
pi.set_mode(stepPIN, pigpio.INPUT)
pi.set_mode(dirPIN, pigpio.INPUT)
pi.set_mode(enablePIN, pigpio.INPUT)

def handler(sender=None):
    print("got signal from %r" % sender)


def catchall_tracking_signals_handler(what, confidence, region, tracking):
    if what == 'false-positives':
        print(
            "Received a tracking signal and it says " + what,
            confidence,
            "% at ",
            region,
            " tracking?",
            tracking,
        )


def hello(steps):
    bit = 0
    pi.write(dirPIN, 0)  # CCW
    for i in range(steps):
        pi.write(stepPIN, bit)
        bit = 1 - bit  # Swap value from 1 to 0 to 1 etc
        time.sleep(0.005)  # 0.001 = 2RPM or 35s cycle time
    return True


if __name__ == "__main__":
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

    pi.write(enablePIN, 0)  # Enable stepper driver

    GLib.timeout_add(100, hello, 50)

    # GLib.timeout_add(1000, make_calls)


    loop.run()
