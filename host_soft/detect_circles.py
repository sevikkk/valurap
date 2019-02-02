import cv2
import numpy as np
import os

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

for fn in os.listdir('.'):
    if not fn.startswith("snap-"):
        continue
    if not fn.endswith(".jpg"):
        continue
    print(fn)

    img = cv2.imread(fn)
    ret, circles = cv2.findCirclesGrid(img, (6,6))
    if not ret:
        continue

    cv2.drawChessboardCorners(img, (6, 6), circles, ret)

    if not window:
        cv2.namedWindow("bubu", cv2.WINDOW_NORMAL)
        window = True

    cv2.imshow("bubu", img)
    cv2.waitKey(100)

    print(circles)

    p1 = circles[0][0]
    p2 = circles[1][0]
    p3 = circles[6][0]
    print(p1,p2,p3)
    print(p2[0] - p1[0])
    print(p2[1] - p1[1])
    print(p3[0] - p1[0])
    print(p3[1] - p1[1])
    objpoints.append(objp)
    imgpoints.append(circles)

cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[::-1][1:3], None, None)
print("ret:", ret)
print("mtx:", mtx)
print("dist:", dist)
for i in range(len(rvecs)):
    print("   {}: {} {}".format(i, rvecs[i].T, tvecs[i].T))

