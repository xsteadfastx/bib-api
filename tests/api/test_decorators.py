from flask import Flask, jsonify
import pytest

from tests.tools import load_json

from app.api.decorators import valid_facility
from app.api.errors import InvalidUsage


@pytest.mark.parametrize('facility,status_code,data', [
    ('wolfsburg', 200, {'access': True}),
    ('nuernberg', 404, {'message': 'facility not found'})
])
def test_valid_facility(facility, status_code, data, monkeypatch):

    class MockApp(object):
        facilities = {'wolfsburg': {}}

    monkeypatch.setattr('app.api.decorators.current_app', MockApp)

    app = Flask(__name__)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code

        return response

    @app.route('/<facility>/valid')
    @valid_facility
    def valid(facility):
        return jsonify({'access': True})

    rv = app.test_client().get('/{}/valid'.format(facility))

    assert rv.status_code == status_code
    assert load_json(rv.data) == data
