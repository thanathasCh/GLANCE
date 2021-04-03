import os
import io
from common import config
from common import secret
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from cv import backend
from cv import image_processing as ip
from utility import background, remote
from utility.local import storage
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegratio

app = Flask(config.WEB_NAME)
CORS(app, support_credential=True)
    

@app.route('/')
def test():
    return 'Test'


@app.route('/demo')
def demo():
    data = request.get_json()
    inputId = data['inputId']
    imageUrls = data['imageUrls']
    background.run_demo(inputId, imageUrls)

    return 'Done'

@app.route('/test-model')
def embed_model():
    background._check_tasks_embed_model()
    return 'Done'

@app.route('/test-poc')
def index():
    background._check_tasks_poc()
    return 'Done'


@app.route('/load-products')
def load_products():
    # imagePaths = remote.get_unprocessed_product()
    imagePaths = remote.get_products_by_shelf(1)
    productIds = []
    productImages = []

    for imagePath in imagePaths:
        product_id = imagePath['id']

        try:
            image = remote.get_image(imagePath['imageUrl'])
        except:
            continue

        # productIds.append(product_id)
        # productImages.append(image)
        # backend.add_fm_db(product_id, 0, image)

        for rImg in ip.rotateImg(image):
            productIds.append(product_id)
            productImages.append(rImg)
            backend.add_fm_db(product_id, 0, rImg)


    backend.create_annoty_db(productIds, productImages, 0)
    remote.update_product_status(productIds)

    return 'finished'


@app.route('/highlight-image', methods=['POST'])
def highlight_image():
    data = request.get_json()
    
    img = remote.get_image(data['imageUrl'])
    isGrouped = data['isGrouped']
    product_coords = data['productCoords']
    highlighted_img = ip.highlight_img(img, product_coords, isGrouped)

    return send_file(highlighted_img, mimetype='image/jpeg', as_attachment=True, attachment_filename='image.jpg')


@app.route('/get-colors/<int:count>')
def get_colors(count):
    colors = [backend.convert_color_to_hex(x) for x in backend.get_colors(count)]
    return jsonify(colors)


@app.route('/get-colors-product', methods=['POST'])
def get_colors_product():
    product_ids = request.get_json()
    colors = [backend.convert_color_to_hex(x) for x in backend.get_colors(len(product_ids))]
    color_product_ids = [{'productId': id, 'color': color} for id, color in zip(product_ids, colors)]
    return jsonify(color_product_ids)

# @app.route('/add_images', methods=['POST'])
# def add_images():
#     try:
#         ids = request.get_json()['ids']
#         images = remote.get_images(ids)
#         storage.add_feature(ids, images)
#     except:
#         return 'failed'
#     return 'finished'


# @app.route('/update_images', methods=['POST'])
# def update_images():
#     try:
#         ids = request.get_json()[ids]
#         images = remote.get_images(ids)
#         storage.update_feature(ids, images)
#     except:
#         return 'failed'
#     return 'finished'


# @app.route('/delete_images', methods=['POST'])
# def delete_images():
#     try:
#         ids = request.get_json()[ids]
#         images = remote.get_images(ids)
#         storage.delete_features(ids, images)
#     except:
#         return 'failed'
#     return 'finished'



# sentry_sdk.init(
#     dsn=secret.SENTRY_DNS,
#     integrations=[FlaskIntegration()],
#     traces_sample_rate=1.0
# )

# background.start()
app.run(debug=False, port=4000)