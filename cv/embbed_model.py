import numpy as np 
from random import shuffle
from common import config
from cv import feature_matching as fm
from tensorflow.keras.layers import Input, Flatten, Dense, concatenate
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet import preprocess_input

class EmbbedModel:
    def __init__(self):
        self.model = self._load_model()


    def _get_base_model(self):
        model = Sequential([
            ResNet50(weights='imagenet',
                     include_top=False,
                     input_tensor=Input(config.EMB_INPUT_SHAPE)),

            Flatten(),

            Dense(256, activation='relu'),

            Dense(128, activation='relu'),

            Dense(config.EMB_SIZE, activation=None)
        ])

        return model


    def _get_siamese_network(self):
        embedding_model = self._get_base_model()
    
        input_anchor = Input(shape=config.EMB_INPUT_SHAPE)
        input_positive = Input(shape=config.EMB_INPUT_SHAPE)
        input_negative = Input(shape=config.EMB_INPUT_SHAPE)

        embedding_anchor = embedding_model(input_anchor)
        embedding_positive = embedding_model(input_positive)
        embedding_negative = embedding_model(input_negative)

        output = concatenate([embedding_anchor, embedding_positive, embedding_negative], axis=1)

        net = Model([input_anchor, input_positive, input_negative], output)

        return embedding_model, net

    
    def _load_model(self):
        emb_model, model = self._get_siamese_network()
        model.load_weights(config.EMB_CHECKPOINT_PATH)

        return emb_model


    def predict_multiple(self, values):
        new_values = np.array([fm.resize_white(x, shape=config.EMB_INPUT_SHAPE) for x in values]).reshape(config.EMB_IMAGE_SIZE)
        return self.model.predict(new_values)

    
    def predict(self, value):
        new_value = np.array(fm.resize_white(value, shape=config.EMB_INPUT_SHAPE)).reshape(config.EMB_IMAGE_SIZE)
        return self.model.predict(new_value)[0]


model = EmbbedModel()