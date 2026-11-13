package dev.imalisani.saucedemo;

import org.openqa.selenium.WebDriver;

final class CheckoutPage extends Page {
    CheckoutPage(WebDriver driver) {
        super(driver);
    }

    void enterCustomer(String firstName, String lastName) {
        type("firstName", firstName);
        type("lastName", lastName);
    }

    void enterPostalCode(String postalCode) {
        type("postalCode", postalCode);
    }

    void submitCustomerDetails() {
        click("continue");
    }

    CheckoutOverviewPage continueToOverview() {
        submitCustomerDetails();
        waitForPath("checkout-step-two.html");
        return new CheckoutOverviewPage(driver);
    }

    String validationError() {
        return text("error");
    }
}
