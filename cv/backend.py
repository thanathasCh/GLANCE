from utility import remote
from utility.local import storage
from cv import preprocess
from cv.object_detection.yolo_backend import YOLOv4
from cv.feature_matching import search_product

model = YOLOv4()

def process_video(video_urls, location_id):
    product_database = storage.get_feature_by_location_id(location_id)
    video = remote.get_video(video_urls)
    images = preprocess.slice_video(video)

    product_list = []
    for image in images:
        results = model.detectImgCoord(images)

        for product, coords in results:
            product_id = search_product(product, product_database)
            product_list.append([product_id, coords])

    remote.upload_images(product_list)


def process_features(images):
    pass