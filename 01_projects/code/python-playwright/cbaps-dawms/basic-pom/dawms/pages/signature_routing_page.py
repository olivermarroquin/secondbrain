"""
SignatureRoutingPage: Route submission for signature approval
Select signer and submit for signature
"""

import logging
from playwright.sync_api import Page, Locator
from dawms.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class SignatureRoutingPage:
    """
    SignatureRoutingPage handles signature routing workflow.
    This is the Python equivalent of the Java SignatureRoutingPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize SignatureRoutingPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.signer_dropdown: Locator = page.locator("#signer")
        self.route_for_signature_button: Locator = page.locator(
            "button:has-text('Submit for Signature')"
        )
        
        # Stability anchor: wait for signature routing page to load
        pwm.wait_visible("text=Signature Routing")
        logger.info("Signature Routing Page loaded successfully.")
    
    def submit_for_signature(self, signer_role_or_name: str) -> 'MilestoneStatusPage':
        """
        Submit submission for signature to selected signer
        
        Args:
            signer_role_or_name: Signer role or name
            
        Returns:
            MilestoneStatusPage instance
        """
        from dawms.pages.milestone_status_page import MilestoneStatusPage
        
        self.signer_dropdown.select_option(signer_role_or_name)
        logger.info(f"Selected signer: {signer_role_or_name}")
        
        self.pwm.click(self.route_for_signature_button)
        logger.info("Clicked 'Submit for Signature' button.")
        
        return MilestoneStatusPage(self.page, self.pwm)
