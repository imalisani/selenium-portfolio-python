# Test Plan — Shopping Cart

## Scope

Verify that a logged-in user can add a product to the cart and that the cart badge
reflects the correct count.

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
| Cart badge does not appear after adding item | Low | High | Explicit wait on badge visibility — see [ADR-002](./decisions/002-explicit-waits-only.md) |
| The badge renders before the cart state updates | Low | High | The assertion reads the badge text, not its presence. A visible badge showing the wrong count is the defect worth catching |
| Login fails before reaching inventory | Low | High | Covered independently by the login plan, so a failure here points at the cart rather than at authentication |
| Selector changes in the Sauce Demo UI | Medium | Medium | Selectors isolated in Page Objects, using `data-test` attributes rather than styling hooks |

## Scenarios (Gherkin)

```gherkin
Feature: Shopping cart

  @smoke
  Scenario: Add a single product to the cart
    Given the user is logged in as "standard_user"
    When the user adds "Sauce Labs Backpack" to the cart
    Then the cart badge should display "1"
```

## Traceability

| Scenario | Tag | Test |
|---|---|---|
| Add a single product to the cart | `@smoke` | `tests/test_cart.py::test_add_a_single_product_to_the_cart` |

## What is deliberately not automated, and why

| Scenario | Reason |
|---|---|
| Remove a product from the cart | Not yet in scope — will be added with checkout coverage |
| Add every product and verify total | Combinatorial, low risk — a manual spot-check is sufficient for now |
| Cart state after browser refresh | Depends on session and cookie behaviour outside the application's core flow |
| Visual appearance of the cart icon | Visual regression needs a dedicated tool and a baseline to compare against; asserting it here would test the screenshot, not the cart |
