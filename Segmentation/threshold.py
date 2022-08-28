import cv2
import sqlite3 as lite
import sys
import pickle


class MyThreshold:

    name = None
    params = None

    def __init__(self, color, active_trackbar=False):

        self.name = color
        self.params = []
        self.load_params()

        max_value_H = 180
        max_value = 255
        if active_trackbar:
            cv2.namedWindow(self.name)
            cv2.createTrackbar(self.params[0][0], self.name, self.params[0][1], max_value_H, self.low_H_thresh_trackbar)
            cv2.createTrackbar(self.params[1][0], self.name, self.params[1][1], max_value_H, self.high_H_thresh_trackbar)
            cv2.createTrackbar(self.params[2][0], self.name, self.params[2][1], max_value, self.low_S_thresh_trackbar)
            cv2.createTrackbar(self.params[3][0], self.name, self.params[3][1], max_value, self.high_S_thresh_trackbar)
            cv2.createTrackbar(self.params[4][0], self.name, self.params[4][1], max_value, self.low_V_thresh_trackbar)
            cv2.createTrackbar(self.params[5][0], self.name, self.params[5][1], max_value, self.high_V_thresh_trackbar)
            cv2.createTrackbar(self.params[6][0], self.name, self.params[6][1], max_value_H, self.low_H_thresh_trackbar2)
            cv2.createTrackbar(self.params[7][0], self.name, self.params[7][1], max_value_H, self.high_H_thresh_trackbar2)

    def threshold(self, image):
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        threshold = cv2.inRange(image_hsv, (self.params[0][1], self.params[2][1], self.params[4][1]),
                                (self.params[1][1], self.params[3][1], self.params[5][1]))

        threshold2 = cv2.inRange(image_hsv, (self.params[6][1], self.params[2][1], self.params[4][1]),
                                     (self.params[7][1], self.params[3][1], self.params[5][1]))

        threshold = cv2.addWeighted(threshold, 1, threshold2, 1, 0)
        return threshold

    def load_params(self):
        try:
            pickle_in = open("Segmentation/data/threshold_{}.pickle".format(self.name), "rb")
            self.params = pickle.load(pickle_in)
            pickle_in.close()
            try:
                self.params[6][1]
                self.params[7][1]
            except:
                self.params.append(['Low H2', 0])
                self.params.append(['high_H2', 1])

        except Exception as e:
            print("Default threshold params {}".format(self.name))
            self.params = [['Low H', 0], ['high_H', 180], ['Low S', 0], ['high_S', 255], ['Low V', 0], ['high_V', 255], ['Low H2', 0], ['high_H2', 180]]

    def save_settings(self):
        try:
            pickle_out = open("Segmentation/data/threshold_{}.pickle".format(self.name), "wb")
            pickle.dump(self.params, pickle_out)
            pickle_out.close()
        except Exception as e:
            print("Error save threshold_{}:".format(self.name))

    def low_H_thresh_trackbar(self, val):
        self.params[0][1] = min(self.params[1][1] - 1, val)
        cv2.setTrackbarPos(self.params[0][0], self.name, self.params[0][1])

    def high_H_thresh_trackbar(self, val):
        self.params[1][1] = max(val, self.params[0][1] + 1)
        cv2.setTrackbarPos(self.params[1][0], self.name, self.params[1][1])

    def low_S_thresh_trackbar(self, val):
        self.params[2][1] = min(self.params[3][1] - 1, val)
        cv2.setTrackbarPos(self.params[2][0], self.name, self.params[2][1])

    def high_S_thresh_trackbar(self, val):
        self.params[3][1] = max(val, self.params[2][1] + 1)
        cv2.setTrackbarPos(self.params[3][0], self.name, self.params[3][1])

    def low_V_thresh_trackbar(self, val):
        self.params[4][1] = min(self.params[5][1] - 1, val)
        cv2.setTrackbarPos(self.params[4][0], self.name, self.params[4][1])

    def high_V_thresh_trackbar(self, val):
        self.params[5][1] = max(self.params[4][1]+1, val)
        cv2.setTrackbarPos(self.params[5][0], self.name, self.params[5][1])

    def low_H_thresh_trackbar2(self, val):
        self.params[6][1] = min(self.params[7][1] - 1, val)
        cv2.setTrackbarPos(self.params[6][0], self.name, self.params[6][1])

    def high_H_thresh_trackbar2(self, val):
        self.params[7][1] = max(val, self.params[6][1] + 1)
        cv2.setTrackbarPos(self.params[7][0], self.name, self.params[7][1])

"""
    # yellow
    low_H = 10
    high_H = 30
    low_S = 50
    high_S = 255
    low_V = 70
    high_V = 255

    # blue
    low_H = 80
    high_H = 120
    low_S = 80
    high_S = 255
    low_V = 70
    high_V = 230

    # red
    low_H = 160
    high_H = 180
    low_S = 80
    high_S = 255
    low_V = 30
    high_V = 180
"""