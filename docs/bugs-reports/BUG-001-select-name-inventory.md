# BUG-001 — Product sort dropdown has no accessible name on inventory page

**Application:** [Sauce Demo](https://www.saucedemo.com)
**Area:** Inventory page — product sort control
**Reported by:** Irina Malisani
**Date:** 2026-08
**Defect nature:** authentic
**Status:** fixed in Sauce Demo, verified 2026-11-13

---

## Summary

The product sort `<select>` element (`[data-test="product-sort-container"]`) on the
inventory page had no associated `<label>`, `aria-label`, or `aria-labelledby`
attribute. Screen reader users heard "combo box" with no indication of what the control
does.

**Severity:** critical · **Priority:** p1 · **WCAG:** 4.1.2 Name, Role, Value (Level A)
· **axe rule:** `select-name`

## Independent confirmation

This defect was first reported from the
[Playwright suite](https://github.com/imalisani/playwright-portfolio-typescript/blob/main/docs/bugs-reports/BUG-001-accessibility-login.md),
which holds the full analysis: severity justification, failing markup, the six naming
checks axe evaluates, impact analysis and the recommended one-attribute fix. That
document is the source of truth and is not duplicated here.

What this repository adds is **independent reproduction**:

| | Playwright suite | This suite |
|---|---|---|
| Driver | Playwright | Selenium WebDriver |
| Language | TypeScript | Python |
| axe-core delivery | `@axe-core/playwright` | `axe.min.js` injected from a pinned CDN build |
| Browsers | Chromium, Firefox, WebKit | Chromium |
| Result | `select-name`, critical | `select-name`, critical |

Two drivers, two languages, two ways of loading the same engine, one identical finding.
That rules out the tooling as the cause and leaves the application.

It is also the reason [ADR-004](../decisions/004-accessibility-threshold.md) rejects
wrapper packages that pin their own `axe-core`: had the two suites run different engine
versions, a matching result would have proved nothing.

## Detection

- Test: `tests/test_accessibility.py::test_inventory_page_has_no_critical_or_serious_wcag_violations`
- Originally marked `xfail(strict=True)` per [ADR-005](../decisions/005-known-defects-as-strict-xfail.md)
- Full violation report: `evidence/axe-inventory-page.json`, written on every run

## Fix verification

On 2026-11-13 the strict expected failure reported `XPASS`. The captured HTML
showed `aria-label="Sort products"` on the dropdown, and axe reported zero
violations on the inventory page. The test now runs as a regular regression check.
[GitHub Actions run and evidence](https://github.com/imalisani/selenium-portfolio-python/actions/runs/43505540336)
