import os
import sys
import pytest


def pytest_configure(config):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
    os.environ['SECRET_KEY'] = 'secretkey'
    if 'REDIS_PORT_6379_TCP_ADDR' not in os.environ.keys():
        os.environ['REDIS_PORT_6379_TCP_ADDR'] = 'localhost'


@pytest.yield_fixture
def app():
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
def redis_conn():
    import redis

    r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'])

    yield r

    r.flushall()
