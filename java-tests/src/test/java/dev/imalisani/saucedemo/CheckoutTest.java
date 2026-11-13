package dev.imalisani.saucedemo;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.AfterTestExecutionCallback;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.RegisterExtension;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CheckoutTest {
    private static final Path EVIDENCE = Path.of("target", "evidence");
    private static final String BACKPACK = "Sauce Labs Backpack";
    private static final String BIKE_LIGHT = "Sauce Labs Bike Light";

    private ChromeDriver driver;

    @RegisterExtension
    final AfterTestExecutionCallback evidence = this::captureEvidence;

    @BeforeEach
    void startBrowser() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--window-size=1440,1000");
        options.setExperimentalOption("prefs", Map.of(
                "credentials_enable_service", false,
                "profile.password_manager_enabled", false,
                "profile.password_manager_leak_detection", false));
        if (Boolean.parseBoolean(System.getProperty("headless", "true"))) {
            options.addArguments("--headless=new");
        }
        driver = new ChromeDriver(options);
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
    }

    @AfterEach
    void closeBrowser() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    @Tag("smoke")
    @DisplayName("WEB-CO-01 Checkout shows the expected charges and confirms the order")
    void confirmsOrderWithExpectedCharges() {
        CheckoutPage checkout = cartWithBackpack().startCheckout();
        checkout.enterCustomer("Alex", "Tester");
        checkout.enterPostalCode("10001");

        CheckoutOverviewPage overview = checkout.continueToOverview();
        assertAll("Checkout overview",
                () -> assertEquals(List.of(BACKPACK), overview.products()),
                () -> assertEquals("Item total: $29.99", overview.subtotal()),
                () -> assertEquals("Tax: $2.40", overview.tax()),
                () -> assertEquals("Total: $32.39", overview.total()));

        assertEquals("Thank you for your order!", overview.finishOrder());
    }

    @Test
    @Tag("negative")
    @DisplayName("WEB-CO-02 A missing postal code blocks checkout until it is entered")
    void blocksCheckoutUntilPostalCodeIsProvided() {
        CheckoutPage checkout = cartWithBackpack().startCheckout();
        checkout.enterCustomer("Alex", "Tester");

        checkout.submitCustomerDetails();
        assertEquals("Error: Postal Code is required", checkout.validationError());

        checkout.enterPostalCode("10001");
        CheckoutOverviewPage overview = checkout.continueToOverview();
        assertEquals(List.of(BACKPACK), overview.products());
    }

    @Test
    @Tag("regression")
    @DisplayName("WEB-CO-03 Removing a product updates the cart and checkout subtotal")
    void excludesRemovedProductFromCheckout() {
        InventoryPage inventory = new LoginPage(driver).signInAsStandardUser();
        inventory.addBackpack();
        inventory.addBikeLight();
        CartPage cart = inventory.openCart();
        assertEquals(List.of(BACKPACK, BIKE_LIGHT), cart.products());
        assertEquals("2", cart.badgeCount());

        cart.removeBikeLight();
        assertEquals(List.of(BACKPACK), cart.products());
        assertEquals("1", cart.badgeCount());

        CheckoutPage checkout = cart.startCheckout();
        checkout.enterCustomer("Alex", "Tester");
        checkout.enterPostalCode("10001");
        CheckoutOverviewPage overview = checkout.continueToOverview();
        assertAll("Checkout after removing the bike light",
                () -> assertEquals(List.of(BACKPACK), overview.products()),
                () -> assertEquals("Item total: $29.99", overview.subtotal()));
    }

    private CartPage cartWithBackpack() {
        InventoryPage inventory = new LoginPage(driver).signInAsStandardUser();
        inventory.addBackpack();
        return inventory.openCart();
    }

    private void captureEvidence(ExtensionContext context) {
        String name = context.getRequiredTestMethod().getName();
        try {
            Files.createDirectories(EVIDENCE);
            Files.write(EVIDENCE.resolve(name + ".png"), driver.getScreenshotAs(OutputType.BYTES));
        } catch (IOException | WebDriverException error) {
            System.err.println("Could not save screenshot for " + name + ": " + error.getMessage());
        }

        if (context.getExecutionException().isPresent()) {
            try {
                Files.writeString(EVIDENCE.resolve(name + ".html"), driver.getPageSource());
            } catch (IOException | WebDriverException error) {
                System.err.println("Could not save page source for " + name + ": " + error.getMessage());
            }
        }
    }
}
