from unittest.mock import patch
from ics import Calendar
from test_api import app


@patch('api.browser.browser_login')
@patch('api.browser.webdriver')
def test_ical(mock_source, mock_login, app):
    with open('tests/files/rent_list.html', 'r', encoding='utf-8') as f:
        mock_source.PhantomJS().page_source = f.read()

    data = {'password': '123456', 'cardnumber': 'B123456'}

    url = app.post_json('/api/ical-url', data).json['url']

    rv = app.get(url)

    assert rv.content_type == 'text/calendar'

    cal = Calendar(rv.body.decode('utf-8'))

    assert len(cal.events) == 1

    event = cal.events[0]

    assert event.name == 'Bibliothekrueckgabe: 7 Teile'

    description = ('- Burgen und feste Plätze : d. Wehrbau vor Einf. d. '
                   'Feuerwaffen; mit Anh. Kriegsgeräte u. schwere Waffen /  '
                   '[Red.: Rudolf Huber ... Unter Mitarb. von ...]'
                   '7.033 Bur208306696601\n'
                   '- Wie erkenne ich romanische Kunst? : [Architektur, '
                   'Skulptur, Malerei] /  [Autor: Flavio Conti ; Sabatino '
                   'Moscati]7.033.4 Wie208314383701\n'
                   '- Romanik : Städte, Klöster und Kathedralen / Xavier '
                   'Barral i Altet. Fotos: Claude Huber ...7.033.4 '
                   'Rom00011473\n'
                   '- Gotik / Francesca Prina7.033.5 Got01195047\n'
                   '- Romanik / Francesca Prina7.033.4 Rom01195049\n'
                   '- Renaissance / Sonia Servida7.034.1 Ren01195048\n'
                   '- Barock / Claudia Zanlungo ; Daniela Tarabra7.034.7 '
                   'Bar01210576')
    assert event.description == description
