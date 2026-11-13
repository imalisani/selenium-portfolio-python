package dev.imalisani.saucedemo;

import org.openqa.selenium.WebDriver;

import java.util.List;

final class CheckoutOverviewPage extends Page {
    CheckoutOverviewPage(WebDriver driver) {
        super(driver);
    }

    List<String> products() {
        return itemNames();
    }

    String subtotal() {
        return text("subtotal-label");
    }

    String tax() {
        return text("tax-label");
    }

    String total() {
        return text("total-label");
    }

    String finishOrder() {
        click("finish");
        waitForPath("checkout-complete.html");
        return text("complete-header");
    }
}
