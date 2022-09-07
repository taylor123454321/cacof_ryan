import time
#time.sleep(300)

import numpy as np
import cv2
import os

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

# Set flag for only recoding at night
time_flag = False # True enables recording at any time

# Set video length in seconds
video_length = 20
#video_length = 120

path = r'video'
#path = r'../home/pi/Documents/video'
file_name = str(time.strftime('%Y-%m-%d_%H.%M.%S_Turret1.txt'))

# Creating a file at specified folder
# join directory and file path
with open(os.path.join(path, file_name), 'w') as fp:
    # uncomment below line if you want to create an empty file
    fp.write('Program started and wrote this line')

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Live tracking variables
status = 0  # 0 is if no pest found, 1 if pest is found


def get_video_output(out = None):
    #Specify the path and name of the video file as well as the encoding, fps and resolution
    if out:
        out.release()
    return cv2.VideoWriter('video/static_comp_IR_' + str(time.strftime('%Y-%m-%d_%H.%M.%S_Turret1')) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))
    #return cv2.VideoWriter('../home/pi/Documents/video/static_comp_IR_' + str(time.strftime('%Y-%m-%d_%H.%M.%S_Turret1')) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))


def catchall_tracking_signals_handler(what, confidence, region, tracking_status):
    global status
    status = tracking_status


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

if __name__ == "__main__":
    tracking = TrackingService(catchall_tracking_signals_handler)

    # just to keep program alive
    # replace with your code
    next_time = time.time() + video_length
    out = get_video_output()
    status = 0
    
    while tracking.t.is_alive():
        try:
            while True:
                if status == 1:
                    with open(os.path.join(path, file_name), 'a') as fp:
                        # uncomment below line if you want to create an empty file
                        fp.write('\nTracking started' + str(time.strftime('%Y-%m-%d_%H.%M.%S')))

                    hour = int(time.strftime('%H'))
                    # print(type(hour))
                    # print(hour)

                    if hour > 19 or hour < 6 or time_flag == True:
                        if time.time() > next_time:
                            next_time += video_length
                            out = get_video_output(out)
                            print("New video")

                        # Capture frame-by-frame
                        ret, frame = cap.read()
                        #print("status = ", status)
                        if ret:
                            out.write(frame)
        except KeyboardInterrupt:
            cap.release()
            cv2.destroyAllWindows()
            sys.exit("End of program")
