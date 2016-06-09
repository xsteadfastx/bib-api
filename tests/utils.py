from itsdangerous import BadSignature, URLSafeSerializer
from os import path
import json


def file_path(file_dir, *args):
    """Returns a joined absolute path.

    :param file_dir: usually takes a __file__
    :type file_dir: str
    :param *args: file strings
    :type *args: str
    :returns: a joined absolute path
    :rtype: str
    """
    return path.abspath(
        path.join(path.dirname(path.realpath(file_dir)), *args))


def load_json(data):
    """Parses JSON and returns a UTF-8 decoded dict.

    :param data: JSON data
    :type: str
    :returns: UTF-8 decoded dictionary
    :rtype: dict
    """
    return json.loads(data.decode('UTF-8'))


def create_token(data):
    """Generates a token for testing.

    :param data: Username and password dictionary.
    :type data: dict
    :returns: token
    :rtype: str
    """
    return URLSafeSerializer('testing', salt='wolfsburg').dumps(data)


def verify_token(token):
    """Checks if a token is valid and returns its value.

    :param token: token.
    :type token: str
    :returns: Decoded value or False
    :rtype: str or False
    """
    s = URLSafeSerializer('testing', salt='wolfsburg')

    try:
        response = s.loads(token)

    except BadSignature:
        response = False

    return response
