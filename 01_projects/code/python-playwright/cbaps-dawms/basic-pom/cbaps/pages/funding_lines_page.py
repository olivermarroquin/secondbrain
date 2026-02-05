"""
FundingLinesPage: Add and manage funding lines for a requisition
Allows adding multiple funding lines and continuing to routing
"""

import logging
from playwright.sync_api import Page, Locator
from cbaps.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class FundingLinesPage:
    """
    FundingLinesPage handles funding line management.
    This is the Python equivalent of the Java FundingLinesPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize FundingLinesPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.add_line_button: Locator = page.locator("button:has-text('Add Line')")
        self.amount_input: Locator = page.locator("#fundAmount")
        self.save_line_button: Locator = page.locator("button:has-text('Save')")
        self.continue_to_routing_button: Locator = page.locator(
            "button:has-text('Continue to Routing')"
        )
        
        # Stability anchor: wait for page to load
        pwm.wait_visible("text=Funding Lines")
        logger.info("Funding Lines Page loaded successfully.")
    
    def add_funding_line(self, amount: str) -> 'FundingLinesPage':
        """
        Add a funding line with specified amount
        
        Args:
            amount: Funding amount
            
        Returns:
            self for method chaining
        """
        self.pwm.click(self.add_line_button)
        logger.info("Clicked 'Add Line' button.")
        
        self.pwm.type(self.amount_input, amount)
        logger.info(f"Entered funding amount: {amount}")
        
        self.pwm.click(self.save_line_button)
        logger.info("Clicked 'Save' button for funding line.")
        
        return self
    
    def continue_to_routing(self) -> 'RoutingApprovalPage':
        """
        Continue to Routing/Approval step
        
        Returns:
            RoutingApprovalPage instance
        """
        from cbaps.pages.routing_approval_page import RoutingApprovalPage
        
        self.pwm.click(self.continue_to_routing_button)
        logger.info("Clicked 'Continue to Routing' button.")
        return RoutingApprovalPage(self.page, self.pwm)
