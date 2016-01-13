from selenium import webdriver


def create_browser():
    """A helper function for easy browser creation.

    :return: A browser.
    :rtype: selenium.webdriver.phantomjs.webdriver.WebDriver
    """
    browser = webdriver.PhantomJS()
    browser.set_window_size(1120, 550)

    return browser
