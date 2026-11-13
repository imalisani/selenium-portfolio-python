package dev.imalisani.saucedemo;

import org.openqa.selenium.WebDriver;

final class InventoryPage extends Page {
    InventoryPage(WebDriver driver) {
        super(driver);
    }

    void addBackpack() {
        click("add-to-cart-sauce-labs-backpack");
    }

    void addBikeLight() {
        click("add-to-cart-sauce-labs-bike-light");
    }

    CartPage openCart() {
        click("shopping-cart-link");
        waitForPath("cart.html");
        return new CartPage(driver);
    }
}
