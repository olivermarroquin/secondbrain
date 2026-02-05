from playwright.sync_api import Page
from loguru import logger

class SignatureRoutingPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.signer_dropdown = page.locator("#signer")
        self.submit_btn = page.locator("button:has-text('Submit for Signature')")
        self.pw.wait_for_selector("#signer")
    
    def submit_for_signature(self, signer: str):
        from .milestone_status_page import MilestoneStatusPage
        logger.info(f"✍️ Submitting: {signer}")
        self.pw.select_dropdown(self.signer_dropdown, signer)
        self.pw.click_element(self.submit_btn)
        return MilestoneStatusPage(self.page, self.pw)
