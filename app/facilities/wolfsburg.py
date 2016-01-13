from datetime import date, datetime
from urllib.parse import urljoin
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from app.browser import create_browser
from app.tools import next_page


def search(term, page=1):
    """Searches for a term.

    :param term: A term to search for.
    :param page: Pagination page.
    :type term: str
    :type page: int
    :return: Dictionary with results and next_page integer.
    :rtype: dict
    """
    entry_url = ('http://webopac.stadt.wolfsburg.de'
                 '/webopac/index.asp?DB=web_biblio')

    # list to store results
    results = []

    # set up browser
    browser = create_browser()

    # fill out search and click the button
    browser.get(entry_url)
    browser.find_element_by_name('stichwort').send_keys(term)
    browser.find_element_by_name('stichwort').send_keys(Keys.RETURN)

    # return empty list if wanted page is not there
    page_numbers = parse_page_numbers(browser.page_source)
    if page not in page_numbers:
        return {'results': [], 'next_page': None}

    if page != 1:
        browser.find_element_by_link_text(str(page)).click()

    links = parse_search_title_overview(browser.page_source, entry_url)

    for link in links:
        browser.get(link)

        # if the word "Bände" in the source the link should be skipped
        if 'Bände' in browser.page_source:
            continue

        # parse the source for title and append it to the resaults list
        results.append(parse_title(browser.page_source, entry_url))

    next_page_number = next_page(page_numbers, page)

    return {'results': results, 'next_page': next_page_number}


def parse_search_title_overview(page_source, base_url):
    """Parses search page results.

    :param page_source: HTML page source.
    :param base_url: URL of the base that gets joined together.
    :type page_source: str
    :type base_url: str
    :return: List of item urls.
    :rtype: list
    """
    soup = BeautifulSoup(page_source, 'lxml')

    table = soup.find('table', 'resulttab')

    if not table:
        return []

    rows = [i
            for i in table.find_all('tr')
            if 'class' in i.attrs
            if 'result_treffer' in i.attrs['class'][0]]

    return [urljoin(base_url, i.a.get('href')) for i in rows]


def parse_string_for_year(line):
    """Parses string-line for year.

    :param line: Line string.
    :type line: str
    :return: Year.
    :rtype: datetime.date or None
    """
    year = re.findall('\d\d\d\d', line)
    if year:
        return date(int(year[0]), 1, 1)
    else:
        return None


def parse_due_date(line):
    """Parses due date from line.

    :param line: Line string.
    :type line: str
    :return: datetime.date if successful, None otherwise.
    :rtype: datetime.date or None
    """
    try:
        return datetime.strptime(line, '%d.%m.%Y').date()

    except ValueError:
        return None


def parse_copy_availability(line):
    """Parses 'Status-'line for availability.

    :param line: Line string.
    :type line: str
    :return: Availability.
    :rtype: bool
    """
    if 'Entliehen' in line:
        return False

    elif 'Verfügbar' in line:
        return True

    else:
        return False


def parse_title(page_source, base_url):
    """Parses title details.

    :param page_source: HTML page source of title details.
    :param base_url: URL of the base that gets joined together.
    :type page_source: str
    :type base_url: str
    :return: Title dict.
    :rtype: dict
    """
    title = {}

    soup = BeautifulSoup(page_source, 'lxml')

    # title
    title['title'] = soup.find_all('div', class_='detail_titel')[0].text

    # cover
    cover = soup.find('div', class_='detail_cover').img['src']
    if 'amazon' in cover:
        title['cover'] = cover
    elif cover.startswith('/read'):
        title['cover'] = urljoin(base_url, cover)

    for tr in soup.find_all('tr'):

        line = str(tr)

        # annotation
        if 'Beschreibung:' in line:
            title['annotation'] = tr.find_all('td')[1].text

        # author
        if 'Verfasserangaben:' in line:
            title['author'] = tr.find_all('td')[1].text

        # isbn
        if 'ISBN:' in line:
            title['isbn'] = tr.find_all('td')[1].text

        # year
        if 'Impressum:' in line:
            impressum = tr.find_all('td')[1].text
            title['year'] = parse_string_for_year(impressum)

    # parse copies
    copies = []
    for tr in soup.find_all('tr', class_='tabExemplar'):

        copy = {}

        tds = tr.find_all('td')

        # id
        copy['id'] = tds[0].text

        # position
        copy['position'] = tds[1].text

        # type
        copy['type'] = tds[2].text

        # available
        copy['available'] = parse_copy_availability(tds[3].text)

        # branch
        copy['branch'] = tds[4].text

        # due_date
        copy['due_date'] = parse_due_date(tds[5].text)

        # add to list
        copies.append(copy)

    # add copies to title dict
    title['copies'] = copies

    return title


def parse_page_numbers(page_source):
    """Parses possible pages for pagination.

    :param page_source: HTML page source.
    :type page_source: str
    :return: List of pages.
    :rtype: list[int]
    """
    pages = []

    soup = BeautifulSoup(page_source, 'lxml')

    nav = soup.find('div', class_='result_nav')

    if nav:
        pages.extend(nav.find_all('u'))
        pages.extend(nav.find_all('a'))

    if pages:
        pages = [int(i.text) for i in pages]

    return pages
