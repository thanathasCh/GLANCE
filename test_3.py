import os
import cv2
from utility import remote

base_url = 'https://glancevault.blob.core.windows.net/glanceblobs/POCimages/'
# _images_path = [
#     'R1S1.1',
#     'R1S1.2',
#     'R1S2.1',
#     'R1S2.2',
#     'R1S3.1',
#     'R1S3.2',
#     'R1S4.1',
#     'R1S4.2',
#     'R1S4.3',
#     'R1S5.1',
#     'R1S5.2',
#     'R1S5.3',
#     'R1S6.1',
#     'R1S6.2',
#     'R1S6.3',
#     'R1S7.1',
#     'R1S7.2',
#     'R1S8.1',
#     'R1S8.2',
#     'R1S9.1',
#     'R1S9.2'
# ]
_images_path = [
    'R1S1.1',
    'R1S5.2',
    'R1S7.1'
]

for index, i in enumerate(_images_path):
    full_path = base_url + i + '.jpg'
    img = remote.get_image(full_path)
    cv2.imwrite(f'test_db/{index}.jpg', img)