from __future__ import print_function
import cv2
import copy
import Segmentation.myfcn as myfcn
from myTSR import MyTSR


tsr = MyTSR()

COLOR_BLUE = (255, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_YELLOW = (0, 255, 255)
FONT = cv2.FONT_HERSHEY_SIMPLEX
number = 0

FILM_LEFT = "1.1.mp4"
FILM_CENTER = "1.2.mp4"
FILM_RIGHT = "1.3.mp4"

cap_left = cv2.VideoCapture("images/{}".format(FILM_LEFT))
cap_center = cv2.VideoCapture("images/{}".format(FILM_CENTER))
cap_right = cv2.VideoCapture("images/{}".format(FILM_RIGHT))

start_frame = True
frame_copy = None
frame_left = None
frame_center = None
frame_right = None

while True:
    if start_frame:
        _, frame_left = cap_left.read()
        _, frame_center = cap_center.read()
        _, frame_right = cap_right.read()
        if (frame_left is None) or (frame_center is None) or (frame_right is None): break
        frame_copy_left = copy.copy(frame_left)
        frame_copy_center = copy.copy(frame_center)
        frame_copy_right = copy.copy(frame_right)
    else:
        frame_left = copy.copy(frame_copy_left)
        frame_center = copy.copy(frame_copy_center)
        frame_right = copy.copy(frame_copy_right)

    for frame, name in [[frame_left, "Left"], [frame_center, "Center"], [frame_right, "Right"]]:  #
        frame_roi = myfcn.region_of_interest(frame)
        frame_equalized = myfcn.rgb_equalized_hist(frame_roi)

        # blue
        blue_signs = tsr.get_blue_signs(frame_equalized)
        for sign in blue_signs:
            x1 = sign[0] - sign[2]
            y1 = sign[1] - sign[2]
            x2 = sign[0] + sign[2]
            y2 = sign[1] + sign[2]
            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), COLOR_BLUE, 1)
            cv2.putText(frame, "{}% - {}".format(sign[4], sign[5]),
                        (x1, y2 + 20), FONT, 0.4, COLOR_BLUE, 1)

        # red
        red_signs = tsr.get_red_signs(frame_equalized)
        for sign in red_signs:
            x1 = sign[0] - sign[2]
            y1 = sign[1] - sign[2]
            x2 = sign[0] + sign[2]
            y2 = sign[1] + sign[2]
            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), COLOR_RED, 1)
            cv2.putText(frame, "{}% - {}".format(sign[4], sign[5]),
                        (x1, y2 + 20), FONT, 0.4, COLOR_RED, 1)

        # yellow
        yellow_signs = tsr.get_yellow_signs(frame_equalized)
        for sign in yellow_signs:
            x1 = sign[0] - sign[2]
            y1 = sign[1] - sign[2]
            x2 = sign[0] + sign[2]
            y2 = sign[1] + sign[2]
            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), COLOR_YELLOW, 1)
            cv2.putText(frame, "{}% - {}".format(sign[4], sign[5]),
                        (x1, y2 + 20), FONT, 0.4, COLOR_YELLOW, 1)

        cv2.imshow(name, frame)

    key = cv2.waitKey(1)
    # quit
    if key == ord('q'):
        break
    # pause
    if key == ord('p'):
        if start_frame:
            start_frame = False
        else:
            start_frame = True
    # save settings
    if key == ord('s'):
        tsr.save_settings()
    # screen shot
    """
    if key == ord('h'):
        for frame, name in [[frame_copy_left, "Left"], [frame_copy_center, "Center"], [frame_copy_right, "Right"]]:
            cv2.imwrite("images/Benchmark/{}/{}.jpg".format(name, number), frame)
        number += 1
        print("make {} snapshot".format(number))
    """

cv2.destroyAllWindows()
