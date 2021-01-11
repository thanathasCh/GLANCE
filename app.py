import os
from common import config
from common import secret
from flask import Flask, request
from utility import remote
from utility.local import storage
from utility import background
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(config.WEB_NAME)

@app.route('/')
def index():
    return 'Hello World'


@app.route('/add_images', methods=['POST'])
def add_images():
    try:
        ids = request.get_json()[ids]
        images = remote.get_images(ids)
        storage.add_feature(ids, images)
    except:
        return 'failed'
    return 'finished'


@app.route('/update_images', methods=['POST'])
def update_images():
    try:
        ids = request.get_json()[ids]
        images = remote.get_images(ids)
        storage.update_feature(ids, images)
    except:
        return 'failed'
    return 'finished'


@app.route('/delete_images', methods=['POST'])
def delete_images():
    try:
        ids = request.get_json()[ids]
        images = remote.get_images(ids)
        storage.delete_features(ids, images)
    except:
        return 'failed'
    return 'finished'


# sentry_sdk.init(
#     dsn=secret.SENTRY_DNS,
#     integrations=[FlaskIntegration()],
#     traces_sample_rate=1.0
# )

app.run(debug=True)