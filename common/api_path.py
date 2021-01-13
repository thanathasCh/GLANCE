from urllib.parse import urljoin

# Base Url
_glance_base_url = 'https://glance-api.azurewebsites.net/api/v1/Operation/'


upload_input = urljoin(_glance_base_url, 'UploadInput')
list_unprocessed_videos = urljoin(_glance_base_url, 'ListUnprocessedInput')
upload_product = urljoin(_glance_base_url, 'UploadProduct')
list_unprocessed_products = urljoin(_glance_base_url, 'ListUnprocessedProducts')
insert_shelf = urljoin(_glance_base_url, 'InsertShelf')
insert_shelf_products = urljoin(_glance_base_url, 'InsertShelfProducts')
upload_undetected_product = urljoin(_glance_base_url, 'UploadUndetectedProduct')
list_undetected_product_features = urljoin(_glance_base_url, 'ListUndetectedProductFeatures')