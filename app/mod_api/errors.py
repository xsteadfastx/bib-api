from flask import jsonify

from app.mod_api import mod_api


class InvalidUsage(Exception):
    """Own exception for return a dictionary for jsonifying."""
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Create a dict."""
        rv = {}
        rv['message'] = self.message

        return rv


@mod_api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Needed errorhandler for the app."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response
