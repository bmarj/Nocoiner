import os
# import inspect
from flask import Flask

from api.config import config
from api.utils import template_filters
from flask_migrate import Migrate
from api.models.model_base import db
from api.models.schema_base import ma
from api.user_management import um
# db = SQLAlchemy()
# ma = Marshmallow()
# login_manager = LoginManager()

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
    # setting default environment to production as a fail-safe
    env = os.environ.get("FLASK_ENV", "production")
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

    template_filters.init_app(app)

    # Flask-SQLAlchemy must be initialized before Flask-Marshmallow.
    db.init_app(app)
    ma.init_app(app)
    um.init_app(app)
    # attach routes and custom error pages here

    # from api import errors, monitor, orders, order_lines
    # app.register_blueprint(errors.bp)
    # app.register_blueprint(monitor.bp, url_prefix='/monitor')
    # app.register_blueprint(orders.bp, url_prefix='/orders')
    # app.register_blueprint(order_lines.bp, url_prefix='/order_lines')

    from api import reporting
    app.register_blueprint(reporting.bp, url_prefix='/reporting')

    # enable migrations with Flask-migrate and Alembic
    migrate = Migrate(app, db)

    return app
