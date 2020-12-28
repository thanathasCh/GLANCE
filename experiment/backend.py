import tensorflow as tf
import numpy as np 
import random
import config
import cv2
import pickle

from random import shuffle
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.applications import ResNet101V2
from tensorflow.keras.applications.resnet_v2 import preprocess_input

def load_test_data():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = np.array([cv2.cvtColor(cv2.resize(x, config.image_shape), cv2.COLOR_GRAY2RGB)/255. for x in x_train])
    x_test = np.array([cv2.cvtColor(cv2.resize(x, config.image_shape), cv2.COLOR_GRAY2RGB)/255. for x in x_test])

    return ((x_train, y_train), (x_test, y_test))


def load_data():
    data = pickle.load(open(config.data_file , 'rb'))
    shuffle(data)
    x_train, y_train = [], []
    
    for cls, img in data:
        try:
            x_train.append(cv2.resize(img, config.image_shape)/255.)
            y_train.append(cls)
        except:
            print('One image is empty.')

    return ((np.array(x_train), np.array(y_train)), ([], []))


def create_batch(x_train, y_train):
    x_anchors = np.zeros(config.batch_input_shape)
    x_positives = np.zeros(config.batch_input_shape)
    x_negatives = np.zeros(config.batch_input_shape)

    for i in range(0, config.batch_size):
        random_index = random.randint(0, x_train.shape[0] - 1)
        x_anchor = x_train[random_index]
        y = y_train[random_index]

        indices_for_pos = np.squeeze(np.where(y_train == y))
        indices_for_neg = np.squeeze(np.where(y_train != y))

        x_positive = x_train[indices_for_pos[random.randint(0, len(indices_for_pos) - 1)]]
        x_negative = x_train[indices_for_neg[random.randint(0, len(indices_for_neg) - 1)]]

        x_anchors[i] = x_anchor
        x_positives[i] = x_positive
        x_negatives[i] = x_negative

    return [x_anchors, x_positives, x_negatives]


def create_base_model(describe=False):
    res_model = ResNet101V2(weights='imagenet',
                            include_top=False,
                            input_tensor=Input(shape=config.input_shape))

    model = Sequential()
    model.add(res_model)
    model.add(Flatten())
    model.add(Dense(config.emb_size, activation='softmax'))

    return model


def create_siamese_network(describe=False):
    embedding_model = create_base_model()
    
    input_anchor = Input(shape=config.input_shape)
    input_positive = Input(shape=config.input_shape)
    input_negative = Input(shape=config.input_shape)

    embedding_anchor = embedding_model(input_anchor)
    embedding_positive = embedding_model(input_positive)
    embedding_negative = embedding_model(input_negative)

    output = concatenate([embedding_anchor, embedding_positive, embedding_negative], axis=1)

    net = Model([input_anchor, input_positive, input_negative], output)

    if describe:
        net.summary()

    return embedding_model, net


def triplet_loss(y_true, y_pred):
    anchor, positive, negative = y_pred[:,:config.emb_size], y_pred[:,config.emb_size:2*config.emb_size], y_pred[:,2*config.emb_size:]
    positive_dist = tf.reduce_mean(tf.square(anchor - positive), axis=1)
    negative_dist = tf.reduce_mean(tf.square(anchor - negative), axis=1)
    return tf.maximum(positive_dist - negative_dist + config.alpha, 0.)


def data_generator(x_train, y_train):
    while True:
        x = create_batch(x_train, y_train)
        y = np.zeros((config.batch_size, 3*config.emb_size))
        yield x, y

def get_callbacks():
    return [
        tf.keras.callbacks.TensorBoard(
            log_dir='logs',
            histogram_freq=0,
            write_graph=True,
            write_images=True,
            update_freq='epoch',
            profile_batch=2,
            embeddings_freq=0,
            embeddings_metadata=None
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath='checkpoints/weights-{epoch:08d}.h5',
            monitor='val_loss',
            verbose=False,
            save_weights_only=False,
            mode='auto',
            save_freq='epoch'
        )
    ]


def clear_logs(clear_checkpoint=False):
    import shutil
    import os

    shutil.rmtree('logs')
    os.mkdir('logs')

    if clear_checkpoint:
        shutil.rmtree('checkpoints')
        os.mkdir('checkpoints')