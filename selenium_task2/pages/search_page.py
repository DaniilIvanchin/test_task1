from selenium_task2.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium_task2.core.parse_price import parse_price


class SearchPage(BasePage):
    SORT_DROPDOWN = (By.ID, "sort_by_trigger")
    SORT_OPTION_PRICE_DESC = (By.XPATH, '//a[@id="Price_DESC"]')
    PRICES_LOCATOR_TEMPLATE = (By.XPATH,
                               '(//div[contains(@class,"discount_final_price") or contains(@class,"col search_price")])[position() <= {}]')
    RESULT_CONTAINER = (By.ID, "search_result_container")

    def filter_dropdown(self):
        self.wait.until(EC.element_to_be_clickable(self.SORT_DROPDOWN)).click()

    def sort_by_price_desc(self):
        self.wait.until(EC.element_to_be_clickable(self.SORT_OPTION_PRICE_DESC)).click()

        self.wait.until(
            lambda d: float(
                self.wait.until(EC.presence_of_element_located(self.RESULT_CONTAINER)).value_of_css_property(
                    "opacity")) < 0.99
        )

        self.wait.until(
            lambda d: float(
                self.wait.until(EC.presence_of_element_located(self.RESULT_CONTAINER)).value_of_css_property(
                    "opacity")) >= 0.98
        )

    def get_first_n_prices(self, n):
        by, value = self.PRICES_LOCATOR_TEMPLATE
        locator = (by, value.format(n))
        elements = self.wait.until(EC.presence_of_all_elements_located(locator))

        prices = []
        for el in elements[:n]:
            text = el.text.strip()
            if not text:
                continue

            price = parse_price(text)
            if price is not None:
                prices.append(price)

        return prices
