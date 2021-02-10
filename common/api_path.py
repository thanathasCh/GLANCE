from urllib.parse import urljoin

# Base Url
_glance_base_url = 'https://glance-api.azurewebsites.net/api/v1/Operation/'
_glance_poc_bucket = 'https://glancevault.blob.core.windows.net/glanceblobs/POCimages/'


upload_input = urljoin(_glance_base_url, 'UploadInput')
list_unprocessed_videos = urljoin(_glance_base_url, 'ListUnprocessedInput')
upload_product = urljoin(_glance_base_url, 'UploadProduct')
list_unprocessed_products = urljoin(_glance_base_url, 'ListUnprocessedProducts')
insert_shelf = urljoin(_glance_base_url, 'InsertShelf')
insert_shelf_products = urljoin(_glance_base_url, 'InsertShelfProducts')
upload_undetected_product = urljoin(_glance_base_url, 'UploadUndetectedProduct')
list_undetected_product_features = urljoin(_glance_base_url, 'ListUndetectedProductFeatures')
update_product_status = urljoin(_glance_base_url, 'UpdateProductsFeatureStatus')

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

poc_image_path = [f'{_glance_poc_bucket}{x}.jpg' for x in _images_path]