import time
#time.sleep(30)

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

def get_video_output(out=None):
    #Specify the path and name of the video file as well as the encoding, fps and resolution
    if out:
        out.release()
    return cv2.VideoWriter('video/static_comp_IR_ ' + str(time.strftime('%Y-%m-%d_%H.%M.%S_Turret1')) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))
    #return cv2.VideoWriter('../home/pi/Documents/video/static_comp_IR_ ' + str(time.strftime('%Y-%m-%d_%H.%M.%S_Turret1')) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))



next_time = time.time() + 10#120
out = get_video_output()

try:
    while True:
        hour = int(time.strftime('%H'))
        print(type(hour))
        print(hour)
        if hour > 22 or hour < 2:
            if time.time() > next_time:
                next_time += 10#120
                out = get_video_output(out)
                print("New video")

            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:
                out.write(frame)
except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
