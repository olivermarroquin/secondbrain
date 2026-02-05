"""
MilestoneStatusPage: Final milestone and status validation page
Displays current submission milestone and status
"""

import logging
from playwright.sync_api import Page, Locator
from dawms.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class MilestoneStatusPage:
    """
    MilestoneStatusPage displays final milestone and status.
    This is the Python equivalent of the Java MilestoneStatusPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize MilestoneStatusPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.milestone_label: Locator = page.locator("#milestone")
        self.status_label: Locator = page.locator("#status")
        
        # Stability anchor: wait for status to be visible
        pwm.wait_visible("#status")
        logger.info("Milestone Status Page loaded successfully.")
    
    def get_milestone(self) -> str:
        """
        Get current submission milestone
        
        Returns:
            Milestone text
        """
        milestone = self.milestone_label.text_content()
        logger.info(f"Retrieved milestone: {milestone}")
        return milestone
    
    def get_status(self) -> str:
        """
        Get current submission status
        
        Returns:
            Status text
        """
        status = self.status_label.text_content()
        logger.info(f"Retrieved status: {status}")
        return status
