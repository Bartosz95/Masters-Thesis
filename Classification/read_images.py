import os
import cv2
import Classification.settings as settings
import numpy as np
import pickle
import random
from myTSR import MyTSR


def read_data(PATH):
    data = []
    CATEGORIES = os.listdir(PATH)
    for CATEGORY in CATEGORIES[:]:
        print(CATEGORY)
        path_to_images = os.path.join(PATH, CATEGORY)
        image_name_list = os.listdir(path_to_images)
        for image_name in image_name_list[:]:
            path_to_image = os.path.join(path_to_images, image_name)
            try:
                image = cv2.imread(path_to_image)
                image = MyTSR.prepare_image(image)
                class_number = int(CATEGORY.split(' ')[0])
                data.append([image, class_number])
            except Exception:
                print(image_name)
    return data


def save_data(data, Color, name):
    X = []
    Y = []
    for features, label in data:
        X.append(features)
        Y.append(label)
    X = np.array(X).reshape(-1, settings.image_weight, settings.image_height, settings.image_depth)
    X = X/255.0

    pickle_out = open("data/{}_X_{}.pickle".format(Color, name), "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open("data/{}_Y_{}.pickle".format(Color, name), "wb")
    pickle.dump(Y, pickle_out)
    pickle_out.close()


directory = settings.PATH_DIR
IMG_SIZE = settings.IMG_SIZE

colors = ['blue', 'red', 'yellow']  # []
destinations = ['Training', 'Test']
for color in colors:
    for destination in destinations:
        PATH = os.path.join('..', directory,  color, destination)
        data = read_data(PATH)
        random.shuffle(data)
        save_data(data, color, destination)

cv2.destroyAllWindows()
