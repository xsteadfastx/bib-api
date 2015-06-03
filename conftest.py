import os
import sys


def pytest_configure(config):
    os.environ['PYTHONPATH'] = ':'.join(sys.path)
    os.environ['SECRET_KEY'] = 'secretkey'
