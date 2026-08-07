from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)
        self.add_backpack_btn = (By.ID, "add-to-cart-sauce-labs-backpack")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

    def add_backpack_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.add_backpack_btn)).click()

    def get_cart_count(self):
        return self.wait.until(EC.visibility_of_element_located(self.cart_badge)).text
