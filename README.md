# Selenium QA Automation Portfolio

[![Selenium UI tests](https://github.com/Kasun1983nimantha/qa-automation-portfolio/actions/workflows/ui-tests.yml/badge.svg)](https://github.com/Kasun1983nimantha/qa-automation-portfolio/actions/workflows/ui-tests.yml)

A Python + pytest portfolio that tests the shopping journey in [Sauce Demo](https://www.saucedemo.com/): authentication, product sorting, cart changes, and checkout. It demonstrates test design, reusable Selenium page objects, isolated browser fixtures, and CI failure investigation.

**19 automated scenarios · 3 smoke scenarios · Chrome + Firefox CI matrix**

This is a learning/portfolio project against a public demo application. It is not commercial work experience, and Sauce Labs does not endorse this repository. Only public demo credentials and fictional customer details are used.

## Start here

- **Review the tests:** [`ui-tests/tests/`](ui-tests/tests/)
- **Understand coverage and tradeoffs:** [test strategy](docs/test-strategy.md)
- **Compare manual and automated cases:** [test cases](manual-testing/test-cases.md)
- **See execution evidence:** [validation record](docs/validation.md) and [GitHub Actions](https://github.com/Kasun1983nimantha/qa-automation-portfolio/actions)
- **Prepare to explain the work:** [interview walkthrough](docs/interview-walkthrough.md)

## Run locally

Requires Python 3.12 or newer, Chrome or Firefox, and internet access. Selenium Manager resolves the appropriate driver automatically; its first run may download a driver or browser.

```bash
git clone https://github.com/Kasun1983nimantha/qa-automation-portfolio.git
cd qa-automation-portfolio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m pytest --html=reports/report.html --self-contained-html
```

On Windows PowerShell, create the environment with `py -3 -m venv .venv` and activate with `.venv\Scripts\Activate.ps1`. If activation is unavailable, use `.venv\Scripts\python.exe` directly for pip and pytest commands.

```bash
# Critical journeys only (3 scenarios)
python -m pytest -m smoke

# Cross-browser regression
python -m pytest --browser firefox

# Watch the browser
python -m pytest --headed -m smoke

# One area, or one parameterized case
python -m pytest ui-tests/tests/test_checkout.py
python -m pytest -k missing-postal-code

# Code quality
ruff check .
ruff format --check .
```

`requirements.txt` pins direct dependencies; `requirements.lock.txt` also pins the resolved transitive dependencies used for validation and CI. After an intentional dependency update, regenerate the lock in a clean environment and rerun both browsers.

For a cloud-synced workspace, keep the virtual environment outside the synced directory if macOS offloads its package files. See the [validation record](docs/validation.md) for the observed environment issue.

## What is tested

| Area | Scenarios | Business risk |
| --- | ---: | --- |
| Authentication | 7 | Valid users cannot sign in; invalid users gain access; logout leaves protected access |
| Inventory sorting | 4 | Customers cannot compare products reliably |
| Cart | 3 | Wrong products/prices/quantities; removals or refresh lose state |
| Checkout | 5 | Missing details accepted; incorrect totals; cancellation loses cart; order does not complete |

Assertions check visible outcomes and exact selected products, quantities, and money values. Sorting checks against the pre-sort product list, so an empty list cannot pass. Money uses `Decimal` to avoid binary floating-point comparisons.

## Design

```text
pytest test → fixture (new browser) → page object → Selenium WebDriver → Sauce Demo
     ↓ failure
HTML report + screenshot + DOM snapshot + browser/URL context
```

- **Page Object Model:** locators and browser interactions live in page classes; business assertions live in tests.
- **Explicit waits:** wait for visible/clickable elements and resulting page state; no fixed sleeps or implicit waits.
- **Isolation:** every case gets a new browser profile and clean session; no order-dependent tests.
- **Data-driven tests:** parameterized login, sorting, and checkout cases have readable IDs.
- **Diagnostics:** setup/call failures with a live driver produce a PNG, DOM snapshot, and context file in `reports/failures/`; HTML reports embed the screenshot.
- **Honest failures:** no automatic retries, swallowed assertions, or blanket expected failures. Diagnose a failure before rerunning it.

## CI and reports

GitHub Actions runs lint/format checks followed by separate Chrome and Firefox jobs on pushes to `main`, pull requests, and manual dispatch. Each browser uploads HTML/JUnit reports and any failure evidence for 14 days, even when tests fail. The workflow uses read-only repository permissions and commit-pinned actions.

Open **Actions → Selenium UI tests → a run → Artifacts**, download a browser artifact, and open its HTML report. Generated reports are ignored by Git. Consult the validation record for what has actually run; the badge reflects the latest workflow result.

## Repository layout

```text
.github/workflows/ui-tests.yml   CI and report artifacts
conftest.py                      Browser options, fixtures, failure capture
ui-tests/
  pages/                        Login, inventory, cart, checkout page objects
  tests/                        Business assertions and parameterized scenarios
manual-testing/                 Traceable cases and a blank defect template
docs/                           Strategy, validation, interview walkthrough
requirements.txt               Direct dependency pins
requirements.lock.txt          Resolved dependency pins
pyproject.toml                  pytest and Ruff configuration
api-tests/, postman/, sql-tests/ Planned portfolio extensions (not implemented)
```

## Limitations and next steps

The demo is a third-party service: availability, UI, and catalog changes may break tests. The six-item catalog and expected prices are explicit fixtures, not live retail requirements. Checkout simulates an order; it does not process payments. API, database, accessibility, visual regression, performance, and mobile-device testing are outside this suite's current scope.

Next learning tasks: add product-detail coverage, keyboard-only exploratory testing, and an API project backed by a documented test service. Do not claim those as implemented until code and execution evidence exist.

## References

- [Selenium waiting strategies](https://www.selenium.dev/documentation/webdriver/waits/)
- [Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
