from playwright.sync_api import Page
from loguru import logger

class SubmissionIntakePage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.type_dropdown = page.locator("#submissionType")
        self.app_number_input = page.locator("#applicationNumber")
        self.create_btn = page.locator("button:has-text('Create Submission')")
        self.pw.wait_for_selector("#submissionType")
    
    def create_submission(self, data):
        logger.info(f"📝 Creating submission: {data.application_number}")
        self.pw.select_dropdown(self.type_dropdown, data.submission_type)
        self.pw.enter_text(self.app_number_input, data.application_number)
        self.pw.click_element(self.create_btn)
        from .reviewer_assignment_page import ReviewerAssignmentPage
        return ReviewerAssignmentPage(self.page, self.pw)
