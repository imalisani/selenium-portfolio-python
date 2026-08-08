# 004 — Accessibility fails on serious, reports everything

**Status:** accepted
**Date:** 2026-08

## Context

`axe-core` grades WCAG violations by impact: minor, moderate, serious, critical. A test
that fails on any violation will never pass against a real application.

There is no maintained Python wrapper for `axe-core`. The Playwright repository uses
`@axe-core/playwright`, itself a thin wrapper that injects the same `axe.min.js` into the
page.

## Decision

Inject `axe-core` directly from a **pinned** CDN version and call `axe.run` through
`execute_async_script`. No wrapper package.

The test fails only on **critical** and **serious** violations. Every violation, at every
impact level, is written to `evidence/axe-*.json`.

## Consequences

- Pinning the version means an upstream release cannot silently change what the suite
  considers a violation. Upgrading is a deliberate, reviewable commit.
- Both repositories run the same `axe-core` against the same pages, so a difference in
  results is a real difference and not a difference between wrappers.
- The gate is one a team can keep. A check that never goes green gets disabled, and a
  disabled check protects nothing.
- Cost: the run needs network access to the CDN, which adds a third-party dependency to a
  suite that already depends on a third-party SUT.

## Alternatives rejected

**`axe-selenium-python`.** Unmaintained, and it pins an old `axe-core` internally. A
stale accessibility ruleset is worse than none, because it reports confidence it has not
earned.

**Fail on any violation.** On an existing application it produces a permanently red
check, and a permanently red check teaches the team to ignore red checks.

**Report only, never fail.** Then it is not a test.
