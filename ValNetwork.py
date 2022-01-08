from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras import backend as K
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.optimizers import RMSprop
from keras import layers
import keras
from sklearn.model_selection import train_test_split
import numpy as np
import cv2
import pickle

class DLModel(object):
    def __init__(self, width, channel):
        self.input_shape = (channel, width, width)
        self.width = width
        self.NetworkModel()

    def NetworkModel(self):
        inputs = layers.Input(shape = self.input_shape)
        conv1 = layers.Conv2D(filters=32,kernel_size=(3,3),padding="same",kernel_initializer="he_normal",activation="relu")(inputs)
        conv2 = layers.Conv2D(filters=64,kernel_size=(3,3),padding="same",kernel_initializer="he_normal",activation="relu")(conv1)
        conv3 = layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same", kernel_initializer="he_normal",activation="relu")(conv2)
        
        conv4 = layers.Conv2D(filters = 4, kernel_size = (1,1), kernel_initializer="he_normal",activation="relu")(conv3)
        flat1 = Flatten()(conv4)
        policy_net = Dense(self.width * self.width + 1, activation="softmax")(flat1)
        
        conv5 = layers.Conv2D(filters = 2, kernel_size = (1,1), kernel_initializer="he_normal",activation="relu")(conv3)
        flat2 = Flatten()(conv5)
        dense = Dense(64)(flat2)
        value_net = Dense(1, activation="tanh")(dense)
        
        # self.policy_net = keras.models.Model(inputs = inputs,outputs = policy_net)
        # self.value_net = keras.models.Model(inputs = inputs, outputs = value_net)

        self.model = keras.models.Model(inputs = inputs, outputs = [policy_net, value_net])

    def TrainingProcess(self, x, y, num_epochs = 1):
        (x_train, x_test, y_pi_train, y_pi_test) = train_test_split(x, y[0], test_size = 0.2, random_state = 0)
        (x_train, x_test, y_z_train, y_z_test) = train_test_split(x, y[1], test_size = 0.2, random_state = 0)

        self.model.compile(optimizer='adam', loss=['categorical_crossentropy', 'mean_squared_error'])
        # self.model.compile(optimizer='adam', loss= 'mean_squared_error')
        self.model.fit(x_train, [y_pi_train, y_z_train], validation_data = (x_test, [y_pi_test, y_z_test]), epochs = num_epochs, batch_size = 1)
        # self.model.save_weights('modelCross.h5')
    
    def GetProbVal(self, x):
        x = np.array(x)
        x = x.reshape((1, 4, 6, 6))
        return self.model.predict_on_batch(x)


    def saveModel(self, stri):
        self.model.save_weights(stri)