from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_task2.core.config_reader import ConfigReader


class BasePage:
    DEFAULT_TIMEOUT = 10
    CHECK_PAGE_LOCATOR = None
    def __init__(self, driver):
        timeout = ConfigReader.get("timeout", self.DEFAULT_TIMEOUT)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    def is_opened(self):
        self.wait.until(EC.visibility_of_element_located(self.CHECK_PAGE_LOCATOR))
