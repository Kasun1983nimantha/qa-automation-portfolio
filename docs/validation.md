# Validation record

Date: 2026-09-25. Target: https://www.saucedemo.com/.

## Observed local results

| Check | Observed result |
| --- | --- |
| Chrome full regression | 19 passed in 39.38 seconds |
| Firefox full regression | 19 passed in 108.92 seconds (includes first-run browser preparation) |
| Final smoke run after diagnostic fix | 3 passed, 16 deselected in 6.86 seconds |
| Ruff lint and format | Passed |
| Failure artifact probe | Assertion and fixture-setup failures both produced PNG, DOM HTML, context text, and embedded report screenshots |

Environment: macOS 26.5.1 (Apple Silicon), Python 3.14.4, Selenium 4.49.0, pytest 9.1.1, Chrome 153.0.8010.49, Firefox 156.0.1. Both browser suites ran headlessly with a new browser session per scenario. Exact dependency versions are recorded in `requirements.lock.txt`.

The temporary diagnostic probe deliberately failed one assertion and one fixture. It was removed after verification and is not part of the 19 delivered scenarios. The probe caught a missing setup-failure capture; storing the driver in pytest's per-test stash fixed it. A smoke run was then used to recheck the final fixture.

## CI evidence

[GitHub Actions run #1](https://github.com/Kasun1983nimantha/qa-automation-portfolio/actions/runs/36078999422) passed for code commit `c3b277e2879e0a2e40c845765dab1f8b660557a0` on Ubuntu with Python 3.12:

| CI job | Observed result |
| --- | --- |
| Code quality | Lint and formatting passed |
| Chrome regression | 19 passed in 26.56 seconds |
| Firefox regression | 19 passed in 100.00 seconds |
| Report uploads | Both browser artifacts uploaded successfully |

Artifacts are named `selenium-chrome-1` and `selenium-firefox-1` and expire after the workflow's 14-day retention period. The test code is unchanged in the subsequent documentation/ignore-file update; that update skips CI. Future runs are available in the [Actions run list](https://github.com/Kasun1983nimantha/qa-automation-portfolio/actions).

## Reproduce

```bash
python -m pytest --browser chrome --html=reports/chrome.html --self-contained-html --junitxml=reports/chrome.xml
python -m pytest --browser firefox --html=reports/firefox.html --self-contained-html --junitxml=reports/firefox.xml
ruff check .
ruff format --check .
```

The first local environment under a synced Documents directory stalled because package files were offloaded (`dataless` on macOS). Validation used a clean temporary environment outside that directory. If this happens locally, create the virtual environment outside a cloud-synced folder; no test assertions need to change.

These results support the listed scenarios on this date only. They are not evidence of real payments, backend validation, or unimplemented API/SQL testing.
