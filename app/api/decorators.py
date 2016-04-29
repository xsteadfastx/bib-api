from functools import wraps

from flask import current_app, request
from itsdangerous import URLSafeSerializer

from app.api.errors import InvalidUsage


def valid_facility(f):
    """A decorator to return a 404 if the facilitry is not there.

    :param f: Function to decorate.
    :type f: function
    :return: Decorated function.
    :rtype: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'facility' in kwargs.keys():
            if kwargs['facility'] not in current_app.facilities.keys():
                raise InvalidUsage('facility not found', status_code=404)

        return f(*args, **kwargs)

    return decorated_function


def valid_token(f):
    """A decorator to check if there is a token and if its valid.

    :param f: Function to decorate.
    :type f: function
    :return: Decorated function.
    :rtype: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        s = URLSafeSerializer(current_app.config['SECRET_KEY'],
                              salt=kwargs['facility'])

        if 'token' not in request.args:
            raise InvalidUsage('no token', status_code=401)

        try:
            s.loads(request.args.get('token'))

        except:
            raise InvalidUsage('bad token', status_code=401)

        return f(*args, **kwargs)

    return decorated_function
