import os
from common.shared import config
from common.shared import secret
from flask import Flask
from common.utility import remote
from common.utility.local import LocalStorage
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn=secret.SENTRY_DNS,
#     integrations=[FlaskIntegration()],
#     traces_sample_rate=1.0
# )
app = Flask(config.WEB_NAME)

@app.route('/')
def index():
    # local = LocalStorage()
    # local.get_features()
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)
