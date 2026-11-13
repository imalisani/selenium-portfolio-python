package dev.imalisani.saucedemo;

import org.openqa.selenium.WebDriver;

final class LoginPage extends Page {
    LoginPage(WebDriver driver) {
        super(driver);
    }

    InventoryPage signInAsStandardUser() {
        driver.get("https://www.saucedemo.com/");
        type("username", "standard_user");
        type("password", "secret_sauce");
        click("login-button");
        waitForPath("inventory.html");
        return new InventoryPage(driver);
    }
}
