from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    """Product listing shown after a successful login."""

    TIMEOUT = 10

    TITLE = (By.CSS_SELECTOR, ".title")
    INVENTORY_LIST = (By.CSS_SELECTOR, '[data-test="inventory-list"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    ADD_BACKPACK_BUTTON = (
        By.CSS_SELECTOR,
        '[data-test="add-to-cart-sauce-labs-backpack"]',
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def get_title(self):
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def add_backpack_to_cart(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_BACKPACK_BUTTON)
        ).click()

    def get_cart_count(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.CART_BADGE)
        ).text
