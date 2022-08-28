from __future__ import print_function
import cv2
import tensorflow as tf
import numpy as np

from Segmentation.threshold import MyThreshold
from Segmentation.blob_detector import MyBlobDetector
from Segmentation.hough_circle import MyHoughCircle
from Classification.settings import signs_name_blue, signs_name_red, signs_name_yellow
from Classification.settings import model_name, IMG_SIZE, image_depth


class MyTSR:
    model_blue = None
    model_red = None
    model_yellow = None

    signs_name_blue = None
    signs_name_red = None
    signs_name_yellow = None

    th_blue = None
    th_red = None
    th_yellow = None

    bd_blue = None
    hc_red = None
    bd_yellow = None

    kernel = None

    blue_i = 0
    red_i = 0
    yellow_i = 0

    def __init__(self, color1="blue", color2="red", color3="yellow"):

        self.model_blue = tf.keras.models.load_model('Classification/models/blue_{}.model'.format(model_name))
        self.model_red = tf.keras.models.load_model('Classification/models/red_{}.model'.format(model_name))
        self.model_yellow = tf.keras.models.load_model('Classification/models/yellow_{}.model'.format(model_name))

        self.th_blue = MyThreshold(color1)
        self.bd_blue = MyBlobDetector(color1)

        self.th_red = MyThreshold(color2)
        self.hc_red = MyHoughCircle(color2)

        self.th_yellow = MyThreshold(color3)
        self.bd_yellow = MyBlobDetector(color3)

        self.kernel = np.ones((3, 3), np.uint8)

    @staticmethod
    def prepare_image(image):
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image - cv2.equalizeHist(image)
        image = cv2.resize(image, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC)
        return image

    @staticmethod
    def get_roi(image, x, y, size, fit, delta):
        height, width, depth = image.shape
        size = int(size * fit + delta)
        x1 = x - size
        y1 = y - size
        x2 = x + size
        y2 = y + size
        if (x1 < 0) or (x1 >= x2) or (x2 > width) or (y1 < 0) or (y1 >= y2) or (y2 > height):
            return None
        roi = image[y1:y2, x1:x2]
        return roi

    def recognition(self, image, model, sings_name):
        image = self.prepare_image(image)
        image = np.array(image).reshape(-1, IMG_SIZE, IMG_SIZE, image_depth)
        image = image / 255.0
        prediction = model.predict(image)
        sign_number = np.argmax(prediction)
        name = sings_name[sign_number]
        percent = int(prediction[0][sign_number] * 10000) / 100
        return sign_number, percent, name

    def classification(self, image, signs_coordinates, model, signs_name, low_percent=99, fit=1.0, delfta=0):
        recognized_signs = []
        for sign_coordinates in signs_coordinates:
            x, y, size = sign_coordinates
            roi = self.get_roi(image=image, x=x, y=y, size=size, fit=fit, delta=delfta)
            if roi is None:
                break
            #cv2.imshow("", cv2.resize(roi, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC))

            sign_number, percent, name = self.recognition(roi, model, signs_name)
            if percent < low_percent:
                break
            recognized_signs.append([x, y, size, percent, name])
            #print(name, percent)
            #cv2.waitKey(0)

        return recognized_signs

    def blue_segmentation(self, image):
        image_threshold = self.th_blue.threshold(image)
        image_dilation = cv2.dilate(image_threshold, self.kernel, iterations=1)
        image_close = cv2.morphologyEx(image_dilation, cv2.MORPH_CLOSE, self.kernel, iterations=5)
        signs_coordinates = self.bd_blue.detect(image_close)
        return signs_coordinates

    def red_segmentation(self, image):
        image_threshold = self.th_red.threshold(image)
        image_close = cv2.morphologyEx(image_threshold, cv2.MORPH_CLOSE, self.kernel, iterations=1)
        signs_coordinates = self.hc_red.detect(image_close)
        return signs_coordinates

    def yellow_segmentation(self, image):
        image_threshold_ = self.th_yellow.threshold(image)
        image_open_ = cv2.morphologyEx(image_threshold_, cv2.MORPH_OPEN, self.kernel, iterations=1)
        image_close_ = cv2.morphologyEx(image_open_, cv2.MORPH_CLOSE, self.kernel, iterations=2)
        signs_coordinates = self.bd_blue.detect(image_close_)
        return signs_coordinates

    def get_blue_signs(self, image):
        signs_coordinates = self.blue_segmentation(image)
        recognized_signs = self.classification(image=image,
                                               signs_coordinates=signs_coordinates,
                                               model=self.model_blue,
                                               signs_name=signs_name_blue,
                                               low_percent=90,
                                               fit=1,
                                               delfta=5)
        return recognized_signs, signs_coordinates

    def get_red_signs(self, image):
        signs_coordinates = self.red_segmentation(image)
        recognized_signs = self.classification(image=image,
                                               signs_coordinates=signs_coordinates,
                                               model=self.model_red,
                                               signs_name=signs_name_red,
                                               low_percent=90,
                                               fit=1.5,
                                               delfta=0)
        return recognized_signs, signs_coordinates

    def get_yellow_signs(self, image):
        signs_coordinates = self.yellow_segmentation(image)
        recognized_signs = self.classification(image=image,
                                               signs_coordinates=signs_coordinates,
                                               model=self.model_yellow,
                                               signs_name=signs_name_yellow,
                                               low_percent=90.1,
                                               fit=1.5,
                                               delfta=5)
        return recognized_signs, signs_coordinates

    def save_settings(self):
        self.th_blue.save_settings()
        self.th_red.save_settings()
        self.th_yellow.save_settings()
        self.hc_red.save_settings()
        self.bd_blue.save_settings()
