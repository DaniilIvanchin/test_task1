import pytest
import string
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BASE_URL = "https://store.steampowered.com/"
PAGE_LOAD_TIMEOUT = 15
AUTH_BUTTON = By.XPATH, '//a[text()="войти"]'
GLOBAL_ACTION_LINK = (By.XPATH, '//a[contains(@class, "global_action_link")]')


class WaitLess:
    def __call__(self, driver):
        try:
            element = driver.find_element(*GLOBAL_ACTION_LINK)
            return element if element.is_displayed() else False
        except:
            return False


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(WaitLess())
    yield driver
    driver.quit()


def test_login_with_random_credentials(driver):
    authorization_button = WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.element_to_be_clickable(AUTH_BUTTON))
    authorization_button.click()

    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(WaitLess())

    login_field = WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '(//input[@type="text"])[1]'))
    )
    password_field = WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))
    )

    login_field.send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    password_field.send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    ERROR_CONTAINER = (By.XPATH, "(//a[contains(@href,'HelpWithLogin')]/preceding-sibling::div[1])")
    ERROR_TEXT = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."

    ELEMENT = WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        EC.visibility_of_element_located(ERROR_CONTAINER)
    )

    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        lambda d: ELEMENT.text.strip() != ""
    )

    ACTUAL_TEXT = ELEMENT.text.strip()

    assert ERROR_TEXT in ACTUAL_TEXT, (
        f"Expected: '{ERROR_TEXT}', actual: '{ACTUAL_TEXT}'")
