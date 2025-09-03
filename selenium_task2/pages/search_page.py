from selenium_task2.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium_task2.core.parse_price import parse_price


class SearchPage(BasePage):
    SORT_DROPDOWN = (By.ID, "sort_by_trigger")
    SORT_OPTION_PRICE_DESC = (By.XPATH, '//a[@id="Price_DESC"]')
    PRICES_LOCATOR_TEMPLATE = '(//div[contains(@class,"discount_final_price") or contains(@class,"col search_price")])[position() <= {n}]'

    def filter_dropdown(self):
        self.wait.until(EC.element_to_be_clickable(self.SORT_DROPDOWN)).click()

    def sort_by_price_desc(self):
        first_price = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.PRICES_LOCATOR_TEMPLATE.format(n=1)))
        )

        self.wait.until(EC.element_to_be_clickable(self.SORT_OPTION_PRICE_DESC)).click()

        self.wait.until(EC.staleness_of(first_price))

    def get_first_n_prices(self, n):
        locator = (By.XPATH, self.PRICES_LOCATOR_TEMPLATE.format(n=n))
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
