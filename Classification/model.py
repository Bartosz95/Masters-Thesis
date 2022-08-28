from tensorflow import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.callbacks import TensorBoard
import Classification.settings as settings
import pickle
import numpy as np


def read_data(color):
    # Train data
    TRAIN = settings.PATH_TRAIN
    pickle_in = open("data/{}_X_{}.pickle".format(color, TRAIN), "rb")
    x_train = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open("data/{}_Y_{}.pickle".format(color, TRAIN), "rb")
    y_train = pickle.load(pickle_in)
    pickle_in.close()

    # Test data
    TEST = settings.PATH_TEST
    pickle_in = open("data/{}_X_{}.pickle".format(color, TEST), "rb")
    x_test = pickle.load(pickle_in)
    pickle_in.close()
    pickle_in = open("data/{}_Y_{}.pickle".format(color, TEST), "rb")
    y_test = pickle.load(pickle_in)
    pickle_in.close()
    return x_train, y_train, x_test, y_test


def learn_model(x_train, y_train, x_test, y_test, color):
    if color == 'blue':
        COUNT_OF_CLASSES = settings.COUNT_OF_CLASSES_BLUE
    elif color == 'red':
        COUNT_OF_CLASSES = settings.COUNT_OF_CLASSES_RED
    elif color == 'yellow':
        COUNT_OF_CLASSES = settings.COUNT_OF_CLASSES_YELLOW

    # tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))

    model = Sequential()

    model.add(Conv2D(filters=64,
                     kernel_size=(3, 3),
                     input_shape=x_train.shape[1:],
                     activation=tf.nn.relu)
              )
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())

    model.add(Dense(64, activation=tf.nn.relu))
    model.add(Dense(64, activation=tf.nn.relu))
    model.add(Dense(32, activation=tf.nn.relu))
    model.add(Dense(COUNT_OF_CLASSES, activation=tf.nn.sigmoid))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy']
                  )

    model.fit(x=np.array(x_train), y=np.array(y_train),
              epochs=10,
              shuffle=True,
              # callbacks=[tensorboard],
              validation_data=(np.array(x_test), np.array(y_test))
              )

    return model


model_name = settings.model_name
colors = ['blue', 'red', 'yellow'] #
for color in colors:
    x_train, y_train, x_test, y_test = read_data(color)
    model = learn_model(x_train, y_train, x_test, y_test, color)
    model.save('models/{}_{}.model'.format(color, model_name))
