import time

import pytest
import string
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def test_enter_site():
    driver.get("https://store.steampowered.com/")
    assert "https://store.steampowered.com/" in driver.current_url

def test_click_site():
    driver.find_elements("class name", "global_action_link")[0].click()
    driver.implicitly_wait(2)
    assert "login" in driver.current_url

def test_enter_password():
    driver.find_elements("class name", "_2GBWeup5cttgbTw8FM3tfx")[0].send_keys(''.join(random.choices(string.ascii_letters + string.digits, k=8)))
    driver.find_elements("class name", "_2GBWeup5cttgbTw8FM3tfx")[1].send_keys(''.join(random.choices(string.ascii_letters + string.digits, k=8)))
    time.sleep(3)
