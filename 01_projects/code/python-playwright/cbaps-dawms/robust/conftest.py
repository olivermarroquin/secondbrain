import pytest
from shared.playwright_manager import PlaywrightManager

@pytest.fixture(scope="function")
def pw():
    m = PlaywrightManager()
    m.init_playwright()
    yield m
    m.close_playwright()

@pytest.fixture(scope="function")
def page(pw):
    yield pw.open_new_page()
