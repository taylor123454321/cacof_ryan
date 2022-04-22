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

what_thing = "init_empty"
status = 0  # 0 is if no pest found, 1 if pest is found
region_global = [0]*4  # Array for centroid of pest


def catchall_tracking_signals_handler(what, confidence, region, track):
    print(
        "What," + what,
        confidence,
        "% at ",
        region[0], region[1], region[2], region[3],
        " track",
        track,
    )
    global what_thing
    global status
    global region_global
    what_thing = str(what)
    status = track
    region_global = region

    if track == 0:
        status = 0
        region_global = [0]*4



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


f = open(str(time.strftime('%Y-%m-%d_%H.%M.%S_Turret1')) + ".txt", "w")


if __name__ == "__main__":
    tracking = TrackingService(catchall_tracking_signals_handler)

    # just to keep program alive
    # replace with your code
    while tracking.t.is_alive():
        try:
            
            # f = open("~/home/pi/Documents/logs/" + str(time.strftime('%Y-%m-%d_%H_Turret1')) + ".txt", "w")
            #  f = open("D:\\myfiles\welcome.txt", "r")
            count = 0
            while 1:
                if status == 1:
                    print("Status = ", status, "Count = ", count)
                    if count <= 0:
                        f.write(str(time.strftime('%Y-%m-%d_%H.%M.%S_Turret1\n')))
                        count = 5
                    else:
                        count = count - 1
                    print(count)
                    f.write("What, " + what_thing + " Here, " + str(region_global[0]) + str(region_global[1]) + str(region_global[2]) + str(region_global[3]) + "\n")
                time.sleep(1)
                print("Slept")

        except KeyboardInterrupt:
            f.close()
            break

