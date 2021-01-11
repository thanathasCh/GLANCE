import cv2
import imutils
import numpy as np
from common import config

detector = cv2.ORB_create(config.ORB_NUM)
matcher = cv2.FlannBasedMatcher(config.INDEX_PARAMS, config.SEARCH_PARAMS)


def compute_features(img):
    img = resize_white(img)
    kp, desc = detector.detectAndCompute(img, None)
    return kp, desc


def compute_distance():
    pass


def search_product(target, database):
    # TODO create instance base
    # kp1, desc2 = compute_features(target)

    # for db in database:
    #     matches = matcher.knnMatch(desc1, desc2, 2)
    #     good_matches = [m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * ratio]

    #     if len(good_matches) > config.MIN_MATCH:
    #         src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    #         dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches])
    #         mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.)
    #         accuracy = float(mask.sum()) / mask.size

    #         if mask.sum() > config.MIN_MATCH:
    return -1
