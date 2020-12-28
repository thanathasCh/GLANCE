import cv2
import backend
import numpy as np 
import os
import imutils

for orgPath in os.listdir('validation'):
    org = backend.resize_white(cv2.imread(f'validation/{orgPath}'))

    res = None
    min_match = 10
    ratio = .75
    detector = cv2.ORB_create(1000)
    index_params = dict(algorithm = 6,
                        table_number = 6,
                        key_size = 12,
                        multi_probe_level = 1)
    search_params = dict(checks=32)
    matcher = cv2.FlannBasedMatcher(index_params, search_params)

    gray1 = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
    kp1, desc1 = detector.detectAndCompute(gray1, None)

    image_score = []

    for imgPath in os.listdir('database'):
        compare_img = backend.resize_white(cv2.imread(f'database/{imgPath}'))
        gray2 = cv2.cvtColor(compare_img, cv2.COLOR_BGR2GRAY)
        kp2, desc2 = detector.detectAndCompute(gray2, None)
        matches = matcher.knnMatch(desc1, desc2, 2)

        good_matches = [m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * ratio]

        if len(good_matches) > min_match:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches])
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches])

            mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.)
            accuracy = float(mask.sum()) / mask.size

            # if mask.sum() > min_match:
            #     matchesMask = mask.ravel().tolist()
            #     h, w, _ = org.shape
            #     pts = np.float32([[[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]]])
            #     dst = cv2.perspectiveTransform(pts, mtrx)
            #     compare = cv2.polylines(compare_img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            #     res = cv2.drawMatches(org, kp1, compare_img, kp2, good_matches, None, matchesMask=matchesMask,
            #                             flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

            image_score.append([compare_img, accuracy])

    image_score.sort(key=lambda x: x[1], reverse=True)

    stacked_img = org
    for i in range(len(image_score)):
        if stacked_img is None:
            stacked_img = image_score[i][0]
        else:
            stacked_img = np.concatenate([stacked_img, image_score[i][0]], axis=0)
        print(stacked_img.shape)

    stacked_img = imutils.resize(stacked_img, height=500)
    cv2.imshow('a', stacked_img)
    cv2.waitKey()