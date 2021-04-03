import cv2
import imutils
import io
import numpy as np
from common import config
from utility import remote
from utility.local import storage
from cv.object_detection.yolo_backend import YOLOv4
from cv import feature_matching as fm
import pickle
from common.model import ShelfModel, ShelfProduct
from common.color import generate_colors
from tqdm import tqdm
from cv import annoy_model
from cv.embbed_model import model as emb_model


model = YOLOv4()


def slice_video(video, speed=10):
    slice_num = speed
    return video[0::slice_num]


def img_to_bytes(img):
    return io.BytesIO(cv2.imencode('.jpg', img)[1])


# def process_video(unpro_video):
#     product_database = storage.get_feature_by_location_id(0)
#     shelf_class = ShelfModel(unpro_video.inputId, [])

#     video = remote.get_video(unpro_video.videoUrl)
#     shelves = slice_video(video, unpro_video.scanSpeed)

#     for shelf in shelves:
#         results = model.detectImgCoord(shelf)
#         shelf_product = ShelfProduct(image_path, 0, 0, [])

#         for product, coords in results:
#             product_id = fm.search_product(product, product_database)

#             if product_id != -1:
#                 shelf_product.addProduct(product_id, f'{coords[0][0]} {coords[0][1]} {coords[1][0]} {coords[1][1]}')
#             # else:
#             #     unknown_database = storage.get_undetected_features_by_location_id(0)
#             #     unknown_id = fm.search_product(product, unknown_database)

#             #     if unknown_id == -1:
#             #         storage.add_unknown_feature_by_location_id(0, product)
                
#             #     # add to the db
#             #     # TODO  

#         shelf_class.addShelfProduct(shelf_product)
#     remote.upload_shelf(shelf_class.to_dict())


def process_image_poc(images):
    shelf_class = ShelfModel(1, [])
    resized_shelves = []

    for image_path, shelf in tqdm(images):
        resized_shelf = imutils.resize(shelf, width=1980)
        resized_shelves.append(img_to_bytes(resized_shelf))
        results = model.detectImgCoord(resized_shelf)
        shelf_product = ShelfProduct(int(image_path[-9]), int(image_path[-7]), int(image_path[-5]), [])
        product_database = fm.get_features_by_path(image_path[-10:-4])

        for product, coords in results:
            product_id = fm.search_product(product, product_database)
            if product_id != -1:
                shelf_product.addProduct(product_id, f'{coords[0][0]} {coords[0][1]} {coords[1][0]} {coords[1][1]}')
            else:
                pass

        shelf_class.addShelfProduct(shelf_product)
    # print(shelf_class.to_dict())
    print(remote.upload_shelf(shelf_class.to_dict(), resized_shelves).content)


def process_image_emb_poc(inputId, images):
    shelf_class = ShelfModel(inputId, [])
    resized_shelves = []
    location_id = 0

    for image_path, shelf in tqdm(images):
        resized_shelf = imutils.resize(shelf, width=1980)
        resized_shelves.append(img_to_bytes(resized_shelf))
        results = model.detectImgCoord(resized_shelf)
        shelf_product = ShelfProduct(int(image_path[-9]), int(image_path[-7]), int(image_path[-5]), [])
        
        for product, coords in results:
            product_id = fm.search_product_emb(product, location_id)
            if product_id != -1:
                shelf_product.addProduct(product_id, f'{coords[0][0]} {coords[0][1]} {coords[1][0]} {coords[1][1]}')
            else:
                pass

        shelf_class.addShelfProduct(shelf_product)

    # print(shelf_class.to_dict())
    print(remote.upload_shelf(shelf_class.to_dict(), resized_shelves).content)


def process_feature(image):
    return fm.compute_features(image)


def add_fm_db(product_id, location_id, image):
    kp, desc = process_feature(image)
    storage.add_feature(product_id, location_id, kp, desc)


def create_annoty_db(ids, images, locationId):
    features = emb_model.predict_multiple(images)
    annoy_model.create_model(ids, features, locationId)


def feature_to_pickle(kp, desc):
    kp_data = [(x.pt, x.size, x.angle, x.response, x.octave, x.class_id) for x in kp]
    return pickle.dumps((kp_data, desc), 0)


def pickle_to_feature(binary):
    data = pickle.loads(binary)
    kp = [cv2.KeyPoint(x=x[0][0], y=x[0][1], _size=x[1], _angle=x[2], _response=x[3], _octave=x[4], _class_id=x[5]) for x in data[0]]
    desc = data[1]
    
    return kp, desc


def get_colors(count):
    return generate_colors(count)


def convert_color_to_hex(color):
    return '#%02x%02x%02x' % (color[2], color[1], color[0])

# def bytes_to_img(binary):
#     return cv2.imdecode(np.fromstring(binary, np.uint8), cv2.IMREAD_UNCHANGED)