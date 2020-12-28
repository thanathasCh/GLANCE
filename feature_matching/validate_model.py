import os

from numpy.core.defchararray import encode
import cv2
import numpy as np
from tqdm import tqdm
from tensorflow.keras.applications import ResNet50V2, ResNet101V2, VGG16, VGG19
from tensorflow.keras.applications.resnet_v2 import preprocess_input as resnet_pre_input
from tensorflow.keras.applications.vgg16 import preprocess_input as vgg16_pre_input
from tensorflow.keras.applications.vgg19 import preprocess_input as vgg19_pre_input

DB_PATH = 'database'
VAL_PATH = 'validation'
TARGET_SIZE = (244, 244)

def img_to_features(img, preprocess_input, model):
    image_data = cv2.resize(img, TARGET_SIZE)
    image_data = np.expand_dims(image_data, axis=0)
    image_data = preprocess_input(image_data)
    return model.predict(image_data).flatten()


# models = [ResNet50, ResNet]

resNet50 = ResNet50V2(weights='imagenet', include_top=False)
# resNet101 = ResNet101V2(weights='imagenet', include_top=False)
# vgg16 = VGG16(weights='imagenet', include_top=False)
# vgg19 = VGG19(weights='imagenet', include_top=False)

database = [[cv2.resize(cv2.imread(f'{DB_PATH}/{x}'), TARGET_SIZE), int(x.split('.')[0])] for x in os.listdir(VAL_PATH)]
validation = [[cv2.resize(cv2.imread(f'{VAL_PATH}/{x}'), TARGET_SIZE), int(x.split('.')[0])] for x in os.listdir(DB_PATH)]

# for i in validation:
#     print(i[0].shape)
results = []
objects_to_compare = [img_to_features(x[0], resnet_pre_input, resNet50) for x in database]

for img, label in validation:
    encoded_img = img_to_features(img, resnet_pre_input, resNet50)
    # distances = []
    for each_image in objects_to_compare:
        print(np.linalg.norm(encoded_img - each_image))
        # distances.append(np.linalg.norm(encoded_img - each_image))
    input('<>...')
    # object_distances = np.linalg.norm(objects_to_compare - encoded_img, axis=1)
    # print(object_distances)
    # input('>..')
    # result from comparing suppose to be within 0 to 1
    # match_result = list(object_distances <= 0.6)
    # match_image_index = np.argmin(match_result)
    # results.append([img, database[match_image_index][0]])


# for org, match in results:
#     cv2.imshow('org', org)
#     cv2.imshow('match', match)
#     cv2.waitKey()