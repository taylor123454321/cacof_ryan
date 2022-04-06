import numpy as np
import cv2
import time
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

def get_video_output(out=None):
    #Specify the path and name of the video file as well as the encoding, fps and resolution
    if out:
        out.release()
    return cv2.VideoWriter('video/test_' + str(time.strftime('%Y-%m-%d_%H.%M.%S_Turret1')) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))



next_time = time.time() + 30
out = get_video_output()

try:
    while True:
        if time.time() > next_time:
            next_time += 30
            out = get_video_output(out)
            print("New video")

        # Capture frame-by-frame
        ret, frame = cap.read() 
        if ret:
            out.write(frame)
except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
