import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_agregar_producto_al_carrito(driver):
    driver.get("https://www.saucedemo.com/")
    
    login_page = LoginPage(driver)
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()
    
    inventory_page = InventoryPage(driver)
    inventory_page.add_backpack_to_cart()
    
    os.makedirs("evidence", exist_ok=True)
    driver.save_screenshot("evidence/evidencia_carrito.png")
    assert inventory_page.get_cart_count() == "1"