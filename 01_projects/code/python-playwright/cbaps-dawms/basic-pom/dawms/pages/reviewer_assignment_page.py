"""
ReviewerAssignmentPage: Assign reviewers to drug submissions
Handles reviewer role selection, reviewer assignment, and routing to signature
"""

import logging
from playwright.sync_api import Page, Locator
from dawms.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class ReviewerAssignmentPage:
    """
    ReviewerAssignmentPage handles reviewer assignment workflow.
    This is the Python equivalent of the Java ReviewerAssignmentPage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize ReviewerAssignmentPage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.reviewer_role_dropdown: Locator = page.locator("#reviewerRole")
        self.reviewer_name_input: Locator = page.locator("#reviewerName")
        self.assign_reviewer_button: Locator = page.locator("button:has-text('Assign')")
        self.continue_to_signature_button: Locator = page.locator(
            "button:has-text('Route to Signature')"
        )
        
        # Stability anchor: wait for page to load
        pwm.wait_visible("text=Reviewer Assignment")
        logger.info("Reviewer Assignment Page loaded successfully.")
    
    def assign_reviewer(
        self, role: str, reviewer_name: str
    ) -> 'ReviewerAssignmentPage':
        """
        Assign a reviewer with specified role and name
        
        Args:
            role: Reviewer role (Clinical Reviewer, Pharmacologist, etc.)
            reviewer_name: Name of reviewer
            
        Returns:
            self for method chaining
        """
        self.reviewer_role_dropdown.select_option(role)
        logger.info(f"Selected reviewer role: {role}")
        
        self.pwm.type(self.reviewer_name_input, reviewer_name)
        logger.info(f"Entered reviewer name: {reviewer_name}")
        
        self.pwm.click(self.assign_reviewer_button)
        logger.info("Clicked 'Assign' button.")
        
        return self
    
    def route_to_signature_step(self) -> 'SignatureRoutingPage':
        """
        Continue to Signature Routing step
        
        Returns:
            SignatureRoutingPage instance
        """
        from dawms.pages.signature_routing_page import SignatureRoutingPage
        
        self.pwm.click(self.continue_to_signature_button)
        logger.info("Clicked 'Route to Signature' button.")
        return SignatureRoutingPage(self.page, self.pwm)
