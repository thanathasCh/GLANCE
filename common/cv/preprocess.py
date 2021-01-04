import numpy as np
import cv2
from common.shared import config
from common.cv.object_detection.yolo_backend import YOLOv4

model = YOLOv4()

def bytes_to_img(binary):
    return cv2.imdecode(np.fromstring(binary, np.uint8), cv2.IMREAD_UNCHANGED)


def img_to_bytes(img):
    return cv2.imencode('.jpg', img)[1].tostring()


def slice_video(video, distance=2):
    fps = video.get(cv2.CAP_PROP_FPS)
    # TODO slide video into images


def detect_products(img):
    return model.detectImg(img)


def get_white_image(shape=config.FX_IMAGE_SIZE):
    return np.full(shape, config.WHITE, np.uint8)


def resize_white(img):
    h, w, _ = img.shape
    resized_img = None

    if w > h:
        resized_img = imutils.resize(img, width=config.FX_IMAGE_SIZE[0])
    else:
        resized_img = imutils.resize(img, height=config.FX_IMAGE_SIZE[0])

    new_img = get_white_image()
    
    org_h, org_w, _ = resized_img.shape
    new_h, new_w, _ = new_img.shape

    y_off = round((new_h-org_h) / 2)
    x_off = round((new_w-org_w) / 2)

    new_img[y_off:y_off+org_h, x_off:x_off+org_w] = resized_img

    return new_img