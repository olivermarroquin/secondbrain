"""
Pytest configuration for CBAPS tests
Defines fixtures and hooks used across all CBAPS test modules
"""

import pytest
from pathlib import Path


def pytest_configure(config):
    """Configure pytest"""
    # Create output directories
    Path("target/logs").mkdir(parents=True, exist_ok=True)
    Path("target/screenshot").mkdir(parents=True, exist_ok=True)
    Path("target/videos").mkdir(parents=True, exist_ok=True)
    Path("target/report").mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result for use in fixture teardown
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_html_report_title(report):
    """Set HTML report title"""
    report.title = "CBAPS Automation Test Report"


def pytest_html_results_table_header(cells):
    """Customize HTML report table headers"""
    cells.insert(2, '<th>Description</th>')


def pytest_html_results_table_row(report, cells):
    """Customize HTML report table rows"""
    cells.insert(2, f'<td>{getattr(report, "description", "")}</td>')


@pytest.fixture(scope="session", autouse=True)
def configure_html_report_env(request):
    """Add environment information to HTML report"""
    metadata = request.config._metadata
    metadata["Application"] = "CBAPS"
    metadata["Environment"] = "QA/Test"
    metadata["Test Framework"] = "Pytest + Playwright"
