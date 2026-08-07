import os
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


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
