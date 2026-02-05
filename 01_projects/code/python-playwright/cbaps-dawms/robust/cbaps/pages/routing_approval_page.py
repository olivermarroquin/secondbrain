from playwright.sync_api import Page
from loguru import logger

class RoutingApprovalPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.approver_dropdown = page.locator("#approver")
        self.submit_btn = page.locator("button:has-text('Submit for Approval')")
        self.pw.wait_for_selector("#approver")
    
    def submit_for_approval(self, approver: str):
        from .status_tracker_page import StatusTrackerPage
        logger.info(f"✍️ Submitting: {approver}")
        self.pw.select_dropdown(self.approver_dropdown, approver)
        self.pw.click_element(self.submit_btn)
        return StatusTrackerPage(self.page, self.pw)
