"""
SubmissionIntakePage: Create and manage drug submissions in DAWMS
Handles submission type, application number, and navigation to reviewer assignment
"""

import logging
from playwright.sync_api import Page, Locator
from dawms.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class SubmissionIntakePage:
    """
    SubmissionIntakePage handles drug submission intake.
    This is the Python equivalent of the Java SubmissionIntakePage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize SubmissionIntakePage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.submission_type_dropdown: Locator = page.locator("#submissionType")
        self.application_number_input: Locator = page.locator("#applicationNumber")
        self.create_submission_button: Locator = page.locator(
            "button:has-text('Create Submission')"
        )
        
        # Stability anchor: wait for page to be ready
        pwm.wait_visible("#submissionType")
        logger.info("Submission Intake Page loaded successfully.")
    
    def create_submission(
        self, submission_type: str, app_number: str
    ) -> 'ReviewerAssignmentPage':
        """
        Create a new submission with type and application number
        
        Args:
            submission_type: Type of submission (NDA, ANDA, BLA, etc.)
            app_number: Application number
            
        Returns:
            ReviewerAssignmentPage instance
        """
        from dawms.pages.reviewer_assignment_page import ReviewerAssignmentPage
        
        self.submission_type_dropdown.select_option(submission_type)
        logger.info(f"Selected submission type: {submission_type}")
        
        self.pwm.type(self.application_number_input, app_number)
        logger.info(f"Entered application number: {app_number}")
        
        self.pwm.click(self.create_submission_button)
        logger.info("Clicked 'Create Submission' button.")
        
        return ReviewerAssignmentPage(self.page, self.pwm)
