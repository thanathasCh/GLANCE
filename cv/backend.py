import cv2
import numpy as np
from common import config
from utility import remote, os_path
from utility.local import storage
from cv.object_detection.yolo_backend import YOLOv4
from cv import feature_matching as fm
import pickle
from common.model import ShelfModel, ShelfProduct, class2dict


model = YOLOv4()


def slice_video(video, speed=10):
    # TODO Check blur and calculate slice_num  
    slice_num = speed
    return video[0::slice_num]


def process_video(unpro_video):
    product_database = storage.get_feature_by_location_id(0)
    shelf_class = ShelfModel(unpro_video.inputId, [])

    video = remote.get_video(unpro_video.videoUrl)
    shelves = slice_video(video, unpro_video.scanSpeed)

    for shelf in shelves:
        results = model.detectImgCoord(shelf)
        image_path = os_path.save_images(config.TEMP_IMAGES)
        shelf_product = ShelfProduct(image_path, 0, 0, [])

        for product, coords in results:
            product_id = fm.search_product(product, product_database)

            if product_id != -1:
                shelf_product.addProduct(product_id, f'{coords[0]} {coords[1]} {coords[2]} {coords[3]}')
            # else:
                # unknown_database = storage.get_undetected_features_by_location_id(0)
                # unknown_id = fm.search_product(product, unknown_database)

                # if unknown_id == -1:
                #     # add to storage
                #     pass
                
                # # add to the db
                # # TODO  

        shelf_class.addShelfProduct(shelf_product)
    
    remote.upload_shelf(class2dict(shelf_class))


def process_feature(image):
    return fm.compute_features(image)


def feature_to_pickle(kp, desc):
    kp_data = [(x.pt, x.size, x.angle, x.response, x.octave, x.class_id) for x in kp]
    return pickle.dumps((kp_data, desc), 0)


def pickle_to_feature(binary):
    data = pickle.loads(binary)
    kp = [cv2.KeyPoint(x=x[0][0], y=x[0][1], _size=x[1], _angle=x[2], _response=x[3], _octave=x[4], _class_id=x[5]) for x in data[0]]
    desc = data[1]
    
    return kp, desc


# def bytes_to_img(binary):
#     return cv2.imdecode(np.fromstring(binary, np.uint8), cv2.IMREAD_UNCHANGED)


# def img_to_bytes(img):
#     return cv2.imencode('.jpg', img)[1].tostring()