import cv2
import numpy as np
import os
import time

param1 = np.zeros((6 * 6, 3), np.float32)
param2 = np.mgrid[0:6,0:6].T.reshape(-1,2)
params = [param1, param2]

objp = params[0]
objp[:, :2] = params[1]

objp = 2.469438 * objp 
print(objp)

objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
window = False

mtx = np.array([[1.85583369e+03, 0.00000000e+00, 7.96781205e+02],
       [0.00000000e+00, 1.86524428e+03, 6.48427700e+02],
       [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.array([[ 4.38909294e-02, -3.72379589e-01,  5.96935378e-03,
        -1.39161992e-04, -1.18364075e+00]])

prev_fn = None
while 1:
    flist = []
    for fn in os.listdir('images'):
        if not fn.startswith("snap-"):
            continue
        if not fn.endswith(".jpg"):
            continue
        flist.append(fn)
    flist.sort()
    fn = flist[-1]
    if fn == prev_fn:
        time.sleep(0.1)
        continue

    prev_fn = fn

    img = cv2.imread('images/' + fn)
    ret, circles = cv2.findCirclesGrid(img, (6,6))
    if ret:
        cv2.drawChessboardCorners(img, (6, 6), circles, ret)
        retval, rvec, tvec = cv2.solvePnP(objp, circles, mtx, dist)
        print("solved:", retval, rvec.T[0], tvec.T[0])

    if not window:
        cv2.namedWindow("bubu", cv2.WINDOW_NORMAL)
        window = True

    cv2.imshow("bubu", img)
    cv2.waitKey(100)

