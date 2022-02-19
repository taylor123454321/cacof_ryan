import numpy as np
import cv2s
import time

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

def get_output(out=None):
    #Specify the path and name of the video file as well as the encoding, fps and resolution
    if out:
        out.release()
    return cv2.VideoWriter('test' + str(time.strftime('%d %m %Y - %H %M %S' )) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (frame_width, frame_height))


cap = cv2.VideoCapture(0)
next_time = time.time() + 20
out = get_output()

while True:
    if time.time() > next_time:
        next_time += 20
        out = get_output(out)

    # Capture frame-by-frame
    ret, frame = cap.read() 

    if ret:
        out.write(frame)

cap.release()
cv2.destroyAllWindows()
