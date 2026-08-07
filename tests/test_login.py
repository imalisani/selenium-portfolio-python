import os
import pytest
from pages.login_page import LoginPage


def test_login_exitoso(driver):
    driver.get("https://www.saucedemo.com/")

    login_page = LoginPage(driver)

    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    os.makedirs("evidence", exist_ok=True)
    driver.save_screenshot("evidence/evidencia_login.png")
    assert "inventory.html" in driver.current_url
