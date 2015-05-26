from bs4 import BeautifulSoup
from datetime import datetime, date
import re


class SearchResult(object):
    '''An helper object to store search result items.'''

    def __init__(self, name, available, year, type):
        self.name = name
        self.available = available
        self.year = year
        self.type = type

    def __repr__(self):
        return '<SearchResult(name={}, available={})'.format(self.name,
                                                             self.available)


def search_results(source):
    '''Parse the search results page and return SearchResult objects.'''
    page_results = []

    # making soup out of the page source
    soup = BeautifulSoup(source)

    for i in soup.find_all('h1'):
        if 'Vollanzeige' in i.text.rstrip():
            return [item(source)], False

    # find all table items
    rows = soup.find_all('tr', class_=re.compile('rTable_tr_.*'))

    # if no rows are found we assume that there arent any search results
    # and return an empty dictionary
    if not rows:
        return []

    # creating a list of result items
    for row in rows:
        cols = row.find_all('td')

        name = cols[3].text.strip()

        # getting availibility
        img = cols[4].find('img')
        if 'nicht' in img['alt']:
            available = False
        else:
            available = True

        # convert year to a date object
        if not cols[5].text.strip():
            year = None

        else:
            year = date(int(cols[5].text.strip()), 1, 1)

        # extract media type
        img = cols[2].find('img')
        type = img['alt']

        # adding the list
        page_results.append(SearchResult(name, available, year, type))

    if 'disabled' not in list(soup.find(id='Toolbar$0_5').attrs):
        next_page = True
    else:
        next_page = False

    return page_results, next_page


def item(source):
    soup = BeautifulSoup(source)

    # parse first table
    table = soup.find(
        'table', summary='Auflistung der Kategorien des ausgewählten Treffers')
    rows = table.find_all('td')

    # extract media type
    img = rows[0].find('img')
    type = img['alt']

    name = rows[1].text

    parsed_year = re.search(r'\d\d\d\d', rows[3].text).group()
    year = date(int(parsed_year), 1, 1)

    # parse second table
    table = soup.find('table', class_='rTable_table')
    rows = table.find_all('td')

    if 'Verfügbar' in rows[5].text:
        available = True
    else:
        available = False

    return SearchResult(name, available, year, type)


class RentResult(object):
    def __init__(self, from_date, till_date, name, notes):
        self.from_date = from_date
        self.till_date = till_date
        self.name = name
        self.notes = notes

    def __repr__(self):
        return '<Result(name={})>'.format(self.name)


def rent_list(source):
    rent_results = []

    # soup it up
    soup = BeautifulSoup(source)

    # find all table items
    rows = soup.find_all('tr', class_=re.compile('rTable_tr_.*'))

    for row in rows:
        cols = row.find_all('td')

        dates = cols[1].text.split('-')
        from_date = datetime.strptime(dates[0].strip(), '%d.%m.%Y').date()
        till_date = datetime.strptime(dates[1].strip(), '%d.%m.%Y').date()

        name = cols[3].text.strip()

        notes = cols[4].text.strip()

        rent_results.append(RentResult(from_date, till_date, name, notes))

    return rent_results
