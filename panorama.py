import Segmentation.myfcn as my
import os
import cv2
from Segmentation.blob_detector import MyBlobDetector
from Segmentation.threshold import MyThreshold
from Segmentation.hough_circle import MyHoughCircle
from Segmentation.canny import MyCanny

"""
th_blue = MyThreshold("blue", True)
bd_blue = MyBlobDetector("blue", False)



th_yellow = MyThreshold("yellow", True)
bd_yellow = MyBlobDetector("yellow", False)

#th_blue.save_settings()
#th_red.save_settings()
#th_yellow.save_settings()
#bd_blue.save_settings()
#bd_yellow.save_settings()
"""

color = (255, 255, 255)
th_red = MyThreshold("red_right", False)
hc_red = MyHoughCircle('red_right', False)

th_blue = MyThreshold("blue_right", True)
bd_blue = MyBlobDetector("blue_right", True)

p = 'images/Benchmark/Right'
names = os.listdir(p)
for name in names:
    while True:
        path = os.path.join(p, name)
        image = cv2.imread(path)
        cv2.imshow('im', image)

        th = th_blue.threshold(image)
        circles = bd_blue.detect(th)
        print(circles)
        for circle in circles:
            x, y, r = circle
            r *= 2
            cv2.circle(th, (x, y), radius=r, color=color, thickness=1)
        cv2.imshow('th', th)
        key = cv2.waitKey(10)
        if key == ord('s'):
            th_blue.save_settings()
            bd_blue.save_settings()
        if key == ord('n') or key == ord('q'):
            break
    if key == ord('q'):
        break





#cv2.waitKey(0)

cv2.destroyAllWindows()
