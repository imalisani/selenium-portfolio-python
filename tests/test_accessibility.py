import json
import os
from functools import lru_cache
from urllib.request import urlopen

import pytest

from pages.login_page import LoginPage

AXE_VERSION = "4.10.2"
AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@" + AXE_VERSION + "/axe.min.js"
WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]
BLOCKING_IMPACTS = ("critical", "serious")
EVIDENCE_DIR = "evidence"

ANALYZE = """
const done = arguments[arguments.length - 1];
axe.run(document, { runOnly: { type: 'tag', values: arguments[0] } })
   .then(results => done({ violations: results.violations }))
   .catch(error => done({ error: String(error) }));
"""


@lru_cache(maxsize=1)
def _axe_source():
    with urlopen(AXE_CDN, timeout=60) as response:
        return response.read().decode("utf-8")


def _analyze(driver, report_name):
    driver.set_script_timeout(60)
    driver.execute_script(_axe_source())
    results = driver.execute_async_script(ANALYZE, WCAG_TAGS)

    assert "error" not in results, "axe-core failed to run: " + str(
        results.get("error")
    )
    violations = results["violations"]

    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    path = os.path.join(EVIDENCE_DIR, report_name)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(violations, handle, indent=2)

    return violations


def _describe(violations):
    return "\n".join(
        "[{impact}] {id}: {help} ({count} nodes)".format(
            impact=v["impact"],
            id=v["id"],
            help=v["help"],
            count=len(v["nodes"]),
        )
        for v in violations
    )


def _assert_no_blocking_violations(violations):
    blocking = [v for v in violations if v.get("impact") in BLOCKING_IMPACTS]
    assert blocking == [], _describe(blocking)


@pytest.mark.a11y
def test_login_page_has_no_critical_or_serious_wcag_violations(driver):
    LoginPage(driver).goto()

    violations = _analyze(driver, "axe-login-page.json")

    _assert_no_blocking_violations(violations)


@pytest.mark.a11y
@pytest.mark.xfail(
    strict=True,
    reason=(
        "BUG-001: the product sort <select> has no accessible name. "
        "Known defect in the application under test, not in this suite. "
        "strict=True means this turns red the day Sauce Demo fixes it. "
        "See docs/bugs-reports/BUG-001-select-name-inventory.md"
    ),
)
def test_inventory_page_has_no_critical_or_serious_wcag_violations(driver):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")

    violations = _analyze(driver, "axe-inventory-page.json")

    _assert_no_blocking_violations(violations)
