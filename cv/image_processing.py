import io
import cv2
import numpy as np
from common.color import generate_colors


def _adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")

	return cv2.LUT(image, table)


def _rect_distance(rec1, rec2):
    x1, y1, x1b, y1b = rec1
    x2, y2, x2b, y2b = rec2

    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2

    if top or bottom:
        return float('inf')

    if left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    else:
        return 0.


def _isNearby(rec1, rec2):
    return _rect_distance(rec1, rec2) <= 100


def _groupRectangle(rec1, rec2):
    rec_l, rec_r = sorted([rec1, rec2], key=lambda x: x[0])
    return [rec_l[0], rec_l[1], rec_r[2], rec_r[3]]


def _getOverLappedIndex(rec, rectangles):
    for i in range(len(rectangles)):
        if _isNearby(rec, rectangles[i]):
            return i
    
    return -1


def _joinRectangles(rectangles):
    grouped_rectangles = []

    for rec in rectangles:
        overlappedIndex = _getOverLappedIndex(rec, grouped_rectangles)
        if overlappedIndex == -1:
            grouped_rectangles.append(rec)
        else:
            grouped_rectangles[overlappedIndex] = _groupRectangle(rec, grouped_rectangles[overlappedIndex])

    return grouped_rectangles


def _groupHighlightImage(img, product_coords, colors):
    darken_img = _adjust_gamma(img, .25)
    h, w, _ = img.shape
    result = {i: [[int(z) for z in y.split()] for y in x] for i, x in enumerate(product_coords)}
    joined_result = {}

    for label in result:
        rectangles = result[label]
        joined_rectangles = _joinRectangles(rectangles)
        joined_result[label] = joined_rectangles

    for label in joined_result:
        color = colors[label]
        coords = joined_result[label]
        mask = np.zeros((h, w), dtype=np.uint8)

        for x1, y1, x2, y2 in coords:
            mask[y1:y2, x1:x2] = 255
            darken_img[y1:y2, x1:x2] = img[y1:y2, x1:x2]

        _, binary = cv2.threshold(mask, 40, 255, cv2.THRESH_BINARY)
        countours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        for con in countours:
            cv2.drawContours(darken_img, con, -1, color, 3)

    return io.BytesIO(cv2.imencode('.jpg', darken_img)[1])

def _highlightImage(img, product_coords, colors):
    darken_img = _adjust_gamma(img, .25)
    h, w, _ = img.shape

    for product_coord, color in zip(product_coords, colors):
        coords = [[int(y) for y in x.split()] for x in product_coord]

        mask = np.zeros((h, w), dtype=np.uint8)
        for x1, y1, x2, y2 in coords:
            mask[y1:y2, x1:x2] = 255
            darken_img[y1:y2, x1:x2] = img[y1:y2, x1:x2]

        _, binary = cv2.threshold(mask, 40, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        for con in contours:
            cv2.drawContours(darken_img, con, -1, color, 2)

    return io.BytesIO(cv2.imencode('.jpg', darken_img)[1])


def highlight_img(img, product_coords, isGrouped):
    colors = generate_colors(len(product_coords))

    if isGrouped:
        return _groupHighlightImage(img, product_coords, colors)
    else:
        return _highlightImage(img, product_coords, colors)