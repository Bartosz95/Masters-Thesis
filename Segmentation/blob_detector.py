import cv2
import sqlite3 as lite
import sys
import pickle


class MyBlobDetector:
    name = None
    params = None
    detector = None

    def __init__(self, name, active_trackbar=False):
        self.name = name
        self.load_params()
        max_value_th = 255
        max_value_ar = 8000
        max_value = 100
        if active_trackbar:
            cv2.namedWindow(self.name)
            cv2.createTrackbar(self.params[0][0], self.name, self.params[0][1], max_value_th, self.min_threshold_track_bar)
            cv2.createTrackbar(self.params[1][0], self.name, self.params[1][1], max_value_th, self.max_threshold_track_bar)
            cv2.createTrackbar(self.params[2][0], self.name, self.params[2][1], max_value_ar, self.min_area_track_bar)
            cv2.createTrackbar(self.params[3][0], self.name, self.params[3][1], max_value_ar, self.max_area_track_bar)
            cv2.createTrackbar(self.params[4][0], self.name, self.params[4][1], max_value, self.min_circularity_track_bar)
            cv2.createTrackbar(self.params[5][0], self.name, self.params[5][1], max_value, self.max_circularity__track_bar)
            cv2.createTrackbar(self.params[6][0], self.name, self.params[6][1], max_value, self.min_convexity_track_bar)
            cv2.createTrackbar(self.params[7][0], self.name, self.params[7][1], max_value, self.max_convexity__track_bar)
            cv2.createTrackbar(self.params[8][0], self.name, self.params[8][1], max_value, self.min_inertia_ratio_track_bar)
            cv2.createTrackbar(self.params[9][0], self.name, self.params[9][1], max_value, self.max_inertia_ratio__track_bar)

    def detect(self, image):
        self.create_detector()  # przeniesc do konstruntora
        key_points = self.detector.detect(image)
        blob = []
        for key_point in key_points:
            blob.append((int(key_point.pt[0]), int(key_point.pt[1]), int(key_point.size/2)))
        return blob
    
    def create_detector(self):

        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = False
        params.minThreshold = self.params[0][1]
        params.maxThreshold = self.params[1][1]

        params.filterByArea = True
        params.minArea = self.params[2][1]
        params.maxArea = self.params[3][1]

        params.filterByCircularity = True
        params.minCircularity = self.params[4][1] * 0.01
        params.maxCircularity = self.params[5][1] * 0.01

        params.filterByConvexity = True
        params.minConvexity = self.params[6][1] * 0.01
        params.maxConvexity = self.params[7][1] * 0.01

        params.filterByInertia = True
        params.minInertiaRatio = self.params[8][1] * 0.01
        params.maxInertiaRatio = self.params[9][1] * 0.01
        self.detector = cv2.SimpleBlobDetector_create(params)

    def load_params(self):
        try:
            pickle_in = open("Segmentation/data/blob_{}.pickle".format(self.name), "rb")
            self.params = pickle.load(pickle_in)
            pickle_in.close()
        except Exception as e:
            print("Default blob params {}".format(self.name))
            self.params = ['min_Threshold', 0], ['maxThreshold', 255], \
                          ['minArea', 0], ['maxArea', 1000], \
                          ['minCircularity', 0], ['maxCircularity', 100], \
                          ['minConvexity', 0], ['maxConvexity', 100], \
                          ['minInertiaRatio', 0], ['maxInertiaRatio', 100]
            
    def save_settings(self):
        try:
            pickle_out = open("Segmentation/data/blob_{}.pickle".format(self.name), "wb")
            pickle.dump(self.params, pickle_out)
            pickle_out.close()
        except Exception as e:
            print("Error save blob_{}:".format(self.name))

    def min_threshold_track_bar(self, val):
        self.params[0][1] = min(self.params[1][1] - 1, val)
        cv2.setTrackbarPos(self.params[0][0], self.name, self.params[0][1])

    def max_threshold_track_bar(self, val):
        self.params[1][1] = max(val, self.params[0][1] + 1)
        cv2.setTrackbarPos(self.params[1][0], self.name, self.params[1][1])

    def min_area_track_bar(self, val):
        self.params[2][1] = min(self.params[3][1] - 1, val)
        cv2.setTrackbarPos(self.params[2][0], self.name, self.params[2][1])

    def max_area_track_bar(self, val):
        self.params[3][1] = max(val, self.params[2][1] + 1)
        cv2.setTrackbarPos(self.params[3][0], self.name, self.params[3][1])

    def min_circularity_track_bar(self, val):
        self.params[4][1] = min(self.params[5][1] - 1, val)
        cv2.setTrackbarPos(self.params[4][0], self.name, self.params[4][1])

    def max_circularity__track_bar(self, val):
        self.params[5][1] = max(self.params[4][1]+1, val)
        cv2.setTrackbarPos(self.params[5][0], self.name, self.params[5][1])

    def min_convexity_track_bar(self, val):
        self.params[6][1] = min(self.params[7][1] - 1, val)
        cv2.setTrackbarPos(self.params[6][0], self.name, self.params[6][1])

    def max_convexity__track_bar(self, val):
        self.params[7][1] = max(self.params[6][1] + 1, val)
        cv2.setTrackbarPos(self.params[7][0], self.name, self.params[7][1])

    def min_inertia_ratio_track_bar(self, val):
        self.params[8][1] = min(self.params[5][1] - 1, val)
        cv2.setTrackbarPos(self.params[8][0], self.name, self.params[8][1])

    def max_inertia_ratio__track_bar(self, val):
        self.params[9][1] = max(self.params[8][1] + 1, val)
        cv2.setTrackbarPos(self.params[9][0], self.name, self.params[9][1])
