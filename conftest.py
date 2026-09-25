import hashlib
import re
import warnings
from pathlib import Path

import pytest
import pytest_html
from pages.login_page import LoginPage
from selenium import webdriver

_DRIVER_KEY = pytest.StashKey[webdriver.Remote]()


def pytest_addoption(parser):
    parser.addoption("--browser", choices=["chrome", "firefox"], default="chrome")
    parser.addoption("--headed", action="store_true", help="Show the test browser")
    parser.addoption("--base-url", default="https://www.saucedemo.com")
    parser.addoption("--artifacts-dir", default="reports/failures")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if not request.config.getoption("--headed"):
            options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            },
        )
        instance = webdriver.Chrome(options=options)
    else:
        options = webdriver.FirefoxOptions()
        if not request.config.getoption("--headed"):
            options.add_argument("-headless")
        instance = webdriver.Firefox(options=options)
    # Register immediately so later fixture setup failures still close the browser.
    request.addfinalizer(instance.quit)
    request.node.stash[_DRIVER_KEY] = instance
    instance.set_window_size(1440, 1000)
    instance.set_page_load_timeout(30)
    return instance


@pytest.fixture
def login_page(driver, request):
    return LoginPage(driver, request.config.getoption("--base-url")).open()


@pytest.fixture
def inventory(login_page):
    return login_page.login()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if not report.failed or report.when not in ("setup", "call"):
        return
    driver = item.stash.get(_DRIVER_KEY, None)
    if driver is None:
        return
    # A digest keeps parameterized cases distinct even after filename sanitization.
    digest = hashlib.sha256(item.nodeid.encode()).hexdigest()[:10]
    name = re.sub(r"[^A-Za-z0-9_-]", "_", item.name)[:100]
    folder = Path(item.config.getoption("--artifacts-dir")) / f"{name}-{digest}"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        screenshot = driver.get_screenshot_as_base64()
        driver.save_screenshot(str(folder / "screenshot.png"))
        (folder / "page.html").write_text(driver.page_source, encoding="utf-8")
        (folder / "context.txt").write_text(
            f"Test: {item.nodeid}\nPhase: {report.when}\nURL: {driver.current_url}\n"
            f"Browser: {driver.capabilities.get('browserName')} "
            f"{driver.capabilities.get('browserVersion')}\n",
            encoding="utf-8",
        )
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(screenshot, name="Failure screenshot"))
        report.extras = extras
    except Exception as exc:
        # Diagnostics must not replace the original assertion or Selenium error.
        warnings.warn(f"Could not capture failure artifacts: {exc}", stacklevel=2)
