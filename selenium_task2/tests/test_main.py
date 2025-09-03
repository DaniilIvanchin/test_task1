import pytest
from selenium_task2.pages.home_page import HomePage
from selenium_task2.pages.search_page import SearchPage

class TestMainPage:
    @pytest.mark.parametrize(
        "game_name, n",
        [
            ("The Witcher", 10),
            ("Fallout", 20),
        ]
    )
    def test_search_sort_by_price_desc(self, driver, game_name, open_home, n):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        home_page.is_opened()
        home_page.enter_search(game_name)
        search_page.filter_dropdown()
        search_page.sort_by_price_desc()
        prices = search_page.get_first_n_prices(n)

        expected = sorted(prices, reverse=True)
        assert len(prices) == n, f"Expected {n} prices, but got {len(prices)}"
        assert prices == expected, f"Prices are not sorted descending.\nExpected: {expected}\nActual:   {prices}"
