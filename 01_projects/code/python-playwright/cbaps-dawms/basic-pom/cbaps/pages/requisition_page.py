"""
RequisitionPage: Create and manage requisitions in CBAPS
Handles requisition title, fund type, and navigation to funding lines
"""

import logging
from playwright.sync_api import Page, Locator
from cbaps.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class RequisitionPage:
    """
    RequisitionPage handles requisition creation workflow.
    This is the Python equivalent of the Java RequisitionPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize RequisitionPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.title_input: Locator = page.locator("#requisitionTitle")
        self.fund_type_dropdown: Locator = page.locator("#fundType")
        self.submit_button: Locator = page.locator("button:has-text('Submit')")
        self.status_badge: Locator = page.locator("#reqStatus")
        self.go_to_funding_link: Locator = page.locator("a:has-text('Funding Lines')")
        self.route_for_approval_button: Locator = page.locator(
            "button:has-text('Route for Approval')"
        )
        
        # Stability anchor: wait for page to be ready
        pwm.wait_visible("#requisitionTitle")
        logger.info("Requisition Page loaded successfully.")
    
    def create_requisition(self, title: str, fund_type: str):
        """
        Create a new requisition with title and fund type
        
        Args:
            title: Requisition title
            fund_type: Fund type selection
        """
        self.pwm.type(self.title_input, title)
        logger.info(f"Entered requisition title: {title}")
        
        self.fund_type_dropdown.select_option(fund_type)
        logger.info(f"Selected fund type: {fund_type}")
        
        self.pwm.click(self.submit_button)
        logger.info("Clicked Submit button.")
    
    def get_status(self) -> str:
        """
        Get current requisition status
        
        Returns:
            Status text
        """
        status = self.status_badge.text_content()
        logger.info(f"Retrieved status: {status}")
        return status
    
    def go_to_funding_lines(self) -> 'FundingLinesPage':
        """
        Navigate to Funding Lines page
        
        Returns:
            FundingLinesPage instance
        """
        from cbaps.pages.funding_lines_page import FundingLinesPage
        
        self.pwm.click(self.go_to_funding_link)
        logger.info("Navigated to Funding Lines page.")
        return FundingLinesPage(self.page, self.pwm)
    
    def route_for_approval(self) -> 'RoutingApprovalPage':
        """
        Route requisition for approval
        
        Returns:
            RoutingApprovalPage instance
        """
        from cbaps.pages.routing_approval_page import RoutingApprovalPage
        
        self.pwm.click(self.route_for_approval_button)
        logger.info("Clicked 'Route for Approval' button.")
        return RoutingApprovalPage(self.page, self.pwm)
