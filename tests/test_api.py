from unittest.mock import patch
from itsdangerous import URLSafeSerializer
from os import environ

from api.api import AuthSchema


@patch('api.browser.browser_login')
@patch('api.browser.webdriver')
def test_rented(mock_source, mock_login, app):
    with open('tests/files/rent_list.html', 'r', encoding='utf-8') as f:
        mock_source.PhantomJS().page_source = f.read()

    rv = app.post_json('/api/rented',
                       dict(cardnumber='B123456', password='123456')).json

    assert len(rv['results']) == 7

    expected = {
        'notes': '1 Verlängerung',
        'till_date': '2015-06-05',
        'from_date': '2015-04-09',
        'name': ('Burgen und feste Plätze : '
                 'd. Wehrbau vor Einf. d. Feuerwaffen; mit Anh. '
                 'Kriegsgeräte u. schwere Waffen /  '
                 '[Red.: Rudolf Huber ... Unter Mitarb. von ...]7.033 '
                 'Bur208306696601')
    }
    assert rv['results'][0] == expected


def test_rented_no_password(app):
    rv = app.post_json('/api/rented', dict(cardnumber='B123456')).json

    assert rv == {'errors': {'password': ['Missing data for required field.']}}


@patch('api.browser.webdriver')
def test_search_found_items(mock_source, app):
    with open('tests/files/search_results_batman.html', 'r',
              encoding='utf-8') as f:
        mock_source.PhantomJS().page_source = f.read()

    rv = app.post_json('/api/search', dict(name='batman')).json

    assert len(rv['results']) == 110

    expected = {
        'name': ('Batman - Einsatz für den dunklen Ritter [Tonträger] : '
                 'ab 7 Jahren / in vielen Stimmen erzählt von Torsten '
                 'Michaelis. DC Comics. Geschrieben von Robert Greenberger ; '
                 'Blake A. Hoena und Donald Lemke. Aus dem Amerikan. übers. '
                 'von Christian Dreller. Produktion und Regie: Dirk Kauffels. '
                 '- ungekürzte, szenische Lesung mit Musik. - Argon'),
        'year': '2015-01-01',
        'available': False,
        'type': 'CD'
    }
    assert rv['results'][0] == expected


@patch('api.browser.webdriver')
def test_search_nothing_found(mock_source, app):
    with open('tests/files/search_results_foobar.html', 'r',
              encoding='utf-8') as f:
        mock_source.PhantomJS().page_source = f.read()

    rv = app.post_json('/api/search', dict(name='foobar')).json

    assert rv['results'] == []


@patch('api.browser.webdriver')
def test_search_one_item_returned(mock_source, app):
    '''If there is only one resault a item view is returned and not a list.'''
    with open('tests/files/search_results_american_splendor.html', 'r',
              encoding='utf-8') as f:
        mock_source.PhantomJS().page_source = f.read()

    rv = app.post_json('/api/search', dict(name='american splendor')).json

    assert len(rv['results']) == 1

    expected = {
        'name': ('American Splendor [DVD] / Paul Giamatti, Hope Davis. Dir. '
                 'by Robert Pulcini ... '),
        'year': '2005-01-01',
        'type': 'DVD-Video/-Audio',
        'available': True
    }
    assert rv['results'][0] == expected


def test_ical_url(app):
    data = {'password': '123456', 'cardnumber': 'B123456'}

    rv = app.post_json('/api/ical-url', data).json

    s = URLSafeSerializer(environ['SECRET_KEY'])
    token = s.dumps(AuthSchema().load(data))

    assert rv == dict(
        url='http://localhost:80/ical/rented.ics?token={}'.format(token))
