import pytest
from selenium_task2.core.browser import Browser


@pytest.fixture(scope="class")
def driver(request):
    driver = Browser.get_driver()
    request.cls.driver = driver
    yield driver
    Browser.quit()
