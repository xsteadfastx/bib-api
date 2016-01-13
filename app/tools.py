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
