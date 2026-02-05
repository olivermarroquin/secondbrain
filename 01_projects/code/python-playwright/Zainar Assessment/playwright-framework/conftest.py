import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from typing import Generator
import os
from datetime import datetime
from pathlib import Path

pytest_plugins = [
    "fixtures.page_fixtures",
]

def pytest_configure(config):
    Path("reports").mkdir(parents=True, exist_ok=True)
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    Path("reports/logs").mkdir(parents=True, exist_ok=True)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    from config.config import config
    return {
        **browser_context_args,
        "viewport": {
            "width": config.VIEWPORT_WIDTH,
            "height": config.VIEWPORT_HEIGHT,
        },
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="function")
def page(page: Page) -> Generator[Page, None, None]:
    yield page

@pytest.fixture(scope="function", autouse=True)
def capture_screenshot_on_failure(request, page: Page):
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = f"{screenshot_dir}/{request.node.name}_{timestamp}.png"
        try:
            page.screenshot(path=screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"\nFailed to capture screenshot: {e}")

@pytest.fixture(scope="function")
def context(context: BrowserContext) -> Generator[BrowserContext, None, None]:
    yield context

@pytest.fixture(scope="function")
def browser(browser: Browser) -> Generator[Browser, None, None]:
    yield browser

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
