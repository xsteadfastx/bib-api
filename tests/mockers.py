from tests.utils import file_path


class MockBrowser(object):
    def __init__(self):
        self.page_data = self._page_loader()

    def _page_loader(self):
        yield None

    def click(self):
        return True

    def get(self, x):
        return True

    def find_element_by_id(self, x):
        return MockBrowser()

    def find_element_by_name(self, x):
        return MockBrowser()

    def send_keys(self, x):
        return True

    @property
    def page_source(self):
        return next(self.page_data)


class MockBrowserSearch(MockBrowser):
    def _page_loader(self):
        # 1
        with open(
            file_path(
                __file__, 'facilities', 'wolfsburg', 'files',
                'search_results0.html')) as f:
            yield f.read()

        # 2
        with open(
            file_path(
                __file__, 'facilities', 'wolfsburg', 'files',
                'search_results0.html')) as f:
            yield f.read()

        # 3
        for i in range(20):
            with open(
                file_path(
                    __file__, 'facilities', 'wolfsburg', 'files',
                    'title0.html')) as f:
                yield f.read()


class MockBrowserLogin(MockBrowser):
    def __init__(self, page_loader):
        self.page_data = page_loader()


class MockBrowserRentList(MockBrowser):
    def _page_loader(self):
        with open(
            file_path(
                __file__, 'facilities', 'wolfsburg', 'files',
                'account0.html')) as f:

            source = f.read()
            for i in range(3):
                yield source
