#!/usr/bin/env python3

# Take in a single optional integral argument
import sys
import time

DBUS_NAME = "org.cacophony.thermalrecorder"
DBUS_PATH = "/org/cacophony/thermalrecorder"
# Create a reference to the RandomData object on the  session bus
from gi.repository import GLib

import dbus
import dbus.mainloop.glib


def catchall_tracking_signals_handler(what, confidence, region, tracking):
    print(
        "Received a trackng signal and it says " + what,
        confidence,
        "% at ",
        region,
        " tracking?",
        tracking,
    )


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
count = 0
while(1):
    count += 1
    print(count)
    time.sleep(1)