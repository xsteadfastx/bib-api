from collections import defaultdict
from ics import Calendar, Event

from api import browser


def build_ical(cardnumber, password):
    rented = browser.rent_list(cardnumber, password)

    item_dict = defaultdict(list)
    for i in rented:
        item_dict[i.till_date].append(i)

    cal = Calendar()

    for k, v in item_dict.items():
        event = Event()
        event.begin = '{} 00:00:00'.format(k.strftime('%Y-%m-%d'))
        items = '\n'.join(['- {}'.format(i.name) for i in v])
        event.description = items

        event.name = 'Bibliothekrueckgabe: {} Teile'.format(len(v))

        cal.events.append(event)

    return cal
