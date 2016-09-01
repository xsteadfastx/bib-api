import os
import redis

from flask import Flask, g
from flask_bootstrap import Bootstrap

from app.facility_loader import load_facilities
from app.mod_api import mod_api
from app.mod_frontend import mod_frontend


def create_app(config_filename):
    """Creates and initialize app.

    :param config_filename: Config to load.
    :type config_filename: str
    :return: App
    :rtype:flask.app.Flask: App
    """
    app = Flask(__name__)

    # extensions
    Bootstrap(app)

    # configuration
    app.config.from_pyfile(config_filename)

    if 'REDIS_PORT_6379_TCP_ADDR' not in os.environ.keys():
        os.environ['REDIS_PORT_6379_TCP_ADDR'] = 'localhost'

    # logging
    if not app.debug:
        import logging
        # loading this actually sets the logger up
        from app.logger import HANDLER

        app.logger.addHandler(HANDLER)
        app.logger.setLevel(logging.DEBUG)

    # register blueprints
    app.register_blueprint(mod_frontend)
    app.register_blueprint(mod_api, url_prefix='/api')

    # create redis connection before every request
    @app.before_request
    def before_request():
        g.redis = redis.StrictRedis(
            host=os.environ['REDIS_PORT_6379_TCP_ADDR'])

    # add facilities
    app.facilities = load_facilities()

    return app
