import os
from common.shared import config
from flask import Flask
from common import provider

# from common.object_detection import YOLOv4
# from common.feature_matching import resize_white, get_white_image
from common import provider

app = Flask(config.WEB_NAME)

@app.route('/')
def index():
    provider.get_image()
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
