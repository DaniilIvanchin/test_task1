from selenium_task2.core.base_test import BaseTest
import pytest


class TestMainPage(BaseTest):
    @pytest.mark.parametrize("lang", ["russian", "english"])
    def test_search(self, lang):
        self.base_page.open(lang)
        self.base_page.is_opened()
        self.base_page.enter_search("Fallout", lang)
        self.search_page.filter_dropdown()
        self.search_page.sort_by_price_desc()
        self.search_page.get_first_n_prices(20)
        self.search_page.is_sorted_by_desc_price(20)