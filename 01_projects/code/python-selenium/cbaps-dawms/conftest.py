import pytest
from shared.selenium_manager import SeleniumManager

@pytest.fixture(scope="function")
def selenium_mgr():
    m = SeleniumManager()
    m.init_selenium()
    yield m
    m.close_selenium()

@pytest.fixture(scope="function")
def driver(selenium_mgr):
    return selenium_mgr.driver
