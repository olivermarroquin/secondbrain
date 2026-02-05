"""
CBAPSDashboardPage: Main dashboard for CBAPS application
Provides navigation to key CBAPS workflows like Requisition creation
"""

import logging
from playwright.sync_api import Page, Locator
from cbaps.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class CBAPSDashboardPage:
    """
    CBAPSDashboardPage represents the CBAPS main dashboard.
    This is the Python equivalent of the Java CBAPSDashboardPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize CBAPSDashboardPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.create_requisition_btn: Locator = page.locator(
            "button:has-text('Create Requisition')"
        )
        
        # Stability anchor: wait for dashboard to load
        pwm.wait_visible("text=CBAPS Dashboard")
        logger.info("CBAPS Dashboard Page loaded successfully.")
    
    def go_to_create_requisition(self) -> 'RequisitionPage':
        """
        Navigate to Create Requisition page
        
        Returns:
            RequisitionPage instance
        """
        from cbaps.pages.requisition_page import RequisitionPage
        
        self.pwm.click(self.create_requisition_btn)
        logger.info("Clicked 'Create Requisition' button.")
        return RequisitionPage(self.page, self.pwm)
