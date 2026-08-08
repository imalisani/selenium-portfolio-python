# selenium-portfolio-python

End-to-end tests for [Sauce Demo](https://www.saucedemo.com) built with Selenium and
Python, using the Page Object Model.

---

## Why this repository exists

The same application as its
[Playwright counterpart](https://github.com/imalisani/playwright-portfolio-typescript),
tested with a different driver.

Keeping both is deliberate. The tool is an implementation detail: what a test verifies,
and why it verifies it, should survive a change of driver. These two repositories are
where I check whether that holds in practice — and where the real differences between
the two become visible instead of theoretical.

Both suites use the same selector strategy and cover the same scenarios, so what is left
over is the genuine difference between the tools. So far that difference has one name:
**waiting**. Playwright auto-waits on every action; Selenium needs an explicit condition
for each one. [ADR-002](./docs/decisions/002-explicit-waits-only.md) is where that cost
is written down.

Sauce Demo is a practice application, so its defects are intentional and public. The
value here is not in finding them, but in how the checks are designed.

## Coverage

| Flow | Case | Type | Marker |
|---|---|---|---|
| Login | Successful login with `standard_user` | Positive | `smoke` |
| Login | Blocked access with `locked_out_user` | Negative | `negative` |
| Shopping cart | Add a product and verify the cart badge | Positive | `smoke` |
| Login page | No critical or serious WCAG violations | Accessibility | `a11y` |
| Inventory page | No critical or serious WCAG violations | Accessibility | `a11y` (expected failure, [BUG-001](./docs/bugs-reports/BUG-001-select-name-inventory.md)) |

Every test writes a screenshot to `evidence/`. Failures also write the page source.

## Test plans

The reasoning behind the suite — scope and exclusions, test data, risk analysis,
scenarios in Gherkin, and the section that matters most, **what is deliberately not
automated and why**:

- [`docs/test-plan-login.md`](./docs/test-plan-login.md)
- [`docs/test-plan-cart.md`](./docs/test-plan-cart.md)

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
confirmed against the Playwright suite: two drivers, two languages, two ways of loading
the same axe-core build, one identical result. It is marked as a strict expected failure
rather than left red — [ADR-005](./docs/decisions/005-known-defects-as-strict-xfail.md)
explains why, and what happens the day the application fixes it.

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
evidence/         Screenshots and axe reports from real executions
pytest.ini        Marker vocabulary, shared with the plans
requirements.txt
```

## Stack

Selenium WebDriver · Python · Pytest · Page Object Model · axe-core

## Running it

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

- [ ] Add checkout coverage
- [ ] Cross-browser execution (Firefox), matching the Playwright project matrix

## Related

[playwright-portfolio-typescript](https://github.com/imalisani/playwright-portfolio-typescript) —
the same application tested with Playwright and TypeScript.

## Author

Irina Malisani — Quality Engineer
[LinkedIn](https://linkedin.com/in/imalisani) · [GitHub](https://github.com/imalisani)
