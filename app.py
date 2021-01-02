import os
from common.shared import config
from flask import Flask
from common.utility import remote


app = Flask(config.WEB_NAME)

@app.route('/')
def index():
    remote.get_image()
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
