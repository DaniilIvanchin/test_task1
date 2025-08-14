import pytest
import string
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "https://store.steampowered.com/"
page_load_timeout = 15
auth_button = "xpath", '//a[text()="войти"]'


class waitless:
    def __call__(self, driver):
        try:
            element = driver.find_element("xpath", '//a[@class="global_action_link"]')
            return element if element.is_displayed() else False
        except:
            return False


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(base_url)
    WebDriverWait(driver, page_load_timeout).until(waitless())
    yield driver
    driver.quit()


def test_login_with_random_credentials(driver):
    authorization_button = WebDriverWait(driver, page_load_timeout).until(EC.element_to_be_clickable(auth_button))
    authorization_button.click()

    login_field = WebDriverWait(driver, page_load_timeout).until(
        EC.element_to_be_clickable(("xpath", '(//input[@type="text"])[1]'))
    )
    password_field = WebDriverWait(driver, page_load_timeout).until(
        EC.element_to_be_clickable(("xpath", '//input[@type="password"]'))
    )

    login_field.send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    password_field.send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    driver.find_element("xpath", '//button[@type="submit"]').click()

    error_container = (
        'xpath',
        "(//a[contains(@href,'HelpWithLogin')]/preceding-sibling::div[1])"
    )
    error_text = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."

    WebDriverWait(driver, page_load_timeout).until(
        lambda d: d.find_element(*error_container).text.strip() != ""
    )

    actual_text = driver.find_element(*error_container).text.strip()

    assert error_text in actual_text, (
        f"Expected: '{error_text}', actual: '{actual_text}'")
