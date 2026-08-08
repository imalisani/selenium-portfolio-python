# 002 — Explicit waits only, no implicit wait

**Status:** accepted
**Date:** 2026-08

## Context

Selenium offers three ways to wait: implicit waits, explicit waits, and `sleep`.
Playwright, the counterpart repository, auto-waits on every action and needs none of
this. That difference is the most practical thing this pair of repositories can show.

## Decision

Every interaction goes through `WebDriverWait` with an explicit
`expected_condition`. The implicit wait is never set. `sleep` is never used.

`WebDriverWait` lives in the Page Object, not in the test.

## Consequences

- Each wait states *what* it is waiting for. `element_to_be_clickable` and
  `visibility_of_element_located` are different assertions about readiness, and mixing
  them up is a real defect rather than a slow test.
- Mixing implicit and explicit waits produces unpredictable compound timeouts. Setting
  the implicit wait to zero removes that class of problem entirely.
- Cost: more code than Playwright needs for the same behaviour. That cost **is** the
  finding — it is what the comparison exists to make visible.

## Alternatives rejected

**Implicit wait globally.** One line, covers everything, and silently waits on assertions
that expect an element to be *absent* — turning a fast negative check into a guaranteed
timeout.

**`time.sleep`.** Passes locally, fails in CI, and the fix is always to make the number
bigger.
