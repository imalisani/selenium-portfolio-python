import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PASSWORD = "secret_sauce"


@pytest.mark.smoke
def test_successful_login_with_a_standard_user(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.goto()
    login_page.login(STANDARD_USER, PASSWORD)

    assert "inventory.html" in driver.current_url
    assert inventory_page.get_title() == "Products"


@pytest.mark.negative
def test_blocked_user_cannot_access_the_system(driver):
    login_page = LoginPage(driver)

    login_page.goto()
    login_page.login(LOCKED_OUT_USER, PASSWORD)

    assert (
        login_page.get_error_message()
        == "Epic sadface: Sorry, this user has been locked out."
    )
    assert "inventory.html" not in driver.current_url
