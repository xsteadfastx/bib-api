import datetime
import json
import pytest

from tests.tools import load_json, verify_token


def test_facility_list(client, monkeypatch):
    monkeypatch.setattr('app.api.views.current_app.facilities',
                        {'wolfsburg': {}, 'nuernberg': {}, 'paris': {}})

    rv = client.get('/api/facilities')

    assert rv.status_code == 200

    data = load_json(rv.data)

    assert len(data['facilities']) == 3
    assert 'wolfsburg' in data['facilities']
    assert 'nuernberg' in data['facilities']
    assert 'paris' in data['facilities']


@pytest.mark.parametrize('search_return,expected', [
    ({'results': [], 'page': 0}, {'results': [], 'next_page': 0}),
    ({
        "next_page": 5,
        "results": [
            {
                "annotation": "Der Schurke Two-Face wurde durch...",
                "author": "geschrieben von Matthew K. Manning.",
                "copies": [
                    {
                        "available": False,
                        "branch": "01:Kinderbibl. Zentr",
                        "due_date": datetime.date(2016, 2, 5),
                        "id": "M1400963",
                        "position": "4.1 Mann",
                        "type": "Kinder- und Jugendliteratur"
                    }
                ],
                "cover": "http://foo.bar/images/P/3555829.03.MZZZZZZZ.jpg",
                "isbn": "978-3-596-85582-7",
                "title": "Batman - Ein finsterer Plan",
                "year": datetime.date(2013, 1, 1)
            }
        ]
    }, {
        "next_page": 5,
        "results": [
            {
                "annotation": "Der Schurke Two-Face wurde durch...",
                "author": "geschrieben von Matthew K. Manning.",
                "copies": [
                    {
                        "available": False,
                        "branch": "01:Kinderbibl. Zentr",
                        "due_date": "2016-02-05",
                        "id": "M1400963",
                        "position": "4.1 Mann",
                        "type": "Kinder- und Jugendliteratur"
                    }
                ],
                "cover": "http://foo.bar/images/P/3555829.03.MZZZZZZZ.jpg",
                "isbn": "978-3-596-85582-7",
                "title": "Batman - Ein finsterer Plan",
                "year": "2013-01-01"
            }
        ]
    })
])
def test_search(search_return, expected, client, monkeypatch):
    monkeypatch.setattr(
        'app.api.views.current_app.facilities',
        {'wolfsburg': {'search': lambda term, page: search_return}})

    rv = client.post('/api/wolfsburg/search',
                     data=json.dumps({'term': 'batman'}),
                     headers={'content-type': 'application/json'})

    assert load_json(rv.data) == expected


@pytest.mark.parametrize('url,data,expected,status_code', [
    (
        '/api/wolfsburg/token',
        {'username': 'foo', 'password': 'bar'},
        True,
        200
    ),
    (
        '/api/wolfsburg/token',
        {'username': 'foo'},
        {'message': {'password': ['Missing data for required field.']}},
        400
    ),
    (
        '/api/wolfsburg/token',
        {},
        {'message': 'no data'},
        400
    )

])
def test_get_token(url, data, expected, status_code, client, monkeypatch):
    monkeypatch.setattr('app.api.views.current_app.facilities',
                        {'wolfsburg': {}})

    rv = client.post(url, data=json.dumps(data),
                     headers={'content-type': 'application/json'})

    assert rv.status_code == status_code

    if expected is not True:
        assert load_json(rv.data) == expected

    else:
        token = load_json(rv.data)['token']

        assert data == verify_token(token)
