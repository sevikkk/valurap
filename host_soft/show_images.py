import cv2
import numpy as np
import os
import time

param1 = np.zeros((6 * 6, 3), np.float32)
param2 = (np.mgrid[-3:3,-3:3] + 0.5).T.reshape(-1,2)
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

prev_inode = None
while 1:
    inode = os.stat('images/snap0.jpg').st_ino

    if inode == prev_inode:
        time.sleep(0.1)
        continue

    prev_inode = inode

    img = cv2.imread('images/snap0.jpg')
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
