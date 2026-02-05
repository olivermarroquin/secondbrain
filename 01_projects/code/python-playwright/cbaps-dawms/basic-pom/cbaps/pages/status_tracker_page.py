"""
StatusTrackerPage: Final status validation page
Displays current requisition status after routing
"""

import logging
from playwright.sync_api import Page, Locator
from cbaps.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class StatusTrackerPage:
    """
    StatusTrackerPage displays final requisition status.
    This is the Python equivalent of the Java StatusTrackerPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize StatusTrackerPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.status_badge: Locator = page.locator("#reqStatus")
        
        # Stability anchor: wait for status to be visible
        pwm.wait_visible("#reqStatus")
        logger.info("Status Tracker Page loaded successfully.")
    
    def get_status(self) -> str:
        """
        Get current requisition status
        
        Returns:
            Status text
        """
        status = self.status_badge.text_content()
        logger.info(f"Retrieved status: {status}")
        return status
