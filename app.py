import os
import io
from common import config
from common import secret
from flask import Flask, request, send_file
from cv import backend
from utility import background, remote
from utility.local import storage
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(config.WEB_NAME)

@app.route('/')
def index():
    return 'Done'

@app.route('/load-products')
def load_products():
    try:
        imagePaths = remote.get_unprocessed_product()

        for imagePath in imagePaths:
            image = remote.get_image(imagePath['imageUrl'])
            kp, desc = backend.process_feature(image)
            storage.add_feature(imagePath['id'], 0, kp, desc)

        return 'finished'
    except:
        return 'failed'


@app.route('/highlight-image', methods=['POST'])
def highlight_image():
    data = request.get_json()
    img = remote.get_image(data['imageUrl'])
    product_coords = data['productCoords']
    highlighted_img = backend.highlight_img(img, product_coords)

    return send_file(highlighted_img, mimetype='image/jpeg', as_attachment=True, attachment_filename='image.jpg')


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
app.run(debug=True)