import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

EVIDENCE_DIR = "evidence"


def _is_headless():
    """Headless by default in CI, headed locally. Override with HEADLESS=1|0."""
    default = "1" if os.getenv("CI") else "0"
    return os.getenv("HEADLESS", default) == "1"


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Expose each phase result on the item so fixtures can read the outcome."""
    outcome = yield
    setattr(item, "report_" + outcome.get_result().when, outcome.get_result())


@pytest.fixture
def driver(request):
    options = Options()
    if _is_headless():
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    yield driver

    _capture_evidence(driver, request.node)
    driver.quit()


def _capture_evidence(driver, node):
    """Every test leaves a screenshot. Failures also leave the DOM.

    Evidence is written by the fixture, not by the tests: a test that has to
    remember to screenshot itself will eventually forget, and the run that
    matters most is the one that failed.
    """
    slug = node.name.removeprefix("test_").replace("_", "-")
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

    driver.save_screenshot(os.path.join(EVIDENCE_DIR, slug + ".png"))

    report = getattr(node, "report_call", None)
    if report is not None and report.failed:
        path = os.path.join(EVIDENCE_DIR, slug + "-page-source.html")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(driver.page_source)
