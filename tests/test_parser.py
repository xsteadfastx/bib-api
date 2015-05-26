from api import parser
from datetime import date


def test_search_results_items_found():
    with open('tests/files/search_results_batman.html', 'r') as f:
        rv = parser.search_results(f.read())

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
        rv = parser.search_results(f.read())

    assert rv == []


def test_search_results_item_without_year():
    with open('tests/files/search_results_python.html', 'r',
              encoding='utf-8') as f:
        rv = parser.search_results(f.read())

    assert rv[0][-1].year is None
    assert rv[0][-1].type == 'Mehrbändiges Werk'
    assert rv[0][-1].name == ('Monty Python\'s Flying Circus : '
                              'sämtliche Worte / Graham Chapman ... - '
                              'Haffmans')

    assert rv[0][0].year == date(1992, 1, 1)
    assert rv[0][0].name == ('¬Das¬ Leben Brians : Drehbuch und '
                             'apokryphe Szenen / Monty Python. - '
                             'Dt. Erstausg. - Haffmans')
    assert rv[0][0].available is True


def test_search_results_one_item():
    with open('tests/files/search_results_american_splendor.html', 'r',
              encoding='utf-8') as f:
        rv = parser.search_results(f.read())

    assert rv[1] is False

    assert rv[0][0].available is True
    assert rv[0][0].year == date(2005, 1, 1)
    assert rv[0][0].type == 'DVD-Video/-Audio'
    assert rv[0][0].name == ('American Splendor [DVD] / Paul Giamatti, '
                             'Hope Davis. Dir. '
                             'by Robert Pulcini ... ')


def test_item():
    with open('tests/files/search_results_american_splendor.html',
              'r', encoding='utf-8') as f:
        rv = parser.item(f.read())

    name = ('American Splendor [DVD] / '
            'Paul Giamatti, Hope Davis. Dir. by Robert Pulcini ... ')
    assert rv.name == name

    assert rv.available is True
    assert rv.year == date(2005, 1, 1)
    assert rv.type == 'DVD-Video/-Audio'


def test_rent_list():
    with open('tests/files/rent_list.html', 'r', encoding='utf-8') as f:
        rv = parser.rent_list(f.read())

    assert len(rv) == 7

    name = ('Burgen und feste Plätze : d. Wehrbau vor Einf. d. '
            'Feuerwaffen; mit Anh. Kriegsgeräte u. schwere Waffen /  '
            '[Red.: Rudolf Huber ... Unter Mitarb. von ...]'
            '7.033 Bur208306696601')
    assert rv[0].name == name

    assert rv[0].from_date == date(2015, 4, 9)
    assert rv[0].till_date == date(2015, 6, 5)
    assert rv[0].notes == '1 Verlängerung'
