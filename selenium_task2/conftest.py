import pytest
from selenium_task2.core.browser import Browser
from selenium_task2.core.config_reader import ConfigReader


@pytest.fixture(params=ConfigReader.get("browser")["languages"])
def driver(request):
    driver = Browser.get_driver(lang=request.param)
    yield driver
    Browser.quit()

@pytest.fixture
def open_home(driver):
    base_url = ConfigReader.get("base_url")
    driver.get(base_url)
    yield