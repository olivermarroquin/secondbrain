# CBAPS and DAWMS Automation Framework - Python + Playwright

This is the refactored automation framework for **CBAPS** and **DAWMS** applications, built using **Python + Playwright + pytest** with the Page Object Model (POM) pattern.

## 📁 Project Structure

```
cbaps/
├── __init__.py
├── library/
│   ├── __init__.py
│   ├── base.py                      # pytest base fixtures - lifecycle management
│   ├── playwright_manager.py        # Playwright wrapper - browser interactions
│   ├── report_manager.py            # HTML reporting management
│   └── excel_manager.py             # Excel data reader for data-driven tests
├── pages/
│   ├── __init__.py
│   ├── portal_home_page.py          # Portal entry point
│   ├── cbaps_dashboard_page.py      # CBAPS main dashboard
│   ├── requisition_page.py          # Requisition creation
│   ├── funding_lines_page.py        # Funding lines management
│   ├── routing_approval_page.py     # Approval routing
│   └── status_tracker_page.py       # Status validation
└── tests/
    ├── __init__.py
    ├── conftest.py                  # pytest configuration
    └── test_cbaps_end_to_end.py     # Complete CBAPS workflow tests

dawms/
├── __init__.py
├── library/
│   ├── __init__.py
│   ├── base.py                      # pytest base fixtures - lifecycle management
│   ├── playwright_manager.py        # Playwright wrapper - browser interactions
│   ├── report_manager.py            # HTML reporting management
│   └── excel_manager.py             # Excel data reader for data-driven tests
├── pages/
│   ├── __init__.py
│   ├── portal_home_page.py          # Portal entry point
│   ├── dawms_dashboard_page.py      # DAWMS main dashboard
│   ├── submission_intake_page.py    # Drug submission intake
│   ├── reviewer_assignment_page.py  # Reviewer assignment
│   ├── signature_routing_page.py    # Signature routing
│   └── milestone_status_page.py     # Milestone & status validation
└── tests/
    ├── __init__.py
    ├── conftest.py                  # pytest configuration
    └── test_dawms_end_to_end.py     # Complete DAWMS workflow tests
```

## 🎯 Key Design Principles

### 1. **Page Object Model (POM)**
- **Locators** and **page-specific actions** are defined inside **Page Object classes**
- Each application screen has a single source of truth for its UI elements and behaviors
- Page Objects return the next Page Object to enforce workflow sequencing

### 2. **pytest Fixture-Based Architecture**
- **Base** provides **fixtures** for lifecycle management (session, class, function scope)
- **PlaywrightManager** manages **browser interactions** (Playwright wrapper)
- **Page Objects** encapsulate **UI structure** and **business behavior**

### 3. **Test Readability**
- Tests read like real business workflows, not UI scripts
- Example: `Portal → Dashboard → Requisition → Funding → Routing → Status`
- Each step returns the next page object naturally

### 4. **Separation of Concerns**
- **Tests** use pytest fixtures for setup/teardown
- **PlaywrightManager** manages Playwright/Browser/Context/Page lifecycle
- **Page Objects** use PlaywrightManager helpers + Page instance

## 🚀 Quick Start

### Installation

1. **Install Python 3.8+**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers:**
```bash
playwright install
```

### Running Tests

#### Run CBAPS Tests
```bash
# Run all CBAPS tests
pytest cbaps/tests/

# Run specific test
pytest cbaps/tests/test_cbaps_end_to_end.py::TestCBAPSEndToEnd::test_cbaps_create_req_add_funding_route_verify_status

# Run with HTML report
pytest cbaps/tests/ --html=target/report/cbaps-report.html --self-contained-html

# Run with markers
pytest -m cbaps

# Run in parallel (requires pytest-xdist)
pytest cbaps/tests/ -n 4
```

#### Run DAWMS Tests
```bash
# Run all DAWMS tests
pytest dawms/tests/

# Run specific test
pytest dawms/tests/test_dawms_end_to_end.py::TestDAWMSEndToEnd::test_dawms_intake_assign_route_signature_verify_milestone

# Run with HTML report
pytest dawms/tests/ --html=target/report/dawms-report.html --self-contained-html

# Run with markers
pytest -m dawms
```

#### Run All Tests
```bash
# Run all tests from both CBAPS and DAWMS
pytest

# With HTML report
pytest --html=target/report/full-report.html --self-contained-html

# Verbose mode
pytest -v

# Show print statements
pytest -s
```

## 🧪 CBAPS Workflow

**Business Flow:** Requisition Creation → Funding Lines → Approval Routing → Status Tracking

```python
# Portal → CBAPS Dashboard
portal = PortalHomePage(page, pwm)
portal.navigate_to_portal("https://cbaps-portal.example.com")
dashboard = portal.open_cbaps()

# Dashboard → Requisition
req_page = dashboard.go_to_create_requisition()
req_page.create_requisition("FY26 Cloud Tools", "Operations")

# Requisition → Funding Lines
funding_page = req_page.go_to_funding_lines()
funding_page.add_funding_line("5000")

# Funding → Routing
routing_page = funding_page.continue_to_routing()

# Routing → Status
status_page = routing_page.submit_for_approval("Branch Chief")

# Validation
assert status_page.get_status() == "Submitted"
```

## 🧬 DAWMS Workflow

**Business Flow:** Submission Intake → Reviewer Assignment → Signature Routing → Milestone Tracking

```python
# Portal → DAWMS Dashboard
portal = PortalHomePage(page, pwm)
portal.navigate_to_portal("https://dawms-portal.example.com")
dashboard = portal.open_dawms()

# Dashboard → Submission Intake
intake = dashboard.go_to_submission_intake()

# Intake → Reviewer Assignment
assignment = intake.create_submission("NDA", "123456")

# Assignment → Signature Routing
signature = assignment \
    .assign_reviewer("Clinical Reviewer", "Jane Doe") \
    .route_to_signature_step()

# Signature → Milestone/Status
status = signature.submit_for_signature("Division Director")

# Validation
assert status.get_status() == "Pending Signature"
assert status.get_milestone() == "Signature Routing"
```

## 🔧 Key Components

### PlaywrightManager
```python
# Wrapper around Playwright primitives
pwm = PlaywrightManager()
pwm.init_playwright()

# Common actions
pwm.click(locator)
pwm.type(locator, "text")
pwm.wait_visible("selector")
pwm.select_dropdown(locator, "value")
pwm.file_upload(locator, "path/to/file")

# Screenshots
pwm.capture_screenshot_full_page("test_name")
base64_img = pwm.capture_screenshot_base64()
```

### Page Objects
```python
class RequisitionPage:
    def __init__(self, page: Page, pwm: PlaywrightManager):
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.title_input = page.locator("#requisitionTitle")
        
        # Stability anchor
        pwm.wait_visible("#requisitionTitle")
    
    def create_requisition(self, title: str, fund_type: str):
        """Business action"""
        self.pwm.type(self.title_input, title)
        # ... more actions
    
    def go_to_funding_lines(self) -> FundingLinesPage:
        """Return next page object"""
        self.pwm.click(self.go_to_funding_link)
        return FundingLinesPage(self.page, self.pwm)
```

### pytest Fixtures
```python
@pytest.fixture(scope="class")
def playwright_manager():
    """Class-level fixture for Playwright"""
    pwm = PlaywrightManager()
    pwm.init_playwright()
    yield pwm
    pwm.close_playwright()

@pytest.fixture(scope="function")
def page(playwright_manager):
    """Function-level fixture for Page (test isolation)"""
    test_page = playwright_manager.open_new_browser_page()
    yield test_page
    playwright_manager.close_page()
```

### Tests
```python
class TestCBAPSEndToEnd(Base):
    def test_workflow(self, page, playwright_manager):
        """Test reads like business workflow"""
        portal = PortalHomePage(page, playwright_manager)
        dashboard = portal.open_cbaps()
        req_page = dashboard.go_to_create_requisition()
        # ... continue workflow
        
        assert status_page.get_status() == "Submitted"
```

## 📊 Reporting

### pytest-html Reports
```bash
# Generate HTML report
pytest --html=target/report/report.html --self-contained-html

# View report
open target/report/report.html  # macOS
xdg-open target/report/report.html  # Linux
start target/report/report.html  # Windows
```

### Logging
- Logger: Python `logging` module
- Console and file logging
- Log location: `target/logs/automation.log`

## 📹 Artifacts

- **Screenshots**: `target/screenshot/`
- **Videos**: `target/videos/`
- **Reports**: `target/report/`
- **Logs**: `target/logs/`

## 🧩 Common Patterns

### Method Chaining
```python
funding_page.add_funding_line("5000") \
            .add_funding_line("3000") \
            .add_funding_line("2000")
```

### Workflow Navigation
```python
# Each method returns next page object
req_page = dashboard.go_to_create_requisition()
funding_page = req_page.go_to_funding_lines()
routing_page = funding_page.continue_to_routing()
status_page = routing_page.submit_for_approval("Approver")
```

### Step Logging
```python
Base.add_step_to_report("Step 1: Navigated to portal.")
Base.add_step_to_report("Step 2: Created requisition.")
# Shows up in logs
```

## ⚙️ Configuration

### Browser Settings (in PlaywrightManager)
```python
# In playwright_manager.py
self.browser_type = "chromium"  # Options: "chromium", "firefox", "webkit"
self.headless = False  # Set to True for CI/CD
self.maximize = True
self.record_video = True
self.demo_mode = False  # Enable for element highlighting
```

### pytest Configuration
```python
# In conftest.py or pytest.ini

[pytest]
markers =
    cbaps: CBAPS application tests
    dawms: DAWMS application tests
    end_to_end: End-to-end workflow tests
    smoke: Smoke tests

# Run specific markers
pytest -m "cbaps and end_to_end"
```

## 🎓 Best Practices

1. **Always create stability anchors** in Page Object constructors
   ```python
   pwm.wait_visible("text=Page Title")
   ```

2. **Return next Page Object** to enforce workflow
   ```python
   def go_to_funding_lines(self) -> FundingLinesPage:
       self.pwm.click(self.go_to_funding_link)
       return FundingLinesPage(self.page, self.pwm)
   ```

3. **Use business-level method names**
   - ✅ `create_requisition(title, fund_type)`
   - ❌ `fill_title_field()`, `click_submit_button()`

4. **Log every step** for traceability
   ```python
   self.add_step_to_report("Step 5: Added funding line.")
   ```

5. **Validate workflow outcomes**, not just UI elements
   ```python
   assert status_page.get_status() == "Submitted"
   ```

## 🔄 Differences from Java Version

### Language & Framework
- **Java/TestNG** → **Python/pytest**
- **@Test annotations** → **test_ functions**
- **@BeforeClass/@AfterClass** → **fixtures with scope**

### Naming Conventions
- **camelCase** → **snake_case**
- **HomePage.java** → **home_page.py**
- **TestClass** → **TestClass** (class names remain PascalCase)

### Key Equivalents
- **TestNG** → **pytest**
- **ExtentReports** → **pytest-html**
- **SLF4J Logger** → **Python logging**
- **Apache POI** → **openpyxl**
- **Datafaker** → **Faker**

## 📦 Project Setup

### Directory Structure
```bash
playwright-python-cbaps-dawms/
├── cbaps/                  # CBAPS automation
├── dawms/                  # DAWMS automation
├── requirements.txt        # Python dependencies
├── pytest.ini             # pytest configuration (optional)
├── README.md              # This file
└── target/                # Output artifacts (created at runtime)
    ├── logs/
    ├── screenshot/
    ├── videos/
    └── report/
```

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## 🚀 CI/CD Integration

### GitHub Actions Example
```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps
      - name: Run tests
        run: pytest --html=target/report/report.html --self-contained-html
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: target/
```

## 🐛 Debugging

### Run with debugging
```bash
# Pytest debugging
pytest --pdb  # Drop into debugger on failure

# Show print statements
pytest -s

# Verbose output
pytest -vv

# Run specific test with debugging
pytest cbaps/tests/test_cbaps_end_to_end.py::TestCBAPSEndToEnd::test_cbaps_create_req_add_funding_route_verify_status -s -vv
```

### Playwright Inspector
```bash
# Set environment variable
export PWDEBUG=1  # Linux/macOS
set PWDEBUG=1     # Windows

# Then run tests
pytest cbaps/tests/
```

## 📝 Notes

- The framework preserves the original Java architecture patterns in Python
- PlaywrightManager and Base are adapted for Python/pytest conventions
- All utilities (screenshot, video, reporting, Excel) remain functional
- Tests can be extended for parallel execution using pytest-xdist

## 📚 Additional Resources

- [Playwright Python Docs](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-html Plugin](https://pytest-html.readthedocs.io/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)

---

**Created**: February 2026  
**Framework**: Python + Playwright + pytest  
**Pattern**: Page Object Model (POM)  
**Applications**: CBAPS, DAWMS
