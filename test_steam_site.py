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
AUTH_BUTTON = (By.XPATH, '//a[text()="войти"]')
GLOBAL_ACTION_LINK = (By.XPATH, '//a[contains(@class, "global_action_link")]')
LOGIN_BUTTON = (By.XPATH, "//body[contains(@class, 'login')]")
ERROR_CONTAINER = (By.XPATH,
                   "(//a[contains(@href,'HelpWithLogin')]/preceding-sibling::div[1][string-length(normalize-space(text())) > 1])")
ERROR_TEXT = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."
LOGIN_FIELD = (By.XPATH, '//input[@type="text"]')
PASSWORD_FIELD = (By.XPATH, '//input[@type="password"]')


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.visibility_of_element_located(GLOBAL_ACTION_LINK))
    yield driver
    driver.quit()


def new_test (driver):
    wait = WebDriverWait(driver, PAGE_LOAD_TIMEOUT)
    authorization_button = wait.until(EC.element_to_be_clickable(AUTH_BUTTON))
    authorization_button.click()

    wait.until(EC.visibility_of_element_located(LOGIN_BUTTON))

    wait.until(EC.visibility_of_element_located(LOGIN_FIELD)).send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )

    wait.until(EC.visibility_of_element_located(PASSWORD_FIELD)).send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    submit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
    )
    submit_button.click()

    element = wait.until(
        EC.presence_of_element_located(ERROR_CONTAINER)
    )

    actual_text = element.text.strip()

    assert ERROR_TEXT in actual_text, (
        f"Expected: '{ERROR_TEXT}', actual: '{actual_text}'")
