import pytest


def test_index_get(client):
    rv = client.get('/')

    assert rv.status_code == 200
    assert 'bib-api' in rv.data.decode('utf-8')
    assert 'Get a iCal url' in rv.data.decode('utf-8')


@pytest.mark.parametrize('status_code,json_return,expected', [
    (200, {'token': 'my-nice-token'}, 'my-nice-token'),
    (500, None, 'Connection problems with the API!'),
    (200, {}, 'No token recieved!')
])
def test_index_post(status_code, json_return, expected, client, monkeypatch):
    class MockRequests(object):
        def __init__(self):
            self.status_code = status_code

        def json(self):
            return json_return

    monkeypatch.setattr(
        'app.mod_frontend.views.requests.post',
        lambda x, json: MockRequests())

    rv = client.post('/', data={
        'username': 'foo',
        'password': 'bar',
        'facility': 'wolfsburg'}, follow_redirects=True)

    assert rv.status_code == 200
    assert expected in rv.data.decode('utf-8')
