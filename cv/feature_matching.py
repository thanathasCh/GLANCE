import cv2
import imutils
import numpy as np
from common import config
detector = cv2.ORB_create(config.ORB_NUM)
matcher = cv2.FlannBasedMatcher(config.INDEX_PARAMS, config.SEARCH_PARAMS)


def get_white_image(shape=config.FX_IMAGE_SIZE, value=config.WHITE):
    return np.full(shape, value, np.uint8)


def resize_white(img):
    h, w, _ = img.shape
    resized_img = None

    if w > h:
        resized_img = imutils.resize(img, width=config.FX_INPUT_SIZE[0])
    else:
        resized_img = imutils.resize(img, height=config.FX_INPUT_SIZE[0])

    new_img = get_white_image()

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


def compute_distance(k1, desc1, kp2, desc2):
    matches = matcher.knnMatch(desc1, desc2, 2)
    good_matches = [m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * config.RATIO]

    if len(good_matches) > config.MIN_MATCH:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches])
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches])
        mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.)

        if mask.sum() > config.MIN_MATCH:
            return float(mask.sum()) / mask.BATCH_SIZE
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
        accuracy = compute_distance(k1, desc1, kp2, desc2)

        if accuracy > mx_acc:
            mx_acc = accuracy
            best_match = product_id

    return product_id
