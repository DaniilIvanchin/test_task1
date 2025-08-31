from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class BasePage:
    SEARCH_BOX = (By.ID, 'store_nav_search_term')
    BASE_URL = "https://store.steampowered.com/"
    GLOBAL_ACTION_LINK = (By.XPATH, '//a[contains(@class, "global_action_link")]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self, lang="russian"):
        url = f"{self.BASE_URL}?l={lang}"
        self.driver.get(url)

    def is_opened(self):
        self.wait.until(EC.visibility_of_element_located(self.GLOBAL_ACTION_LINK))

    def enter_search(self, text: str, lang="russian"):
        search_box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)
        current_url = self.driver.current_url
        if "l=" not in current_url:
            current_url += f"&l={lang}"
        self.driver.get(current_url)