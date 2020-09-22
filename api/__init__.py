import os
import inspect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.config import config

from api.model.Orders import db
# db = SQLAlchemy()

def create_app(test_config=None):
    """
    The flask application factory. To run the app somewhere else you can:
    ```
    from api import create_app
    app = create_app()

    if __main__ == "__name__":
        app.run()
    ```
    For testing, you can inject config values like:
    create_app({'KEY1': 'val1', 'KEY2': 'val2'})
    """
    app = Flask(__name__)
    app.testing = False

    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")
    # for configuration options, look at api/config.py
    if test_config:
        # purposely done so we can inject test configurations
        # this may be used as well if you'd like to pass
        # in a separate configuration although I would recommend
        # adding/changing it in api/config.py instead
        # ignore environment variable config if config was given
        app.config.from_mapping(**test_config)
    else:
        # config dict is from api/config.py
        app.config.from_object(config[env])

    app.config.from_pyfile('config.ini')  # config dict is from api/config.py
    db.init_app(app)
    # attach routes and custom error pages here

    from api.errors.blueprint import errors
    app.register_blueprint(errors)
    from api.checks.blueprint import checks
    app.register_blueprint(checks, url_prefix='/checks')
    from api.orders.blueprint import orders
    app.register_blueprint(orders, url_prefix='/orders')

    return app
