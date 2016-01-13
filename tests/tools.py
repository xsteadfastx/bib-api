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
    :rtypte: dict
    """
    return json.loads(data.decode('UTF-8'))
