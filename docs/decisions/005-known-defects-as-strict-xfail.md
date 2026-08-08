# 005 — Known application defects are strict expected failures, not red builds

**Status:** accepted
**Date:** 2026-08

## Context

The accessibility suite found a real defect in the application under test
([BUG-001](../bugs-reports/BUG-001-select-name-inventory.md)): a `<select>` with no
accessible name. The application is a third party. There is no version of this
repository in which the defect gets fixed.

That leaves a documented finding and a permanently failing check — and
[ADR-004](./004-accessibility-threshold.md) already argues that a check which never goes
green gets ignored, and an ignored check protects nothing.

## Decision

A known, reported, unfixable-by-us defect is marked
`@pytest.mark.xfail(strict=True)` with the bug report referenced in the reason.

`strict=True` is the whole point: if the assertion ever **passes**, pytest fails the
run.

## Consequences

- The check stays live. It is still executed, still reports every violation to
  `evidence/`, and still catches any *new* critical or serious violation, because those
  are different tests.
- The suite is green when the application is in its known state, so a red build means
  something actually changed. A build that is always red carries no information.
- The day the application is fixed, the run turns red and points at a bug report that
  has become false. Stale bug reports are a real cost in a portfolio: a finding nobody
  rechecked is a finding nobody can trust.
- Cost: `xfail` is easy to reach for when a test is merely flaky. The rule is that it
  requires a written bug report — no report, no `xfail`.

## Alternatives rejected

**Leave it failing.** Honest, and it was the initial stance. But it makes the CI badge
permanently red, trains the reader to ignore the result, and gives no signal when
something new breaks.

**Skip the test.** Removes the execution entirely, so the violation report stops being
generated and a change in the application goes unnoticed. Skipping hides; `xfail`
documents.

**Lower the threshold to exclude `select-name`.** Silently narrows what the suite
considers accessible, and the narrowing lives in configuration where nobody reads it.
The defect stops being visible as a defect.
