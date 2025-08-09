import time
import pytest
import string
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(2)
    yield driver
    driver.quit()

def test_login_with_random_credentials(driver):
    driver.get("https://store.steampowered.com/")
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    authorization_button= WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath",'//a[text()="войти"]')))
    authorization_button.click()
    assert "login" in driver.current_url

    login_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(("xpath", '(//input[@type="text"])[1]'))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(("xpath", '//input[@type="password"]'))
    )

    login_field.send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    password_field.send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    )
    driver.find_element("xpath", '//button[@type="submit"]').click()
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            "xpath", '//div[text()="Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."]'
        ))
    )
    assert "Пожалуйста, проверьте свой пароль" in error_message.text