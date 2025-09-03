from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_task2.pages.base_page import BasePage

class HomePage(BasePage):
    SEARCH_BOX = (By.ID, 'store_nav_search_term')
    CHECK_PAGE_LOCATOR = (By.XPATH, '//a[contains(@class, "global_action_link")]')

    def open(self):
        self.driver.get(self.base_url)

    def enter_search(self, text: str):
        search_box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)