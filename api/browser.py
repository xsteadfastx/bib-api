from selenium import webdriver
from api import parser


def browser_login(browser, cardnumber, password):
    entry_url = ('https://online-service2.nuernberg.de/'
                 'aDISWeb/app?service=direct/0/Home/'
                 '$DirectLink&sp=Sapp1%3A4103')

    # browse to that url
    browser.get(entry_url)
    browser.find_element_by_link_text('Benutzerkonto').click()

    # login
    browser.find_element_by_id('L#AUSW_1').send_keys(cardnumber)
    browser.find_element_by_id('LPASSW_1').send_keys(password)
    browser.find_element_by_name('textButton').click()
    browser.find_element_by_name('messageButton').click()


def rent_list(cardnumber, password):
    # selenium phantomjs magic
    browser = webdriver.PhantomJS()
    browser.set_window_size(1120, 550)

    # login
    browser_login(browser, cardnumber, password)

    # get rentlist
    if 'Keine Ausleihen' in browser.page_source:
        return []

    browser.find_element_by_link_text(
        'Ausleihen zeigen oder verlängern').click()

    # soup it up
    page_source = browser.page_source

    # quit browser
    browser.quit()

    # pars the page and get the results
    results = parser.rent_list(page_source)

    return results


def search(term):
    entry_url = ('https://online-service2.nuernberg.de/'
                 'aDISWeb/app?service=direct/0/Home/'
                 '$DirectLink&sp=Sapp1%3A4103')

    # create results list for later
    results = []

    # selenium phantomjs magic
    browser = webdriver.PhantomJS()
    browser.set_window_size(1120, 550)

    # browse to that url
    browser.get(entry_url)

    # fill out search and click the button
    browser.find_element_by_name('$Textfield').send_keys(term)
    browser.find_element_by_name('textButton').click()

    # browse through the search result list till its just over 100 results
    while len(results) <= 100:
        # parse page and extend result list
        search_results = parser.search_results(browser.page_source)

        # if list is empty break
        if not search_results:
            break

        results.extend(search_results[0])

        # search_results provide a True or False if there is still a page
        # to click through. else the while loop just breaks
        if search_results[1]:
            browser.find_element_by_id('Toolbar$0_5').click()
        else:
            break

    # quit browser
    browser.quit()

    return results
