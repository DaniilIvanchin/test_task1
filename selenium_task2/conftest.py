import pytest
from selenium_task2.pages.base_page import BasePage
from selenium_task2.pages.search_page import SearchPage
from selenium_task2.pages.home_page import HomePage
from selenium_task2.core.browser import Browser
from selenium_task2.core.config_reader import ConfigReader


@pytest.fixture(params=ConfigReader.get("browser")["languages"])
def driver(request):
    driver = Browser.get_driver(lang=request.param)
    yield driver
    Browser.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver)


@pytest.fixture
def home_page(driver):
    return HomePage(driver)


@pytest.fixture
def search_page(driver):
    return SearchPage(driver)
