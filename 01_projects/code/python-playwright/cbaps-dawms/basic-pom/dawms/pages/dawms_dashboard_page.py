"""
DAWMSDashboardPage: Main dashboard for DAWMS application
Provides navigation to key DAWMS workflows like Submission Intake
"""

import logging
from playwright.sync_api import Page, Locator
from dawms.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class DAWMSDashboardPage:
    """
    DAWMSDashboardPage represents the DAWMS main dashboard.
    This is the Python equivalent of the Java DAWMSDashboardPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize DAWMSDashboardPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.submission_intake_btn: Locator = page.locator(
            "button:has-text('Submission Intake')"
        )
        
        # Stability anchor: wait for dashboard to load
        pwm.wait_visible("text=DAWMS Dashboard")
        logger.info("DAWMS Dashboard Page loaded successfully.")
    
    def go_to_submission_intake(self) -> 'SubmissionIntakePage':
        """
        Navigate to Submission Intake page
        
        Returns:
            SubmissionIntakePage instance
        """
        from dawms.pages.submission_intake_page import SubmissionIntakePage
        
        self.pwm.click(self.submission_intake_btn)
        logger.info("Clicked 'Submission Intake' button.")
        return SubmissionIntakePage(self.page, self.pwm)
