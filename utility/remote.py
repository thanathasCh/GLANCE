import os
import requests
import cv2
import json
from common import api_path
from utility import log
from skimage import io as imageIO
from common.model import VideoResponse


def _validate_status(response):
    if response.status_code == 200:
        return True
    else:
        log.print_error(f'Error Code: {response.status_code}')
        return False


def check_process_queue():
    response = requests.get(api_path.list_unprocessed_videos)
    if not _validate_status(response):
        return None

    data = response.json()[0]
    return VideoResponse(data['inputId'], data['videoUrl'], data['scanSpeed'], data['scanDate'])


def get_video(url):
    video = []

    vcap = cv2.VideoCapture(url)

    while(1):
        ret, frame = vcap.read()
        if frame is None:
            break

        video.append(frame)
    
    vcap.release()
    
    return video


def upload_shelf(data, files):
    image_files = [('shelfImages', (f'{i}.jpg' ,x, 'image/jpeg')) for i, x in enumerate(files)]
    
    response = requests.post(api_path.insert_shelf_products, data=data, files=image_files)
    _validate_status(response)

    return response


def get_image(path):
    img = imageIO.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if path.split('.')[-1] == 'png':
        img = img[:,:,:3]

    return img


def get_images(paths):
    return [get_image(path) for path in paths]


def get_unprocessed_product():
    response = requests.get(api_path.list_unprocessed_products)
    
    if not _validate_status(response):
        return None

    return response.json()

 
def list_all_products():
    response = requests.get(api_path.list_all_products)
    _validate_status(response)

    data = []

    for i in response.json():
        id = i['id']
        url = i['imageUrl']
        try:
            data.append([id, get_image(url)])
        except:
            continue

    return data


def get_poc_shelf_images():
    return [[x, get_image(x)] for x in api_path.poc_image_path]


def get_full_poc_shelf_images():
    return [[x, get_image(x)] for x in api_path.full_poc_image_path]


def update_product_status(ids, status='PROCESSED'):
    data = {
        'status': status,
        'productIds': ids
    }

    response = requests.post(api_path.update_product_status, json=data)
    _validate_status(response)


def get_products_by_shelf(rowNumber):
    response = requests.get(api_path.get_products_by_shelf + str(rowNumber))
    _validate_status(response)

    return response.json()