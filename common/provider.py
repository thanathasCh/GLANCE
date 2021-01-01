import requests
import cv2
from common.shared import api_path
from common.utility import image_utility, log


def validate_status(response):
    if response.status_code == 200:
        return True
    else:
        log.print_error(f'Error Code: {response.status_code}')
        return False


def check_database_queue():
    ''' 
    TODO - send request to check if there are any waiting queue in the database
            If exist 
                -> get the list of image url
            else-> get nothing
    '''
    pass


def get_video(url):
    # TODO - load video from given url
    pass


def upload_images(images):
    # TODO - upload images to the database with table information
    pass


def get_image(path=''):
    response = requests.get(api_path.TEST_BLOB)

    if not validate_status(response):
        return None
    
    return image_utility.bytes_to_img(response.content)