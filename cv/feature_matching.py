import os
import cv2
import imutils
import numpy as np
from common import config
from cv.embbed_model import model as emb_model
from cv import annoy_model as am
from utility.local import storage

detector = cv2.ORB_create(config.ORB_NUM)
matcher = cv2.FlannBasedMatcher(config.INDEX_PARAMS, config.SEARCH_PARAMS)

def get_white_image(shape, value=config.WHITE):
    return np.full(shape, value, np.uint8)


def resize_white(img, shape=config.FX_IMAGE_SIZE):
    h, w, _ = img.shape
    resized_img = None

    if w > h:
        resized_img = imutils.resize(img, width=shape[0])
    else:
        resized_img = imutils.resize(img, height=shape[0])

    new_img = get_white_image(shape)

    org_h, org_w, _ = resized_img.shape
    new_h, new_w, _ = new_img.shape

    y_off = round((new_h-org_h) / 2)
    x_off = round((new_w-org_w) / 2)

    new_img[y_off:y_off+org_h, x_off:x_off+org_w] = resized_img
    return new_img


def compute_features(img):
    img = resize_white(img)
    kp, desc = detector.detectAndCompute(img, None)
    return kp, desc

def compute_emb_features(images):
    images = [resize_white(x) for x in images]
    return emb_model.predict_multiple(images)

def compute_emb_featue(img):
    img = resize_white(img, shape=config.EMB_INPUT_SHAPE)
    return emb_model.predict(img)


def compute_distance(kp1, desc1, kp2, desc2):
    matches = matcher.knnMatch(desc1, desc2, 2)
    good_matches = [m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * config.RATIO]

    if len(good_matches) > config.MIN_MATCH:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches])
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches])
        mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.)

        if mask.sum() > config.MIN_MATCH:
            return float(mask.sum()) / mask.size
        else:
            return 0.
    else:
        return 0.


def search_product(img, database):
    best_match = -1
    mx_acc = 0

    kp1, desc1 = compute_features(img)

    for product_id, _, feature in database:
        kp2, desc2 = feature
        accuracy = compute_distance(kp1, desc1, kp2, desc2)

        if accuracy > mx_acc:
            mx_acc = accuracy
            best_match = product_id

    return best_match


def search_product_emb(img, locationId):
    productIds = am.find_annoy(emb_model.predict(img), locationId)
    product_db = storage.get_feature_by_product_ids(productIds)
    result_id = search_product(img, product_db)

    return result_id


def get_features_by_path(path):
    return [[int(x.split('.')[0]) , 0, compute_features(cv2.imread(f'{config.FEATURE_PATH}/{path}/{x}'))] for x in os.listdir(f'{config.FEATURE_PATH}/{path}')]