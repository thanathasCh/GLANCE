import cv2
import numpy as np

def bytes_to_img(binary):
    return cv2.imdecode(np.fromstring(binary, np.uint8), cv2.IMREAD_UNCHANGED)