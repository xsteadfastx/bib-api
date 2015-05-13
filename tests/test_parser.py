from api import parser
from datetime import date


def test_search_results_items_found():
    with open('tests/files/search_results_batman.html', 'r') as f:
        rv = parser.search_results(f)

    assert rv[1] is True
    assert len(rv[0]) == 22

    name = ('Batman - Einsatz für den dunklen Ritter '
            '[Tonträger] : ab 7 Jahren / in vielen Stimmen erzählt von '
            'Torsten Michaelis. DC Comics. Geschrieben von Robert '
            'Greenberger ; Blake A. Hoena und Donald Lemke. '
            'Aus dem Amerikan. übers. von Christian Dreller. Produktion '
            'und Regie: Dirk Kauffels. - ungekürzte, szenische Lesung '
            'mit Musik. - Argon')
    assert rv[0][0].name == name

    assert rv[0][0].available is False


def test_search_results_nothing_found():
    with open('tests/files/search_results_foobar.html', 'r',
              encoding='utf-8') as f:
        rv = parser.search_results(f)

    assert rv == []


def test_rent_list():
    with open('tests/files/rent_list.html', 'r', encoding='utf-8') as f:
        rv = parser.rent_list(f)

    assert len(rv) == 7

    name = ('Burgen und feste Plätze : d. Wehrbau vor Einf. d. '
            'Feuerwaffen; mit Anh. Kriegsgeräte u. schwere Waffen /  '
            '[Red.: Rudolf Huber ... Unter Mitarb. von ...]'
            '7.033 Bur208306696601')
    assert rv[0].name == name

    assert rv[0].from_date == date(2015, 4, 9)

    assert rv[0].till_date == date(2015, 6, 5)

    assert rv[0].notes == '1 Verlängerung'
