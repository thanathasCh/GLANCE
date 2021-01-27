import pickle
import cv2
import io
from utility import remote

shelf_class, resized_shelves = pickle.load(open('saved2.data', 'rb'))

print(remote.upload_shelf(shelf_class.to_dict(), resized_shelves).content)
# print(shelf_class.to_dict())