import requests
import cv2
from utility import remote
from tqdm import tqdm

url = 'https://glance-api.azurewebsites.net/api/v1/Operation/listallproducts'

response = requests.get(url)
data = response.json()

for x in tqdm(data):
    id = x['id']
    imageUrl = x['imageUrl']

    try:
        img = remote.get_image(imageUrl)
        cv2.imwrite(f'test_db/sub/{id}.jpg', img)
    except:
        print(imageUrl)