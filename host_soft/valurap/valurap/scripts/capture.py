import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
#ret, frame = cap.read()
#print("capture:", ret)

#w = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
#h = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
#f = cap.get(cv2.cv.CV_CAP_PROP_FPS)
#m = cap.get(cv2.cv.CV_CAP_PROP_MODE)
#print(w,h,f,m)
#f = cap.set(cv2.cv.CV_CAP_PROP_FPS, 3)
#print(f)
size_x = int(640/3)
size_y = int(480/3)
t = time.time()
while True:
    ret, frame = cap.read()
    small = cv2.cv2.resize(frame, (size_x,size_y))
    #gray = cv2.cvtColor(small,cv2.COLOR_BGR2GRAY)

    t1 = time.time()
    print("capture:", ret, t1 - t)
    ret, circles = cv2.findCirclesGrid(small, (6,6))
    print("find:", ret, (circles[0] + circles[5] + circles[30] + circles[35] - np.array([[size_x*2, size_y*2]])) if ret else None)
    t = t1
