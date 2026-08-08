# 001 — Page Object Model, with selectors as class attributes

**Status:** accepted
**Date:** 2026-08

## Context

Selenium offers no built-in page abstraction. Left alone, locators end up inline in the
tests, and a UI change turns into a search-and-replace across the suite.

## Decision

One class per screen under `pages/`. Locators are **class attributes**, not instance
attributes, so they can be read without constructing the page. Tests describe intent and
assertions; they never contain a selector.

## Consequences

- A UI change touches one Page Object. The test that describes the behaviour stays
  untouched, which is the entire point of the pattern.
- Locators declared as class attributes are inspectable and diffable in isolation — a
  reviewer can see the contract with the DOM without reading the constructor.
- Cost: an extra indirection for someone reading a single test in isolation.

## Alternatives rejected

**Inline locators.** Faster to write for the first two tests, and the reason most sample
suites become unmaintainable by the tenth.

**Page factories with `@FindBy`.** Idiomatic in Java Selenium, not in Python, and it hides
the wait strategy behind a proxy — which is the thing this repository most wants to keep
visible.
