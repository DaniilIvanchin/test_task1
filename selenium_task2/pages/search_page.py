from selenium_task2.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SearchPage(BasePage):
    SORT_DROPDOWN = (By.XPATH, '//button[@id="sort_by_trigger"]')
    SORT_OPTION_PRICE_DESC = (By.XPATH, '//a[@id="Price_DESC"]')

    def filter_dropdown(self):
        self.wait.until(EC.element_to_be_clickable(self.SORT_DROPDOWN)).click()

    def sort_by_price_desc(self):
        self.wait.until(EC.element_to_be_clickable(self.SORT_OPTION_PRICE_DESC)).click()

    def get_first_n_prices(self, n):
        locator = (By.XPATH,
                   f'(//div[contains(@class,"discount_final_price") or contains(@class,"col search_price")])[position() <= {n}]')
        elements = self.wait.until(EC.presence_of_all_elements_located(locator))

        prices = []
        for el in elements[:n]:
            text = el.text.strip()
            if not text:
                continue

            cleaned = (
                text.replace("₸", "")
                .replace("$", "")
                .replace("руб.", "")
                .replace(",", ".")
                .replace("\u202f", "")
                .replace("\u00A0", "")
                .strip()
            )

            parts = cleaned.split()
            if parts:
                cleaned = parts[-1]

            try:
                prices.append(float(cleaned))
            except ValueError:
                continue
        return prices

    def is_sorted_by_desc_price(self, n):
        prices = self.get_first_n_prices(n)
        return prices == sorted(prices, reverse=True)
