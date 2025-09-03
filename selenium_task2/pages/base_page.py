from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_task2.core.config_reader import ConfigReader


class BasePage:
    def __init__(self, driver):
        timeout = ConfigReader.get("timeout", 10)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
        self.base_url = ConfigReader.get("base_url")

    def is_opened(self):
        self.wait.until(EC.visibility_of_element_located(self.CHECK_PAGE_LOCATOR))
