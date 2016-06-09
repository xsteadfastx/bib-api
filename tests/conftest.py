import os
import pytest
import sys


def pytest_configure(config):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

    if 'REDIS_PORT_6379_TCP_ADDR' not in os.environ.keys():
        os.environ['REDIS_PORT_6379_TCP_ADDR'] = 'localhost'


@pytest.yield_fixture
def redis_conn():
    import redis

    r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'])

    yield r


@pytest.yield_fixture
def redis_clean(redis_conn):
    redis_conn.flushall()

    yield

    redis_conn.flushall()


@pytest.yield_fixture
def app(redis_clean):
    from app.app import create_app

    app = create_app('test.cfg')
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture
def client(app):
    with app.test_client() as client:

        yield client


@pytest.yield_fixture
def flask_app():
    from flask import Flask, jsonify

    from app.mod_api.errors import InvalidUsage

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testing'

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code

        return response

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture
def flask_client(flask_app):
    with flask_app.text_client() as client:

        yield client
