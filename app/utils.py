def next_page(page_list, page):
    """Returns next page of a list.

    Its needed for pagination.

    :param page_list: A list of available page numbers.
    :param page: Page to get next page from.
    :type page_list: list
    :type page: int
    :return: Page number of next page.
    :rtype: int
    """
    if page not in page_list:
        return None
    if page_list.index(page) == len(page_list) - 1:
        return None
    return page_list[page_list.index(page) + 1]


def write_page_source(filename, page_source):
    """A little function to write page_source to a file.

    When developing and testing you need to download test data. This does
    nothing much but saving the source to a givin file.

    :param filename: File to write to.
    :param page_source: Page source.
    :type filename: str
    :type page_source: str
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_source)
