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

Sauce Demo is a practice application, so its defects are intentional and public. The
value here is not in finding them, but in how the checks are designed.

## Coverage

| Flow | Case | Type |
|---|---|---|
| Shopping cart | Add a product and verify cart contents | Positive |

Evidence from real executions is stored in `evidence/`.

## Test plan

[`docs/test-plan-cart.md`](./docs/test-plan-cart.md) holds the reasoning behind the
suite: scope and exclusions, test data, risk analysis, scenarios in Gherkin, and — the
section that matters most — **what is deliberately not automated, and why**.

## The rule this structure enforces

No selector ever appears in a test. Tests describe intent; `pages/` holds the locators.
When the UI changes, only the Page Object changes — the test that describes the
behaviour stays untouched. That separation is the entire point of the pattern, and the
first thing that erodes when a suite is written in a hurry.

## Structure

```
docs/             Test plans in Gherkin — the reasoning behind the suite
pages/            Page Objects — locators and actions, one class per screen
tests/            Tests. Intent and assertions only
evidence/         Screenshots from real executions
requirements.txt
```

## Stack

Selenium WebDriver · Python · Pytest · Page Object Model

## Running it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

## Roadmap

- [ ] **Port the login scenario from the Playwright suite**, so both repositories cover
      at least one identical case. That comparison is what this pair is for
- [ ] Document the explicit-wait strategy — the clearest practical difference against
      Playwright's auto-waiting
- [ ] Add checkout coverage
- [ ] Add a CI workflow, matching the Playwright repository

## Related

[playwright-portfolio-typescript](https://github.com/imalisani/playwright-portfolio-typescript) —
the same application tested with Playwright and TypeScript.

## Author

Irina Malisani — Quality Engineer
[LinkedIn](https://linkedin.com/in/imalisani) · [GitHub](https://github.com/imalisani)
