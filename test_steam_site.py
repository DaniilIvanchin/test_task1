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
HOME_FEATURED_TITLE = By.XPATH, "//*[@id='home_featured_and_recommended']"
LOGIN_BUTTON = (By.XPATH, "//body[contains(@class, 'login v6 global responsive_page')]")
wait = None

@pytest.fixture
def driver():
    global wait
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, PAGE_LOAD_TIMEOUT)
    wait.until(EC.visibility_of_element_located(GLOBAL_ACTION_LINK))
    wait.until(EC.visibility_of_element_located(HOME_FEATURED_TITLE))
    yield driver
    driver.quit()


def test_login_with_random_credentials(driver):
    authorization_button = WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.element_to_be_clickable(AUTH_BUTTON))
    authorization_button.click()

    wait.until(EC.visibility_of_element_located(LOGIN_BUTTON))

    login_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '(//input[@type="text"])[1]'))
    )
    password_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))
    )

    login_field.send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    password_field.send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    error_container = (By.XPATH,
                       "(//a[contains(@href,'HelpWithLogin')]/preceding-sibling::div[1][string-length(normalize-space(text())) > 1])")
    error_text = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."

    element = wait.until(
        EC.visibility_of_element_located(error_container)
    )

    actual_text = element.text.strip()

    assert error_text in actual_text, (
        f"Expected: '{error_text}', actual: '{actual_text}'")
