import tensorflow as tf
import cv2
import Classification.settings as settings
import pickle
import numpy as np
import os

"""
COLOR = "blue"
IMG_SIZE = settings.IMG_SIZE
count_of_class = settings.COUNT_OF_BLUE_CLASSES
pickle_in = open("data/X_{}_test.pickle".format(COLOR), "rb")
x_test = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("data/Y_{}_test.pickle".format(COLOR), "rb")
y_test = pickle.load(pickle_in)
pickle_in.close()

data = [x_test, y_test]



def test_model(model, data):
    good_recognized = 0
    bed_recognized = 0
    not_recognized = 0
    count_of_test_data = len(data[0])

    for i in range(count_of_test_data)[:]:
        image = data[0][i]
        number_of_sing = data[1][i]
        image = np.array(image).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
        prediction = model.predict(image)
        k = 0
        for j in range(count_of_class):
            if prediction[0][j] >= 0.9:
                if int(number_of_sing) == j:
                    good_recognized += 1
                else:
                    bed_recognized += 1
            else:
                k += 1
        if k == count_of_class:
            not_recognized += 1
    print("GOOD: {}% | BED: {}% | NOT_REC: {}%".format(int((good_recognized)),  # /count_of_test_data)*100),
                                                 int((bed_recognized)),  #/count_of_test_data)*100),
                                                 int((not_recognized))))  #/count_of_test_data)*100)))
"""

IMG_SIZE = settings.IMG_SIZE
count_of_class = settings.COUNT_OF_CLASSES_BLUE
PATH_DIR = settings.PATH_DIR
PATH_TEST = settings.PATH_TEST
COLOR = 'blue'
PATH = os.path.join(PATH_DIR, PATH_TEST, COLOR)
CATEGORIES = os.listdir(PATH)
sings_name = settings.signs_name_blue


def test_model(model):
    global IMG_SIZE, test_data
    good_recognized = 0
    bed_recognized = 0
    not_recognized = 0
    count_of_test_data = 0

    for CATEGORY in CATEGORIES:
        print(CATEGORY)
        path_to_images = os.path.join(PATH, CATEGORY)
        image_name_list = os.listdir(path_to_images)
        count_of_test_data += len(image_name_list)
        for image_name in image_name_list[:]:
            path_to_image = os.path.join(path_to_images, image_name)
            try:
                image = cv2.imread(path_to_image, cv2.IMREAD_GRAYSCALE)
                image = cv2.resize(image, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC)
                #cv2.imshow("sign", image)
                image = np.array(image).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
                prediction = model.predict(image)
                k = 0
                for j in range(count_of_class):
                    if prediction[0][j] >= 0.9997:
                        if int(CATEGORY.split(' ')[0]) == j:
                            good_recognized += 1
                        else:
                            bed_recognized += 1
                        #print(sings_name[j], prediction[0][j])
                    else:
                        k += 1
                if k == count_of_class:
                    not_recognized += 1

                #cv2.waitKey(0)

            except Exception as e:
                print(image_name, e)

    print("GOOD: {}% | BED: {}% | NOT_REC: {}%".format(int((good_recognized/count_of_test_data)*100),
                                                       int((bed_recognized/count_of_test_data)*100),
                                                       int((not_recognized/count_of_test_data)*100)))


NAME = "64x2-splot, 32x0-dense, scc-loss.model"
model = tf.keras.models.load_model("models/{}".format(NAME))
test_model(model)

""""""
path = '../images/im/'
for image in os.listdir(path):
    path_to_image = os.path.join(path, image)
    image = cv2.imread(path_to_image, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC)
    cv2.imshow("sign", image)
    image = np.array(image).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    prediction = model.predict(image)
    for j in range(count_of_class):
        if prediction[0][j] >= 0.5:
            print(sings_name[j],  prediction[0][j])
    cv2.waitKey(0)


cv2.destroyAllWindows()
