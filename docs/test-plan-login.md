# Test Plan — Login

## Scope

Verify that authentication behaves correctly for a permitted user and for a user the
application has blocked.

### In scope

- Successful login with `standard_user`, landing on the inventory page.
- Blocked access with `locked_out_user`, with the error message shown to the user.

### Out of scope

- Password recovery — Sauce Demo does not implement it.
- Session expiry and remember-me — no such behaviour exists in the application.
- Brute-force protection and rate limiting — not observable from the UI.
- The remaining Sauce Demo users (`problem_user`, `performance_glitch_user`), which
  exercise inventory rendering rather than authentication.

## Test data

| User | Password | Behaviour |
|---|---|---|
| `standard_user` | `secret_sauce` | Normal user, no restrictions |
| `locked_out_user` | `secret_sauce` | Blocked by the application |

## Risk analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| A blocked user reaches the inventory | Low | Critical | The negative test asserts the URL as well as the message — a visible error with a successful redirect would still be a defect |
| The error message changes wording | Medium | Low | Asserted as an exact string; a wording change should fail loudly and be reviewed, not absorbed by a substring match |
| Login succeeds but the page is not ready | Medium | Medium | Assert the page title, not just the URL. A redirect is not a loaded page |
| Selector changes in the Sauce Demo UI | Medium | Medium | Selectors isolated in Page Objects, using `data-test` attributes rather than styling hooks |

## Scenarios (Gherkin)

```gherkin
Feature: Login

  @smoke
  Scenario: Successful login with a standard user
    Given the user is on the login page
    When the user logs in as "standard_user"
    Then the inventory page is displayed
    And the page title reads "Products"

  @negative
  Scenario: Blocked user cannot access the system
    Given the user is on the login page
    When the user logs in as "locked_out_user"
    Then an error message states the user has been locked out
    And the inventory page is not displayed
```

## Traceability

| Scenario | Tag | Test |
|---|---|---|
| Successful login with a standard user | `@smoke` | `tests/test_login.py::test_successful_login_with_a_standard_user` |
| Blocked user cannot access the system | `@negative` | `tests/test_login.py::test_blocked_user_cannot_access_the_system` |

## What is deliberately not automated, and why

| Scenario | Reason |
|---|---|
| Empty username or password | The application's own validation, not a business rule. One manual check is enough; automating every field combination buys coverage numbers, not confidence |
| Login with `problem_user` | The defects it exposes are in inventory rendering. It belongs to a visual or inventory plan, not to authentication |
| Timing behaviour of `performance_glitch_user` | Performance belongs in a load tool with thresholds, not in a functional suite where it produces flakiness |
| Password field masking | Verifiable by inspection in seconds; an automated assertion on `type="password"` tests the browser, not the application |
