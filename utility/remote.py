import os
import requests
import cv2
import json
from common import api_path
from utility import log
from skimage import io as imageIO
from common.model import VideoResponse

def _validate_status(response):
    if response.status_code:
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

        cv2.imshow('frame', frame)
        video.append(frame)
    
    vcap.release()
    
    return video


def upload_shelf(data):
    response = requests.post(api_path.insert_shelf_products, json=data)
    _validate_status(response)


def get_image(path):
    return imageIO.imread(path)


def get_images(paths):
    return [imageIO.imread(path) for path in paths]


def get_unprocessed_product():
    response = requests.get(api_path.list_unprocessed_products)
    
    if not _validate_status(response):
        return None

    return response.json()