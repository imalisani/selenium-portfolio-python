# selenium-portfolio-python

End-to-end tests for [Sauce Demo](https://www.saucedemo.com) built with Selenium and
the Page Object Model. The Python suite covers login, cart, and accessibility.
The [Java suite](#checkout-automation-with-java) covers checkout.

---

## Why this repository exists

The same application as its
[Playwright counterpart](https://github.com/imalisani/playwright-portfolio-typescript),
tested with a different driver.

Keeping both is deliberate. The tool is an implementation detail: what a test verifies,
and why it verifies it, should survive a change of driver. These two repositories are
where I check whether that holds in practice — and where the real differences between
the two become visible instead of theoretical.

The Python and Playwright suites use the same selector strategy for the shared scenarios, so what is left
over is the genuine difference between the tools. So far that difference has one name:
**waiting**. Playwright auto-waits on every action; Selenium needs an explicit condition
for each one. [ADR-002](./docs/decisions/002-explicit-waits-only.md) is where that cost
is written down.

Sauce Demo is a practice application, so its defects are intentional and public. The
value here is not in finding them, but in how the checks are designed.

## Python coverage

| Flow | Case | Type | Marker |
|---|---|---|---|
| Login | Successful login with `standard_user` | Positive | `smoke` |
| Login | Blocked access with `locked_out_user` | Negative | `negative` |
| Shopping cart | Add a product and verify the cart badge | Positive | `smoke` |
| Login page | No critical or serious WCAG violations | Accessibility | `a11y` |
| Inventory page | No critical or serious WCAG violations | Accessibility | `a11y` ([BUG-001 regression check](./docs/bugs-reports/BUG-001-select-name-inventory.md)) |

Every test writes a screenshot to `evidence/`. Failures also write the page source.

## Test plans

The reasoning behind the suite — scope and exclusions, test data, risk analysis,
scenarios in Gherkin, and the section that matters most, **what is deliberately not
automated and why**:

- [`docs/test-plan-login.md`](./docs/test-plan-login.md)
- [`docs/test-plan-cart.md`](./docs/test-plan-cart.md)

## Checkout automation with Java

[Selenium WebDriver 4, Java 17, JUnit 5, and Maven](./java-tests/pom.xml) exercise the public demo with synthetic checkout data. The [test class](./java-tests/src/test/java/dev/imalisani/saucedemo/CheckoutTest.java) contains the assertions, and Page Objects hold the `data-test` selectors and explicit waits. Each scenario starts a fresh Chrome session.

| Case | Risk | Expected result |
|---|---|---|
| WEB-CO-01 · Confirm an order | Incorrect charges or incomplete checkout | The backpack subtotal is $29.99, tax is $2.40, the total is $32.39, and the confirmation appears. |
| WEB-CO-02 · Omit and correct the postal code | Incomplete shipping details advance to review | The form shows a required-field error and opens the order overview after a postal code is entered. |
| WEB-CO-03 · Remove an item before checkout | A removed item is still included in the order | The cart count drops to one, and the order overview includes only the backpack and its subtotal. |

Run from the repository root with JDK 17, Maven 3.9+, and Chrome installed.

```bash
mvn -f java-tests/pom.xml test
mvn -f java-tests/pom.xml -Dheadless=false test
```

The [Selenium Java workflow](https://github.com/imalisani/selenium-portfolio-python/actions/workflows/selenium-java.yml) uploads `selenium-java-checkout-evidence` with JUnit XML, one screenshot per browser test, and HTML page source on test failure. Local evidence is under `java-tests/target/`.

## Decisions

Why the suite is built this way, including the alternatives that were rejected:

- [001 — Page Object Model, with selectors as class attributes](./docs/decisions/001-page-object-model.md)
- [002 — Explicit waits only, no implicit wait](./docs/decisions/002-explicit-waits-only.md)
- [003 — Gherkin in the plans, markers in the code, no BDD runner](./docs/decisions/003-gherkin-without-behave.md)
- [004 — Accessibility fails on serious, reports everything](./docs/decisions/004-accessibility-threshold.md)
- [005 — Known application defects are strict expected failures](./docs/decisions/005-known-defects-as-strict-xfail.md)

## Findings

[BUG-001 — Product sort dropdown has no accessible name](./docs/bugs-reports/BUG-001-select-name-inventory.md)

A real accessibility defect in Sauce Demo, found by this suite and independently
confirmed against the Playwright suite. Sauce Demo added an accessible name to
the dropdown, and the strict expected failure surfaced the fix on 2026-11-13.
The accessibility test now runs as a regular regression check.

## The rule this structure enforces

No selector ever appears in a test. Tests describe intent; `pages/` holds the locators.
When the UI changes, only the Page Object changes — the test that describes the
behaviour stays untouched. That separation is the entire point of the pattern, and the
first thing that erodes when a suite is written in a hurry.

The same applies to evidence: screenshots are taken by a fixture in `conftest.py`, not by
the tests. A test that has to remember to capture its own evidence will eventually
forget, and the run that matters most is the one that failed.

## Structure

```
docs/             Test plans, bug reports, and the decision records behind the suite
pages/            Page Objects — locators and actions, one class per screen
tests/            Tests. Intent and assertions only
java-tests/       Maven module for the Java checkout suite
evidence/         Screenshots and axe reports from real executions
pytest.ini        Marker vocabulary, shared with the plans
requirements.txt
```

## Python stack

Selenium WebDriver · Python · Pytest · Page Object Model · axe-core

## Running the Python suite

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```

Browsers run headed locally and headless in CI. Override with `HEADLESS=1` or
`HEADLESS=0`.

```bash
pytest -m smoke                  # only the core paths
pytest -m negative
pytest -m a11y                   # needs network access for axe-core
```

## Continuous integration

[`.github/workflows/selenium.yml`](./.github/workflows/selenium.yml) runs the suite on
every push and pull request, and uploads `evidence/` as an artifact.

There is no CI badge in this README on purpose. The suite runs against a third-party
application that can change without notice, so a red badge here would report someone
else's deployment rather than the state of this code.

## Roadmap

- [x] Add checkout coverage in Java
- [ ] Cross-browser execution (Firefox), matching the Playwright project matrix

## Related

[playwright-portfolio-typescript](https://github.com/imalisani/playwright-portfolio-typescript) —
the same application tested with Playwright and TypeScript.

## Author

Irina Malisani — Quality Engineer
[LinkedIn](https://linkedin.com/in/imalisani) · [GitHub](https://github.com/imalisani)
