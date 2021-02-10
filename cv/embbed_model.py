import tensorflow as tf
import numpy as np 
import random
import config
import cv2
import pickle

from random import shuffle
from common import config
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.applications import ResNet101V2, NASNetLarge
from tensorflow.keras.applications.resnet_v2 import preprocess_input

class EmbbedModel:
    def __init__(self):
        self.model = Sequential([
            NASNetLarge(weights='imagenet',
                        include_top=False,
                        input_tensor=Input(shape=config.FX_IMAGE_SIZE)),
            Flatten(),
            Dense(config.EMB_SIZE, activation=None)
        ])

    
    def predict_multiple(self, values):
        new_values = np.array(values).reshape(config.FX_IMAGE_SIZE_EMB)
        return self.model.predict(new_values)

    
    def predict(value):
        new_value = np.array([value]).reshape(config.FX_IMAGE_SIZE_EMB)
        return new_value[0]