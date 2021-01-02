import numpy as np
import cv2

def separate_video(video, log, distance=2):
    # TODO - given the video, separate video into images by distance
    pass


def bytes_to_img(binary):
    return cv2.imdecode(np.fromstring(binary, np.uint8), cv2.IMREAD_UNCHANGED)


def slice_video(video, distance=2):
    # TODO Slice video into list of images by 2 meters
    pass


def detect_products(img):
    # TODO given an image -> detect products and return list of products
    pass