import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_add_a_single_product_to_the_cart(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.goto()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.add_backpack_to_cart()

    assert inventory_page.get_cart_count() == "1"
