package dev.imalisani.saucedemo;

import org.openqa.selenium.WebDriver;

import java.util.List;

final class CartPage extends Page {
    CartPage(WebDriver driver) {
        super(driver);
    }

    void removeBikeLight() {
        click("remove-sauce-labs-bike-light");
        waitForItemCount(1);
    }

    String badgeCount() {
        return text("shopping-cart-badge");
    }

    List<String> products() {
        return itemNames();
    }

    CheckoutPage startCheckout() {
        click("checkout");
        waitForPath("checkout-step-one.html");
        return new CheckoutPage(driver);
    }
}
