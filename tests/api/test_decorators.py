from flask import jsonify
import pytest

from tests.utils import load_json

from app.api.decorators import valid_facility, valid_token


@pytest.mark.parametrize('facility,status_code,data', [
    ('wolfsburg', 200, {'access': True}),
    ('nuernberg', 404, {'message': 'facility not found'})
])
def test_valid_facility(facility, status_code, data, flask_app, monkeypatch):

    class MockApp(object):
        facilities = {'wolfsburg': {}}

    monkeypatch.setattr('app.api.decorators.current_app', MockApp)

    @flask_app.route('/<facility>/valid')
    @valid_facility
    def valid(facility):
        return jsonify({'access': True})

    rv = flask_app.test_client().get('/{}/valid'.format(facility))

    assert rv.status_code == status_code
    assert load_json(rv.data) == data


@pytest.mark.parametrize('url,status_code,data', [
    ('/wolfsburg/valid?token=foobar', 401, {'message': 'bad token'}),
    (
        '/wolfsburg/valid?token=ImZvb2JhciI.5MbG27cXJGCfHaXh90CC0MKhem0',
        200,
        {'access': True}
    ),
    ('/wolfsburg/valid', 401, {'message': 'no token'})
])
def test_valid_token(url, status_code, data, flask_app):

    @flask_app.route('/<facility>/valid')
    @valid_token
    def valid(facility):
        return jsonify({'access': True})

    rv = flask_app.test_client().get(url)

    assert rv.status_code == status_code
    assert load_json(rv.data) == data
