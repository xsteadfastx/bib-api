from datetime import datetime
from ics import Calendar
import pytest

from app.api.ical import build_ical


@pytest.mark.parametrize('input,expected', [
    (
        {
            'saldo': '-36,00',
            'items': [
                {
                    'due_date': '2016-04-15', 'author': 'Dürer, Albrecht',
                    'title': 'Albrecht Dürer'
                }, {
                    'due_date': '2016-04-20', 'author': 'Hopkins, John',
                    'title': 'Modezeichnen'
                }, {
                    'due_date': '2016-04-15', 'author': 'Hopper, Edward',
                    'title': 'Edward Hopper'
                }
            ]
        },
        {
            'number_of_events': 2,
            'events': [
                {
                    'begin': datetime(2016, 4, 15, 0, 0, 0),
                    'description': ('Dürer, Albrecht: Albrecht Dürer\n'
                                    'Hopper, Edward: Edward Hopper'),
                    'name': 'Bibliotheksrueckgaben: 2'
                },
                {
                    'begin': datetime(2016, 4, 20, 0, 0, 0),
                    'description': 'Hopkins, John: Modezeichnen',
                    'name': 'Bibliotheksrueckgaben: 1'
                }
            ]
        }

    ),
    (
        {
            'saldo': '',
            'items': []
        },
        {
            'number_of_events': 0,
            'events': []
        }
    )
])
def test_build_ical(input, expected):
    cal = Calendar(build_ical(input))

    assert len(cal.events) == expected['number_of_events']

    for i, event in enumerate(cal.events):
        assert event.begin.date() == expected['events'][i]['begin'].date()
        assert event.name == expected['events'][i]['name']
        assert event.description == expected['events'][i]['description']
