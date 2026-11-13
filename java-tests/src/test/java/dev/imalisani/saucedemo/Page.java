package dev.imalisani.saucedemo;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;
import java.util.regex.Pattern;

abstract class Page {
    protected final WebDriver driver;
    protected final WebDriverWait wait;

    Page(WebDriver driver) {
        this.driver = driver;
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    protected void click(String name) {
        wait.until(ExpectedConditions.elementToBeClickable(selector(name))).click();
    }

    protected void type(String name, String value) {
        wait.until(ExpectedConditions.visibilityOfElementLocated(selector(name))).sendKeys(value);
    }

    protected String text(String name) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(selector(name))).getText();
    }

    protected List<String> itemNames() {
        return wait.until(ExpectedConditions.visibilityOfAllElementsLocatedBy(selector("inventory-item-name")))
                .stream().map(item -> item.getText()).toList();
    }

    protected void waitForItemCount(int count) {
        wait.until(ExpectedConditions.numberOfElementsToBe(selector("inventory-item-name"), count));
    }

    protected void waitForPath(String path) {
        wait.until(ExpectedConditions.urlMatches("/" + Pattern.quote(path) + "(?:[?#].*)?$"));
    }

    private static By selector(String name) {
        return By.cssSelector("[data-test='" + name + "']");
    }
}
