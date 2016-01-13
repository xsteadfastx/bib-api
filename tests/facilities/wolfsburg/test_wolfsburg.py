from datetime import date
import pytest

from tests.tools import file_path
from tests.mockers import MockBrowser

from app.facilities import wolfsburg


@pytest.mark.parametrize('input,expected', [
    ('Stuttgart : Panini-Verl., 2010', date(2010, 1, 1)),
    ('Burbank : Warner Bros. Interactive, 2015', date(2015, 1, 1)),
    ('München : Dorling Kindersley, 2012', date(2012, 1, 1)),
    ('Foo Bar', None)
])
def test_parse_string_for_year(input, expected):
    assert wolfsburg.parse_string_for_year(input) == expected


@pytest.mark.parametrize('input,expected', [
    ('search_results0.html', ['http://foo.bar/index.asp?detmediennr=0',
                              'http://foo.bar/index.asp?detmediennr=1',
                              'http://foo.bar/index.asp?detmediennr=2',
                              'http://foo.bar/index.asp?detmediennr=3',
                              'http://foo.bar/index.asp?detmediennr=4',
                              'http://foo.bar/index.asp?detmediennr=5',
                              'http://foo.bar/index.asp?detmediennr=6',
                              'http://foo.bar/index.asp?detmediennr=7',
                              'http://foo.bar/index.asp?detmediennr=8',
                              'http://foo.bar/index.asp?detmediennr=9']),
    ('search_results1.html', [])
])
def test_parse_search_title_overview(input, expected):
    with open(file_path(__file__, 'files', input), 'r') as f:

        assert wolfsburg.parse_search_title_overview(
            f.read(), 'http://foo.bar') == expected


@pytest.mark.parametrize('input,expected', [
    ('Verfügbar', True),
    ('Entliehen', False),
    ('Foo Bar', False)
])
def test_parse_copy_availability(input, expected):
    assert wolfsburg.parse_copy_availability(input) == expected


@pytest.mark.parametrize('input,expected', [
    ('title0.html', {
        'cover': 'http://foo.bar/read/PICS/Blu-Ray-Disc_b.gif',
        'year': date(2015, 1, 1),
        'title': 'Batman - Arkham knight [X-BOX ONE]',
        'annotation': ('Action-Adventure für 1 Spieler offline und '
                       'bis zu 8 Spielern online.'),
        'copies': [
            {
                'id': 'M1509006',
                'position': 'Ycr Batm',
                'available': False,
                'branch': '00:Zentralbibliothek',
                'due_date': None,
                'type': 'Blu-Ray Spiel'
            }
        ]
    }),
    ('title1.html', {
        'cover': ('http://images-eu.amazon.com'
                  '/images/P/3831020647.03.MZZZZZZZ.jpg'),
        'title': 'Batman',
        'author': 'von Daniel Wallace',
        'isbn': '978-3-8310-2064-5',
        'year': date(2012, 1, 1),
        'annotation': ('Ein üppig illustriertes Nachschlagewerk '
                       'mit detaillierten Einblicken in die Welt '
                       'des dunklen Ritters.'),
        'copies': [
            {
                'id': 'M1210194',
                'available': False,
                'position': 'Pcm 2 Batm',
                'due_date': date(2016, 1, 29),
                'type': 'Sachliteratur',
                'branch': '00:Zentralbibliothek'
            }
        ]
    }),
    ('title2.html', {
        'year': date(2015, 1, 1),
        'cover': ('http://images-eu.amazon.com'
                  '/images/P/3421047197.03.MZZZZZZZ.jpg'),
        'isbn': '978-3-421-04719-9',
        'author': ('Harper Lee. Aus dem Engl. von Ulrike Wasel und '
                   'Klaus  Timmermann'),
        'title': 'Gehe hin, stelle einen Wächter',
        'copies': [
            {
                'branch': '00:Zentralbibliothek',
                'id': 'M1507843',
                'available': False,
                'type': 'Belletristik',
                'due_date': date(2016, 2, 4),
                'position': 'Lee'
            },
            {
                'branch': '00:Zentralbibliothek',
                'id': 'M1510326',
                'available': False,
                'type': 'Belletristik',
                'due_date': date(2016, 2, 13),
                'position': 'Lee'
            },
            {
                'branch': '10:Zw. Detmerode',
                'id': 'M1508914',
                'available': False,
                'type': 'Belletristik',
                'due_date': date(2016, 2, 25),
                'position': 'Lee'
            },
            {
                'branch': '24:Schulbibl. Vorsfe',
                'id': 'M1513492',
                'available': True,
                'type': 'Belletristik',
                'due_date': None,
                'position': 'Lee'
            }
        ]
    })
])
def test_parse_title(input, expected):
    with open(file_path(__file__, 'files', input), 'r') as f:

        assert wolfsburg.parse_title(f.read(), 'http://foo.bar') == expected


@pytest.mark.parametrize('input,expected', [
    ('search_results0.html', [1, 2, 3, 4, 5])
])
def test_parse_page_numbers(input, expected):
    with open(file_path(__file__, 'files', input), 'r') as f:

        assert wolfsburg.parse_page_numbers(f.read()) == expected


def test_search(monkeypatch):
    monkeypatch.setattr('app.facilities.wolfsburg.create_browser', MockBrowser)

    item = {
        'title': 'Batman - Arkham knight [X-BOX ONE]',
        'cover': ('http://webopac.stadt.wolfsburg.de'
                  '/read/PICS/Blu-Ray-Disc_b.gif'),
        'year': date(2015, 1, 1),
        'annotation': ('Action-Adventure für 1 Spieler offline '
                       'und bis zu 8 Spielern online.'),
        'copies': [
            {
                'branch': '00:Zentralbibliothek',
                'position': 'Ycr Batm',
                'id': 'M1509006',
                'due_date': None,
                'available': False,
                'type': 'Blu-Ray Spiel'
            }
        ]
    }

    expected = {
        'next_page': 2,
        'results': [item for i in range(10)]
    }

    assert wolfsburg.search('batman') == expected
