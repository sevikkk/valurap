import time
t0 = time.time()

import cv2
import numpy as np
import os

param1 = np.zeros((6 * 6, 3), np.float32)
param2 = (np.mgrid[-3:3,-3:3] + 0.5).T.reshape(-1,2)
params = [param1, param2]

objp = params[0]
objp[:, :2] = params[1]

objp = 2.469438 * objp 

objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
window = False

mtx = np.array([[1.85583369e+03, 0.00000000e+00, 7.96781205e+02],
       [0.00000000e+00, 1.86524428e+03, 6.48427700e+02],
       [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.array([[ 4.38909294e-02, -3.72379589e-01,  5.96935378e-03,
        -1.39161992e-04, -1.18364075e+00]])
t1 = time.time()
img = cv2.imread('images/snap.jpg')
t2 = time.time()
ret, circles = cv2.findCirclesGrid(img, (6,6))
t3 = time.time()
if ret:
    retval, rvec, tvec = cv2.solvePnP(objp, circles, mtx, dist)
    t4 = time.time()
    print("solved {:10.6f} {:10.6f} {:10.6f} {:10.3f} {:10.3f} {:10.3f}".format(*(list(rvec.T[0]) + list(tvec.T[0]))))
else:
    t4 = time.time()
    print("not_found")

print("timing init {}ms, read {}ms, find {}ms, solve {}ms".format(int(1000* (t1 - t0)), int(1000*(t2 - t1)), int(1000*(t3 - t2)), int(1000*(t4 - t3))))

