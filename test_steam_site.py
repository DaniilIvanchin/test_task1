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
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    yield driver
    driver.quit()

def test_login_with_random_credentials(driver):
    driver.get("https://store.steampowered.com/")

    authorization_button= WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath",'//*[@id="global_action_menu"]/a[2]')))
    authorization_button.click()
    driver.implicitly_wait(3)
    assert "login" in driver.current_url

    driver.find_elements("class name", "_2GBWeup5cttgbTw8FM3tfx")[0].send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8)))
    driver.find_elements("class name", "_2GBWeup5cttgbTw8FM3tfx")[1].send_keys(
        ''.join(random.choices(string.ascii_letters + string.digits, k=8)))
    time.sleep(3)
    driver.find_element("class name", "DjSvCZoKKfoNSmarsEcTS").click()
    time.sleep(3)
    assert "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова." in driver.find_element("class name",
                                                                                                         "_1W_6HXiG4JJ0By1qN_0fGZ").text
