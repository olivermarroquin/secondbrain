```bash
# Playwright Python Test Automation Framework For ZaiNar: Automating 'https://the-internet.herokuapp.com/'
# This framework follows QA Page Object Model patterns with centralized configuration, logging, and reusable utilities. URLs live in one place instead of being hardcoded across files, every action is logged so you can trace exactly what happened during test execution, and common operations use helper functions with built-in retry logic for better stability. Tests automatically capture screenshots on failure, and all page objects inherit the same enhanced error handling from the base page class. I built it like this to ensure that it is easy to maintain and debug.

### Prerequisites
- Python 3.8+
- pip package manager
- macOS / Linux (Windows supported with minor command changes)

### Required Dependencies (requirements.txt)
pytest==7.4.3
playwright==1.57.0
pytest-playwright==0.7.2
pytest-html==4.1.1
```
#### DOT THIS FIRST BEFORE RUNNING TESTS ####

### Clean Setup (Recommended if anything behaves unexpectedly)
# Ensure no active virtual environment
deactivate 2>/dev/null || true

# Remove old artifacts
rm -rf venv
rm -rf .pytest_cache
rm -rf __pycache__
rm -rf ~/Library/Caches/ms-playwright

### Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate

### Install Dependencies
python -m pip install -U pip
python -m pip install -r requirements.txt

### Install Playwright Browser
python -m playwright install chromium

# Ensure shell uses venv binaries
hash -r
rehash 2>/dev/null || true
which -a pytest
which python
which pytest

# IMPORTANT NOTE:
### Troubleshooting (Quick)
- If `pytest` runs the wrong Python/pytest, use the venv interpreter: `python -m pytest` (or re-activate venv and verify `which python` + `which pytest` point to `venv/bin`).
- If Playwright says Chromium is missing or launches then crashes, clear the browser cache and reinstall: `rm -rf ~/Library/Caches/ms-playwright && python -m playwright install chromium`.
``` bash

####RUNING TESTS:
#### Step 3: Run Tests
pytest

### Verify Installation
python -m pytest tests/test_challenging_dom_page --headed

#### Run all tests with visible browser
python -m pytest --headed

#### Run all tests (headless mode)
python -m pytest

### By Category

```bash
# Smoke tests (critical path - 3 tests)
pytest -m smoke

# Regression tests (comprehensive - 5 tests)
pytest -m regression

# Specific page tests
pytest -m challenging_dom
pytest -m dynamic_loading
pytest -m shifting_content


### Generate HTML Report
# Generate report
pytest --html=reports/report.html --self-contained-html

# Open report (Mac)
open reports/report.html

# Open report (Windows)
start reports/report.html


### View Logs
After running tests, check the execution logs:
# View latest log
cat reports/test_run_*.log


#### Open HTML report
# Mac
open reports/report.html
# Windows
start reports/report.html
# Linux
xdg-open reports/report.html


### Environment Configuration

Edit `config/environments.yaml`:

Switch environments:
export TEST_ENV=staging
pytest


### Utilities

**Logger** (`utils/logger.py`)
- Structured logging to files and console
- Automatic timestamping
- Test step logging

**SafeActions** (`utils/helpers.py`)
- Retry logic for clicks
- Safe text extraction
- Robust element interactions

**TableHelper** (`utils/helpers.py`)
- Extract table data as dictionaries
- Header-based data mapping

**Assertions** (`utils/assertions.py`)
- SoftAssert for multiple checks
- PageAssertions for Playwright expects

**Decorators** (`utils/decorators.py`)
- @log_test_execution
- @retry_on_failure