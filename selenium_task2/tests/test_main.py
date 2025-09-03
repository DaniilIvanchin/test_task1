import pytest


class TestMainPage:
    def test_search_sort_by_price_desc(self, home_page, search_page):
        n = 10
        home_page.open()
        home_page.is_opened()
        home_page.enter_search("The Witcher")
        search_page.filter_dropdown()
        search_page.sort_by_price_desc()
        prices = search_page.get_first_n_prices(n)
        assert prices == sorted(prices, reverse=True)