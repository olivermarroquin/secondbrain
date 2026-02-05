from playwright.sync_api import Page
from loguru import logger

class DAWMSDashboardPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.intake_btn = page.locator("button:has-text('Submission Intake')")
        self.pw.wait_for_selector("button:has-text('Submission Intake')")
        logger.info("✅ DAWMS Dashboard loaded")
    
    def go_to_submission_intake(self):
        from .submission_intake_page import SubmissionIntakePage
        self.pw.click_element(self.intake_btn)
        logger.info("➡️ Submission Intake")
        return SubmissionIntakePage(self.page, self.pw)
