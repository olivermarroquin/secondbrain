"""
RoutingApprovalPage: Route requisition to approvers
Select approver and submit routing
"""

import logging
from playwright.sync_api import Page, Locator
from cbaps.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class RoutingApprovalPage:
    """
    RoutingApprovalPage handles approval routing workflow.
    This is the Python equivalent of the Java RoutingApprovalPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize RoutingApprovalPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.select_approver_dropdown: Locator = page.locator("#approver")
        self.submit_routing_button: Locator = page.locator(
            "button:has-text('Submit Routing')"
        )
        
        # Stability anchor: wait for routing page to load
        pwm.wait_visible("text=Routing")
        logger.info("Routing Approval Page loaded successfully.")
    
    def submit_for_approval(self, approver: str) -> 'StatusTrackerPage':
        """
        Submit requisition for approval to selected approver
        
        Args:
            approver: Approver name/role
            
        Returns:
            StatusTrackerPage instance
        """
        from cbaps.pages.status_tracker_page import StatusTrackerPage
        
        self.select_approver_dropdown.select_option(approver)
        logger.info(f"Selected approver: {approver}")
        
        self.pwm.click(self.submit_routing_button)
        logger.info("Clicked 'Submit Routing' button.")
        
        return StatusTrackerPage(self.page, self.pwm)
