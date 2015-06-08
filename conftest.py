import os
import sys
import pytest


def pytest_configure(config):
    os.environ['PYTHONPATH'] = ':'.join(sys.path)
    os.environ['SECRET_KEY'] = 'secretkey'
    if 'REDIS_HOST' not in os.environ.keys():
        os.environ['REDIS_HOST'] = 'localhost'


@pytest.fixture
def app():
    from api import api
    from webtest import TestApp

    return TestApp(api.app)


@pytest.yield_fixture
def redis_conn():
    import redis

    r = redis.StrictRedis(host=os.environ['REDIS_HOST'])
    yield r
    r.flushall()
