"""
Base: pytest base module for DAWMS automation
Manages lifecycle: initialization, setup, teardown, reporting
Tests import and use fixtures from this module
"""

import logging
import pytest
from pathlib import Path
from playwright.sync_api import Page
from dawms.library.playwright_manager import PlaywrightManager
from dawms.library.report_manager import ReportManager

logger = logging.getLogger(__name__)


class Base:
    """
    Base class provides common setup/teardown and utilities for tests.
    This is the Python equivalent of the Java Base class using pytest fixtures.
    """
    
    @pytest.fixture(scope="session")
    def report_manager(self):
        """Session-level fixture for report management"""
        rm = ReportManager()
        rm.setup_report()
        yield rm
        rm.finalize_report()
    
    @pytest.fixture(scope="class")
    def playwright_manager(self):
        """Class-level fixture for Playwright initialization"""
        logger.info("Initializing Playwright object before test class.")
        pwm = PlaywrightManager()
        pwm.init_playwright()
        yield pwm
        pwm.close_playwright()
        logger.info("Closing Playwright object after test class.")
    
    @pytest.fixture(scope="function")
    def page(self, playwright_manager: PlaywrightManager, request) -> Page:
        """
        Method-level fixture - create new Page for each test method (isolation)
        """
        test_page = playwright_manager.open_new_browser_page()
        logger.info(f"Starting test: {request.node.name}")
        
        yield test_page
        
        # Teardown
        try:
            # Capture screenshot on failure
            if request.node.rep_call.failed:
                logger.info(f"Test failed: {request.node.name}")
                screenshot_path = playwright_manager.capture_screenshot_full_page(
                    request.node.name
                )
                logger.info(f"Screenshot captured: {screenshot_path}")
            
            # Get video path if available
            try:
                video_path = test_page.video.path() if test_page.video else None
                if video_path:
                    logger.info(f"Video recorded: {video_path}")
            except Exception as e:
                logger.warning(f"Video not available: {e}")
            
            playwright_manager.close_page()
            
        except Exception as e:
            logger.error(f"Exception during teardown: {e}")
            if test_page:
                playwright_manager.close_page()
    
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        """
        Hook to capture test result for use in teardown
        """
        outcome = yield
        rep = outcome.get_result()
        setattr(item, f"rep_{rep.when}", rep)
    
    @staticmethod
    def add_step_to_report(step_message: str):
        """
        Helper method to log test steps
        """
        logger.info(step_message)


# Logging configuration
def setup_logging():
    """Configure logging for DAWMS automation"""
    Path("target/logs").mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('target/logs/automation.log'),
            logging.StreamHandler()
        ]
    )


# Initialize logging
setup_logging()
