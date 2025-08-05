import pytest
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def test_enter_site():
    driver.get("https://store.steampowered.com/")
    assert "Steam" in driver.title