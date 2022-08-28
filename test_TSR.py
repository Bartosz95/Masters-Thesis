import cv2
import os
import pickle
import Segmentation.myfcn as myfcn
from Classification.settings import signs_name
from myTSR import MyTSR
import pandas as pd


class TestTSR:
    active_camera = None
    cameras = None
    tsr = None
    tsr_right = None
    COLOR_BLUE = (255, 0, 0)
    COLOR_RED = (0, 0, 255)
    COLOR_YELLOW = (0, 255, 255)
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    type_signs_in_database = None

    def __init__(self, active_camera, path_to_benchmark):
        self.active_camera = active_camera  # ['Center', 'Left', 'Right']
        self.cameras = self.get_saved_signs(path_to_benchmark)
        self.tsr = MyTSR()
        self.tsr_right = MyTSR(color2='red_right')
        self.type_signs_in_database = []
        for sign_name in signs_name:
            self.type_signs_in_database.append(signs_name[sign_name])

    @staticmethod
    def get_saved_signs(path_to_benchmark):
        cameras = []
        files = os.listdir(path_to_benchmark)
        for file in files:
            if len(file.split('.')) == 2:
                if file.split('.')[1] == 'pickle':
                    pickle_path = os.path.join(path_to_benchmark, file)
                    pickle_in = open(pickle_path, "rb")
                    cameras.append(pickle.load(pickle_in))
        return cameras

    @staticmethod
    def check_detected_signs(signs_on_image, signs_from_tsr):
        count_of_misses = 0
        count_of_bed_recognised_signs = 0
        good_detected_signs = []
        for sign_from_tsr in signs_from_tsr:
            x_sign_tsr, y_sign_tsr, size_sign_tsr, percent_sign_tsr, type_sign_tsr = sign_from_tsr
            miss = True
            for sign_on_image in signs_on_image:
                (x1, y1, x2, y2), type_sign, color_sign = sign_on_image
                if (x_sign_tsr > x1) and (x_sign_tsr < x2) and (y_sign_tsr > y1) and (y_sign_tsr < y2):
                    miss = False
                    if type_sign_tsr == type_sign:
                        good_detected_signs.append(sign_from_tsr)
                        break
                    else:
                        count_of_bed_recognised_signs += 1
            if miss:
                count_of_misses += 1

        return good_detected_signs, count_of_misses, count_of_bed_recognised_signs

    @staticmethod
    def check_detected_regions(signs_on_image, regions_from_tsr):
        count_of_misses = 0
        count_of_good_detected_regions = 0
        for region_from_tsr in regions_from_tsr:
            x_tsr, y_tsr, size_tsr = region_from_tsr
            miss = True
            for sign_on_image in signs_on_image:
                (x1, y1, x2, y2), type_sign, color_sign = sign_on_image
                if (x_tsr > x1) and (x_tsr < x2) and (y_tsr > y1) and (y_tsr < y2):
                    miss = False
                    count_of_good_detected_regions += 1
                    break
            if miss:
                count_of_misses += 1
        return count_of_good_detected_regions, count_of_misses

    def test_detector_on_image(self, signs_on_image, detected_signs_by_tsr, detected_regions_by_tsr,
                               good_detected_signs, count_of_misses=0, count_of_bed_recognised=0,
                               count_of_good_detected_regions=0, count_of_misses_regions=0):

        good_detected_signs_by_tsr, misses, bed_recognised = \
            self.check_detected_signs(signs_on_image, detected_signs_by_tsr)
        good_detected_signs.extend(good_detected_signs_by_tsr)

        count_of_misses += misses
        count_of_bed_recognised += bed_recognised
        hits_regions_by_tsr, misses_regions_by_tsr = \
            self.check_detected_regions(signs_on_image, detected_regions_by_tsr)
        count_of_good_detected_regions += hits_regions_by_tsr
        count_of_misses_regions += misses_regions_by_tsr

        return good_detected_signs, count_of_misses, count_of_bed_recognised, \
               count_of_good_detected_regions, count_of_misses_regions

    def test(self):
        global yellow_count_of_bed_recognised, red_count_of_bed_recognised, yellow_count_of_bed_recognised

        # on image
        blue_count_of_signs_on_image = 0
        blue_count_of_signs_on_image_exist_in_database = 0
        blue_count_of_signs_on_image_exist_in_database_single = 0
        red_count_of_signs_on_image = 0
        red_count_of_signs_on_image_exist_in_database = 0
        red_count_of_signs_on_image_exist_in_database_single = 0
        yellow_count_of_signs_on_image = 0
        yellow_count_of_signs_on_image_exist_in_database = 0
        yellow_count_of_signs_on_image_exist_in_database_single = 0

        # detected
        blue_count_of_good_detected_regions = 0
        blue_count_of_misses_regions = 0
        blue_count_of_detected_signs = 0
        blue_count_of_detected_signs_single = 0
        blue_count_of_misses = 0
        blue_count_of_bed_recognised = 0

        red_count_of_good_detected_regions = 0
        red_count_of_misses_regions = 0
        red_count_of_detected_signs = 0
        red_count_of_detected_signs_single = 0
        red_count_of_misses = 0
        red_count_of_bed_recognised = 0

        yellow_count_of_good_detected_regions = 0
        yellow_count_of_misses_regions = 0
        yellow_count_of_detected_signs = 0
        yellow_count_of_detected_signs_single = 0
        yellow_count_of_misses = 0
        yellow_count_of_bed_recognised = 0

        j = 0
        print("START TEST")
        count_of_triple_photos = len(self.cameras[0][:])
        for i in range(count_of_triple_photos):
            print(int(i * 100 / count_of_triple_photos), "%")
            signs_on_images = []
            blue_good_detected_signs = []
            red_good_detected_signs = []
            yellow_good_detected_signs = []

            cam = 0
            for camera in self.cameras:
                image, signs_on_image = camera[i]
                signs_on_images.extend(signs_on_image)

                if self.active_camera.count(cam) and (cam == 0 or cam == 1):
                    image_roi = myfcn.region_of_interest(image)
                    image_equalized = myfcn.rgb_equalized_hist(image_roi)

                    blue_detected_signs_by_tsr, blue_detected_regions_by_tsr = self.tsr.get_blue_signs(image_equalized)

                    blue_good_detected_signs, blue_count_of_misses, blue_count_of_bed_recognised, \
                    blue_count_of_good_detected_regions, blue_count_of_misses_regions = self.test_detector_on_image(
                        signs_on_image=signs_on_image,
                        detected_signs_by_tsr=blue_detected_signs_by_tsr,
                        detected_regions_by_tsr=blue_detected_regions_by_tsr,
                        good_detected_signs=blue_good_detected_signs,
                        count_of_misses=blue_count_of_misses,
                        count_of_bed_recognised=blue_count_of_bed_recognised,
                        count_of_good_detected_regions=blue_count_of_good_detected_regions,
                        count_of_misses_regions=blue_count_of_misses_regions
                    )

                    red_detected_signs_by_tsr, red_detected_regions_by_tsr = self.tsr.get_red_signs(image_equalized)

                    red_good_detected_signs, red_count_of_misses, red_count_of_bed_recognised, \
                    red_count_of_good_detected_regions, red_count_of_misses_regions = self.test_detector_on_image(
                        signs_on_image=signs_on_image,
                        detected_signs_by_tsr=red_detected_signs_by_tsr,
                        detected_regions_by_tsr=red_detected_regions_by_tsr,
                        good_detected_signs=red_good_detected_signs,
                        count_of_misses=red_count_of_misses,
                        count_of_bed_recognised=red_count_of_bed_recognised,
                        count_of_good_detected_regions=red_count_of_good_detected_regions,
                        count_of_misses_regions=red_count_of_misses_regions
                    )

                    yellow_detected_signs_by_tsr, yellow_detected_regions_by_tsr = self.tsr.get_yellow_signs(image_equalized)

                    yellow_good_detected_signs, yellow_count_of_misses, yellow_count_of_bed_recognised, \
                    yellow_count_of_good_detected_regions, yellow_count_of_misses_regions = self.test_detector_on_image(
                        signs_on_image=signs_on_image,
                        detected_signs_by_tsr=yellow_detected_signs_by_tsr,
                        detected_regions_by_tsr=yellow_detected_regions_by_tsr,
                        good_detected_signs=yellow_good_detected_signs,
                        count_of_misses=yellow_count_of_misses,
                        count_of_bed_recognised=yellow_count_of_bed_recognised,
                        count_of_good_detected_regions=yellow_count_of_good_detected_regions,
                        count_of_misses_regions=yellow_count_of_misses_regions
                    )

                if self.active_camera.count(cam) and (cam == 2):
                    image_roi = myfcn.region_of_interest(image)
                    image_equalized = myfcn.rgb_equalized_hist(image_roi)

                    blue_detected_signs_by_tsr, blue_detected_regions_by_tsr = self.tsr_right.get_blue_signs(image_equalized)

                    blue_good_detected_signs, blue_count_of_misses, blue_count_of_bed_recognised, \
                    blue_count_of_good_detected_regions, blue_count_of_misses_regions = self.test_detector_on_image(
                        signs_on_image=signs_on_image,
                        detected_signs_by_tsr=blue_detected_signs_by_tsr,
                        detected_regions_by_tsr=blue_detected_regions_by_tsr,
                        good_detected_signs=blue_good_detected_signs,
                        count_of_misses=blue_count_of_misses,
                        count_of_bed_recognised=blue_count_of_bed_recognised,
                        count_of_good_detected_regions=blue_count_of_good_detected_regions,
                        count_of_misses_regions=blue_count_of_misses_regions
                    )

                    red_detected_signs_by_tsr, red_detected_regions_by_tsr = self.tsr_right.get_red_signs(image_equalized)

                    red_good_detected_signs, red_count_of_misses, red_count_of_bed_recognised, \
                    red_count_of_good_detected_regions, red_count_of_misses_regions = self.test_detector_on_image(
                        signs_on_image=signs_on_image,
                        detected_signs_by_tsr=red_detected_signs_by_tsr,
                        detected_regions_by_tsr=red_detected_regions_by_tsr,
                        good_detected_signs=red_good_detected_signs,
                        count_of_misses=red_count_of_misses,
                        count_of_bed_recognised=red_count_of_bed_recognised,
                        count_of_good_detected_regions=red_count_of_good_detected_regions,
                        count_of_misses_regions=red_count_of_misses_regions
                    )

                    yellow_detected_signs_by_tsr, yellow_detected_regions_by_tsr = self.tsr_right.get_yellow_signs(
                        image_equalized)

                    yellow_good_detected_signs, yellow_count_of_misses, yellow_count_of_bed_recognised, \
                    yellow_count_of_good_detected_regions, yellow_count_of_misses_regions = self.test_detector_on_image(
                        signs_on_image=signs_on_image,
                        detected_signs_by_tsr=yellow_detected_signs_by_tsr,
                        detected_regions_by_tsr=yellow_detected_regions_by_tsr,
                        good_detected_signs=yellow_good_detected_signs,
                        count_of_misses=yellow_count_of_misses,
                        count_of_bed_recognised=yellow_count_of_bed_recognised,
                        count_of_good_detected_regions=yellow_count_of_good_detected_regions,
                        count_of_misses_regions=yellow_count_of_misses_regions
                    )
                cam += 1

            # on image
            blue_signs_on_image = []
            blue_signs_on_image_exist_in_database = []
            blue_signs_on_image_exist_in_database_single = []
            red_signs_on_image = []
            red_signs_on_image_exist_in_database = []
            red_signs_on_image_exist_in_database_single = []
            yellow_signs_on_image = []
            yellow_signs_on_image_exist_in_database = []
            yellow_signs_on_image_exist_in_database_single = []
            for sign_on_images in signs_on_images:
                _, sign_type, sign_color = sign_on_images
                if sign_color == 'blue':
                    blue_signs_on_image.extend([sign_type])
                    if self.type_signs_in_database.count(sign_type) >= 1:
                        blue_signs_on_image_exist_in_database.append(sign_type)
                        if blue_signs_on_image_exist_in_database_single.count(sign_type) == 0:
                            blue_signs_on_image_exist_in_database_single.append(sign_type)
                elif sign_color == 'red':
                    red_signs_on_image.extend([sign_type])
                    if self.type_signs_in_database.count(sign_type) >= 1:
                        red_signs_on_image_exist_in_database.append(sign_type)
                        if red_signs_on_image_exist_in_database_single.count(sign_type) == 0:
                            red_signs_on_image_exist_in_database_single.append(sign_type)
                elif sign_color == 'yellow':
                    yellow_signs_on_image.extend([sign_type])
                    if self.type_signs_in_database.count(sign_type) >= 1:
                        yellow_signs_on_image_exist_in_database.append(sign_type)
                        if yellow_signs_on_image_exist_in_database_single.count(sign_type) == 0:
                            yellow_signs_on_image_exist_in_database_single.append(sign_type)

            blue_count_of_signs_on_image += len(blue_signs_on_image)
            blue_count_of_signs_on_image_exist_in_database += len(blue_signs_on_image_exist_in_database)
            blue_count_of_signs_on_image_exist_in_database_single += len(blue_signs_on_image_exist_in_database_single)

            red_count_of_signs_on_image += len(red_signs_on_image)
            red_count_of_signs_on_image_exist_in_database += len(red_signs_on_image_exist_in_database)
            red_count_of_signs_on_image_exist_in_database_single += len(red_signs_on_image_exist_in_database_single)

            yellow_count_of_signs_on_image += len(yellow_signs_on_image)
            yellow_count_of_signs_on_image_exist_in_database += len(yellow_signs_on_image_exist_in_database)
            yellow_count_of_signs_on_image_exist_in_database_single += len(
                yellow_signs_on_image_exist_in_database_single)

            # detected
            blue_detected_signs_single = []
            for blue_good_detected_sign in blue_good_detected_signs:
                sign_type = blue_good_detected_sign[4]
                if blue_detected_signs_single.count([sign_type]) == 0:
                    blue_detected_signs_single.append([sign_type])
            blue_count_of_detected_signs += len(blue_good_detected_signs)
            blue_count_of_detected_signs_single += len(blue_detected_signs_single)

            red_detected_signs_single = []
            for red_good_detected_sign in red_good_detected_signs:
                sign_type = red_good_detected_sign[4]
                if red_detected_signs_single.count([sign_type]) == 0:
                    red_detected_signs_single.append([sign_type])
            red_count_of_detected_signs += len(red_good_detected_signs)
            red_count_of_detected_signs_single += len(red_detected_signs_single)

            yellow_detected_signs_single = []
            for yellow_good_detected_sign in yellow_good_detected_signs:
                sign_type = yellow_good_detected_sign[4]
                if yellow_detected_signs_single.count([sign_type]) == 0:
                    yellow_detected_signs_single.append([sign_type])
            yellow_count_of_detected_signs += len(yellow_good_detected_signs)
            yellow_count_of_detected_signs_single += len(yellow_detected_signs_single)

        all_count_of_signs_on_image = blue_count_of_signs_on_image \
                                      + red_count_of_signs_on_image \
                                      + yellow_count_of_signs_on_image
        all_count_of_signs_on_image_exist_in_database = blue_count_of_signs_on_image_exist_in_database \
                                                        + red_count_of_signs_on_image_exist_in_database \
                                                        + yellow_count_of_signs_on_image_exist_in_database
        all_count_of_signs_on_image_exist_in_database_single = blue_count_of_signs_on_image_exist_in_database_single \
                                                               + red_count_of_signs_on_image_exist_in_database_single \
                                                               + yellow_count_of_signs_on_image_exist_in_database_single
        all_count_of_good_detected_regions = blue_count_of_good_detected_regions \
                                             + red_count_of_good_detected_regions \
                                             + yellow_count_of_good_detected_regions
        all_count_of_misses_regions = blue_count_of_misses_regions \
                                      + red_count_of_misses_regions \
                                      + yellow_count_of_misses_regions

        all_count_of_detected_signs = blue_count_of_detected_signs \
                                      + red_count_of_detected_signs \
                                      + yellow_count_of_detected_signs
        all_count_of_detected_signs_single = blue_count_of_detected_signs_single \
                                             + red_count_of_detected_signs_single \
                                             + yellow_count_of_detected_signs_single
        all_count_of_bed_recognised = blue_count_of_bed_recognised \
                                      + red_count_of_bed_recognised \
                                      + yellow_count_of_bed_recognised
        all_count_of_misses = blue_count_of_misses + red_count_of_misses + yellow_count_of_misses

        data = {
            'Color': [
                "All on image",
                "Database on image",
                "Good Regions",
                "Miss Regions",
                "Good Signs",
                "Bed Signs",
                "Miss Signs",
                "Type on image",
                "One Type Signs"
            ],
            'Blue': [
                blue_count_of_signs_on_image,
                blue_count_of_signs_on_image_exist_in_database,
                blue_count_of_good_detected_regions,
                blue_count_of_misses_regions,
                blue_count_of_detected_signs,
                blue_count_of_bed_recognised,
                blue_count_of_misses,
                blue_count_of_signs_on_image_exist_in_database_single,
                blue_count_of_detected_signs_single,
            ],
            'Red': [
                red_count_of_signs_on_image,
                red_count_of_signs_on_image_exist_in_database,
                red_count_of_good_detected_regions,
                red_count_of_misses_regions,
                red_count_of_detected_signs,
                red_count_of_bed_recognised,
                red_count_of_misses,
                red_count_of_signs_on_image_exist_in_database_single,
                red_count_of_detected_signs_single,
            ],
            'Yellow': [
                yellow_count_of_signs_on_image,
                yellow_count_of_signs_on_image_exist_in_database,
                yellow_count_of_good_detected_regions,
                yellow_count_of_misses_regions,
                yellow_count_of_detected_signs,
                yellow_count_of_bed_recognised,
                yellow_count_of_misses,
                yellow_count_of_signs_on_image_exist_in_database_single,
                yellow_count_of_detected_signs_single,
            ],
            'Totality': [
               all_count_of_signs_on_image,
               all_count_of_signs_on_image_exist_in_database,
               all_count_of_good_detected_regions,
               all_count_of_misses_regions,
               all_count_of_detected_signs,
               all_count_of_bed_recognised,
               all_count_of_misses,
               all_count_of_signs_on_image_exist_in_database_single,
               all_count_of_detected_signs_single,
            ]
        }

        data_percent = {
            '': [
                "Existing in database",
                "Good Regions",
                "Miss Regions",
                "Good Signs",
                "Bed Signs",
                "Miss Signs",
                "One Type Signs"
            ],
            'Blue': [
                int(blue_count_of_signs_on_image_exist_in_database / blue_count_of_signs_on_image * 10000) / 100,
                int(blue_count_of_good_detected_regions / blue_count_of_signs_on_image * 10000) / 100,
                int(blue_count_of_misses_regions / (
                            blue_count_of_misses_regions + blue_count_of_good_detected_regions) * 10000) / 100,
                int(blue_count_of_detected_signs / blue_count_of_signs_on_image_exist_in_database * 10000) / 100,
                int(blue_count_of_bed_recognised / blue_count_of_good_detected_regions * 10000) / 100,
                int(blue_count_of_misses / blue_count_of_misses_regions * 10000) / 100,
                int(blue_count_of_detected_signs_single / blue_count_of_signs_on_image_exist_in_database_single * 10000) / 100,
            ],
            'Red': [
                int(red_count_of_signs_on_image_exist_in_database / red_count_of_signs_on_image * 10000) / 100,
                int(red_count_of_good_detected_regions / red_count_of_signs_on_image * 10000) / 100,
                int(red_count_of_misses_regions / (
                        red_count_of_misses_regions + red_count_of_good_detected_regions) * 10000) / 100,
                int(red_count_of_detected_signs / red_count_of_signs_on_image_exist_in_database * 10000) / 100,
                int(red_count_of_bed_recognised / (1+red_count_of_good_detected_regions) * 10000) / 100,
                int(red_count_of_misses / (1 + red_count_of_misses_regions) * 10000) / 100,
                int(
                    red_count_of_detected_signs_single / red_count_of_signs_on_image_exist_in_database_single * 10000) / 100,
            ],
            'Yellow': [
                int(yellow_count_of_signs_on_image_exist_in_database / yellow_count_of_signs_on_image * 10000) / 100,
                int(yellow_count_of_good_detected_regions / yellow_count_of_signs_on_image * 10000) / 100,
                int(yellow_count_of_misses_regions / (
                        yellow_count_of_misses_regions + yellow_count_of_good_detected_regions) * 10000) / 100,
                int(yellow_count_of_detected_signs / yellow_count_of_signs_on_image_exist_in_database * 10000) / 100,
                int(yellow_count_of_bed_recognised / yellow_count_of_good_detected_regions * 10000) / 100,
                int(yellow_count_of_misses / yellow_count_of_misses_regions * 10000) / 100,
                int(
                    yellow_count_of_detected_signs_single / yellow_count_of_signs_on_image_exist_in_database_single * 10000) / 100,
            ],
            'Totality': [
                int(all_count_of_signs_on_image_exist_in_database / all_count_of_signs_on_image * 10000) / 100,
                int(all_count_of_good_detected_regions / all_count_of_signs_on_image * 10000) / 100,
                int(all_count_of_misses_regions / (
                        all_count_of_misses_regions + all_count_of_good_detected_regions) * 10000) / 100,
                int(all_count_of_detected_signs / all_count_of_signs_on_image_exist_in_database * 10000) / 100,
                int(all_count_of_bed_recognised / all_count_of_good_detected_regions * 10000) / 100,
                int(all_count_of_misses / all_count_of_misses_regions * 10000) / 100,
                int(
                    all_count_of_detected_signs_single / all_count_of_signs_on_image_exist_in_database_single * 10000) / 100,
            ],
        }
        df = pd.DataFrame(data)
        df_percent = pd.DataFrame(data_percent)
        return df, df_percent, data
