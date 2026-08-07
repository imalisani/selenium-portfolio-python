# Test Plan — Shopping Cart

## Scope

Verify that a logged-in user can add a product to the cart and that the cart
badge reflects the correct count.

### In scope

- Add a single product (Sauce Labs Backpack) to the cart.
- Assert the cart badge displays "1".

### Out of scope

- Removing products from the cart.
- Adding multiple products or duplicate products.
- Cart persistence across sessions.
- Checkout flow (covered in a future plan).

## Test data

| User | Password | Behaviour |
|---|---|---|
| `standard_user` | `secret_sauce` | Normal user, no restrictions |

## Risk analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Cart badge does not appear after adding item | Low | High | Explicit wait on badge visibility |
| Login fails before reaching inventory | Low | High | Separate login test catches this independently |
| Selector changes in Sauce Demo UI | Medium | Medium | Selectors isolated in Page Objects — single place to update |

## Scenarios (Gherkin)

```gherkin
Feature: Shopping cart

  Scenario: Add a single product to the cart
    Given the user is logged in as "standard_user"
    When the user adds "Sauce Labs Backpack" to the cart
    Then the cart badge should display "1"
```

## What is deliberately not automated, and why

| Scenario | Reason |
|---|---|
| Remove a product from the cart | Not yet in scope — will be added with checkout coverage |
| Add every product and verify total | Combinatorial, low risk — manual spot-check is sufficient for now |
| Cart state after browser refresh | Depends on session/cookie behaviour outside the application's core flow |
| Visual appearance of the cart icon | Visual regression testing requires a dedicated tool (e.g., Percy) and is out of scope for this suite |
