import cv2
import io
import numpy as np
from common import config
from utility import remote, os_path
from utility.local import storage
from cv.object_detection.yolo_backend import YOLOv4
from cv import feature_matching as fm
import pickle
from common.model import ShelfModel, ShelfProduct
from common.color import generate_colors


model = YOLOv4()


def slice_video(video, speed=10):
    slice_num = speed
    return video[0::slice_num]


def process_video(unpro_video):
    product_database = storage.get_feature_by_location_id(0)
    shelf_class = ShelfModel(unpro_video.inputId, [])

    video = remote.get_video(unpro_video.videoUrl)
    shelves = slice_video(video, unpro_video.scanSpeed)

    for shelf in shelves:
        results = model.detectImgCoord(shelf)
        image_path = os_path.save_images(config.TEMP_IMAGES, shelf)
        shelf_product = ShelfProduct(image_path, 0, 0, [])

        for product, coords in results:
            product_id = fm.search_product(product, product_database)

            if product_id != -1:
                shelf_product.addProduct(product_id, f'{coords[0]} {coords[1]} {coords[2]} {coords[3]}')
            # else:
            #     unknown_database = storage.get_undetected_features_by_location_id(0)
            #     unknown_id = fm.search_product(product, unknown_database)

            #     if unknown_id == -1:
            #         storage.add_unknown_feature_by_location_id(0, product)
                
            #     # add to the db
            #     # TODO  

        shelf_class.addShelfProduct(shelf_product)
    
    remote.upload_shelf(shelf_class.to_dict())


    def process_image_poc(images):
        product_database = storage.get_feature_by_location_id(0)
        shelf_class = ShelfModel(1, [])

        for image_path, shelf in images:
            results = model.detectImgCoord(shelf)
            shelf_product = ShelfProduct(image_path, 0, 0, [])

            for product, coords in results:
                product_id = fm.search_product(product, product_database)

                if product_id != -1:
                    shelf_product.addProduct(product_id, f'{coords[0]} {coords[1]} {coords[2]} {coords[3]}')
                else:
                    # TODO
                    pass

            shelf_class.addShelfProduct(shelf_product)
        remote.upload_shelf(shelf_class.to_dict())


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


def adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")

	return cv2.LUT(image, table)


def highlight_img(img, product_coords):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    darken_img = adjust_gamma(img, .25)
    h, w, _ = img.shape
    colors = generate_colors(len(product_coords))

    for product_coord, color in zip(product_coords, colors):
        coords = [[int(y) for y in x.split()] for x in product_coord]

        mask = np.zeros((h, w), dtype=np.uint8)
        for x1, y1, x2, y2 in coords:
            mask[x1:x2, y1:y2] = 255
            darken_img[x1:x2, y1:y2] = img[x1:x2, y1:y2]

        _, binary = cv2.threshold(mask, 40, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        for con in contours:
            cv2.drawContours(darken_img, con, -1, color, 2)

    return io.BytesIO(cv2.imencode('.jpg', darken_img)[1])

# def bytes_to_img(binary):
#     return cv2.imdecode(np.fromstring(binary, np.uint8), cv2.IMREAD_UNCHANGED)


# def img_to_bytes(img):
#     return cv2.imencode('.jpg', img)[1].tostring()