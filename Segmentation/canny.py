import cv2
import pickle


class MyCanny:
    params = None
    name = None

    def __init__(self, name, active_trackbar=False):
        self.name = name
        self.load_params()
        if active_trackbar:
            cv2.namedWindow(self.name)
            cv2.createTrackbar(self.params[0][0], self.name, self.params[0][1], 255, self.min_threshold_track_bar)
            cv2.createTrackbar(self.params[1][0], self.name, self.params[1][1], 255, self.max_threshold_track_bar)
            cv2.createTrackbar(self.params[2][0], self.name, self.params[2][1], 20, self.kernel_size_track_bar)

    def canny(self, image):
        kernel = self.params[2][1] * 2 - 1
        blur = cv2.GaussianBlur(image, (kernel, kernel), 0)
        canny = cv2.Canny(blur, self.params[0][1], self.params[1][1])
        return canny

    def load_params(self):
        try:
            pickle_in = open("Segmentation/data/canny_{}.pickle".format(self.name), "rb")
            self.params = pickle.load(pickle_in)
            pickle_in.close()
            print(self.params)
        except Exception as e:
            print("Default canny params {}".format(self.name))
            self.params = [['Min', 50], ['Max', 150], ['Kernel', 1]]

    def save_settings(self):
        try:
            pickle_out = open("Segmentation/data/canny_{}.pickle".format(self.name), "wb")
            pickle.dump(self.params, pickle_out)
            pickle_out.close()
        except Exception as e:
            print("Error save circle_{}:".format(self.name))

    def min_threshold_track_bar(self, val):
        self.threshold_min = min(self.threshold_max - 1, val)
        cv2.setTrackbarPos("Min", self.name, self.threshold_min)

    def max_threshold_track_bar(self, val):
        self.threshold_max = max(val, self.threshold_min + 1)
        cv2.setTrackbarPos("Max", self.name, self.threshold_max)

    def kernel_size_track_bar(self, val):
        self.kernel_size = max(1, val)
        cv2.setTrackbarPos("Kernel", self.name, self.kernel_size)
