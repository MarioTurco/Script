import cv2
from computer_vision import *

cv2.namedWindow("preview")
cam = cv2.VideoCapture(0)
#cv2.waitKey(0)

if cam.isOpened(): # try to get the first frame
    rval, frame = cam.read()
else:
    rval = False

while rval:
    frame = sobel_edge_detection(frame, 10, True)
    cv2.imshow("preview", frame)
    rval, frame = cam.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
cam.release()