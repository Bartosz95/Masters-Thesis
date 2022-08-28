import cv2
import pickle


class MyHoughCircle:
    name = None
    params = None
    detector = None

    def __init__(self, name, active_trackbar=False):
        self.name = name
        self.load_params()
        max_value = 100
        if active_trackbar:
            cv2.namedWindow(self.name)
            cv2.createTrackbar(self.params[0][0], self.name, self.params[0][1], max_value, self.resAcumulator_track_bar)
            cv2.createTrackbar(self.params[1][0], self.name, self.params[1][1], max_value, self.minDis_track_bar)
            cv2.createTrackbar(self.params[2][0], self.name, self.params[2][1], max_value, self.threshold_track_bar)
            cv2.createTrackbar(self.params[3][0], self.name, self.params[3][1], max_value, self.center_track_bar)
            cv2.createTrackbar(self.params[4][0], self.name, self.params[4][1], max_value, self.minRadius_track_bar)
            cv2.createTrackbar(self.params[5][0], self.name, self.params[5][1], max_value, self.maxRadius_track_bar)

    def detect(self, image):
        ret = []
        circles = cv2.HoughCircles(image,
                                   method=cv2.HOUGH_GRADIENT,
                                   dp=self.params[0][1]/10,
                                   minDist=self.params[1][1],
                                   param1=self.params[2][1],
                                   param2=self.params[3][1],
                                   minRadius=self.params[4][1],
                                   maxRadius=self.params[5][1])

        if circles is not None:
            for c in circles:
                for circle in c:
                    ret.append((int(circle[0]), int(circle[1]), int(circle[2])))
        return ret

    def load_params(self):
        try:
            pickle_in = open("Segmentation/data/circle_{}.pickle".format(self.name), "rb")
            self.params = pickle.load(pickle_in)
            pickle_in.close()
        except Exception as e:
            print("Default circle params {}".format(self.name))
            self.params = ['resAccumulator', 1], ['minDis', 15], \
                          ['threshold', 1], ['center', 15], \
                          ['minRadius', 6], ['maxRadius', 18]

    def save_settings(self):
        try:
            pickle_out = open("Segmentation/data/circle_{}.pickle".format(self.name), "wb")
            pickle.dump(self.params, pickle_out)
            pickle_out.close()
        except Exception as e:
            print("Error save circle_{}:".format(self.name))

    def resAcumulator_track_bar(self, val):
        self.params[0][1] = val
        cv2.setTrackbarPos(self.params[0][0], self.name, self.params[0][1])

    def minDis_track_bar(self, val):
        self.params[1][1] = val
        cv2.setTrackbarPos(self.params[1][0], self.name, self.params[1][1])

    def threshold_track_bar(self, val):
        self.params[2][1] = val
        cv2.setTrackbarPos(self.params[2][0], self.name, self.params[2][1])

    def center_track_bar(self, val):
        self.params[3][1] = val
        cv2.setTrackbarPos(self.params[3][0], self.name, self.params[3][1])

    def minRadius_track_bar(self, val):
        self.params[4][1] = val
        cv2.setTrackbarPos(self.params[4][0], self.name, self.params[4][1])

    def maxRadius_track_bar(self, val):
        self.params[5][1] = val
        cv2.setTrackbarPos(self.params[5][0], self.name, self.params[5][1])
