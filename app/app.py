from flask import Flask, g
import os
import redis
import sys


def load_facilities():
    """Facility loader.

    Its loading facilities from the facilitie directory. These are some kind
    of plugins in a way. Its used to for easily adding new libraries to the
    API.

    :return: Dictionary with functions to interact with libraries.
    :rtype: dict
    """
    facilities = {}

    facilities_path = os.path.dirname(
        os.path.realpath(__file__)) + '/facilities'
    sys.path.insert(0, facilities_path)

    for facility in os.listdir(facilities_path):

        fname, ext = os.path.splitext(facility)

        if ext == '.py':

            facilities[fname] = {}

            mod = __import__(fname)

            # load needed functions into the dict
            facilities[fname]['search'] = mod.search

    sys.path.pop(0)

    return facilities


def create_app(config_filename):
    """Creates and initialize app.

    :param config_filename: Config to load.
    :type config_filename: str
    :return: App
    :rtype:flask.app.Flask: App
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    if 'REDIS_PORT_6379_TCP_ADDR' not in os.environ.keys():
        os.environ['REDIS_PORT_6379_TCP_ADDR'] = 'localhost'

    from app.api import api
    app.register_blueprint(api)

    app.facilities = load_facilities()

    @app.before_request
    def before_request():
        g.redis = redis.StrictRedis(
            host=os.environ['REDIS_PORT_6379_TCP_ADDR'])

    return app
