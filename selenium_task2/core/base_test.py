import pytest
from selenium_task2.pages.base_page import BasePage
from selenium_task2.pages.search_page import SearchPage


class BaseTest:

    base_page: BasePage
    search_page: SearchPage

    @pytest.fixture(autouse=True)
    def setup(self, request, driver):
        request.cls.driver = driver
        request.cls.base_page = BasePage(driver)
        request.cls.search_page = SearchPage(driver)