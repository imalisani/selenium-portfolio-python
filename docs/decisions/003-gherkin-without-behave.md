# 003 — Gherkin in the plans, markers in the code, no BDD runner

**Status:** accepted
**Date:** 2026-08

## Context

Test plans are written in Gherkin. The obvious next step is a BDD runner — `behave` or
`pytest-bdd` — so the `.feature` files execute directly.

## Decision

Gherkin stays in the plans as a communication artifact. The suite stays in plain pytest.
Plans and tests are linked by a shared vocabulary: `@smoke`, `@negative` and `@a11y`
appear as tags in the plan scenarios and as pytest markers in the code.

```bash
pytest -m smoke     # runs exactly what the plan marks as smoke
```

## Consequences

- The link between plan and code is queryable, not decorative: a reviewer can run the
  marker and watch the scenarios execute.
- No step-definition layer to maintain — the layer that breaks most often and that nobody
  wants to own.
- `--strict-markers` in `pytest.ini` means a typo in a marker fails the run instead of
  silently selecting nothing.
- Cost: plan and suite can drift, because nothing enforces the mapping mechanically.
  Mitigated by the traceability table in each plan.

## Alternatives rejected

**Executable Gherkin via `pytest-bdd`.** Worth it when non-technical people write or read
the scenarios routinely. In a repository this size it adds indirection, a second syntax to
debug, and a dependency, for no gain.

BDD's value is the conversation it forces, not the runner. The conversation already
happened — it is written in the plan.
