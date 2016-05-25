from collections import defaultdict
from ics import Calendar, Event


def build_ical(lent_list):
    """Builds ical from a lent list.

    :param lent_list: lent list.
    :type lent_list: dict
    :return: ical.
    :rtype: str
    """
    cal = Calendar()

    item_dict = defaultdict(list)
    for i in lent_list['items']:
        item_dict[i['due_date']].append('{}: {}'.format(i['author'],
                                                        i['title']))

    for k, v in item_dict.items():
        event = Event()

        event.begin = '{} 00:00:00'.format(k)

        items = '\n'.join(v)
        event.description = items

        event.name = 'Bibliotheksrueckgaben: {}'.format(len(v))

        cal.events.append(event)

    return cal
