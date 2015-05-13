from api import api
from unittest.mock import patch
import pickle


@patch('api.api.request')
@patch('api.api.browser.rent_list')
def test_rented(mock_api_browser, mock_api_request):
    mock_api_request.json = dict(cardnumber='B123456', password='123456')

    with open('tests/files/rent_list_results.p', 'rb') as f:
        mock_api_browser.return_value = pickle.load(f)

    rv = api.rented()

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


@patch('api.api.request')
@patch('api.api.browser.search')
def test_search_found_items(mock_api_browser, mock_api_request):
    mock_api_request.json = dict(search='batman')

    with open('tests/files/search_results_batman.p', 'rb') as f:
        mock_api_browser.return_value = pickle.load(f)

    rv = api.search()

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


@patch('api.api.request')
@patch('api.api.browser.search')
def test_search_nothing_found(mock_api_browser, mock_api_request):
    mock_api_request.json = dict(search='foobar')

    with open('tests/files/search_results_foobar.p', 'rb') as f:
        mock_api_browser.return_value = pickle.load(f)

    rv = api.search()

    assert rv['results'] == []
