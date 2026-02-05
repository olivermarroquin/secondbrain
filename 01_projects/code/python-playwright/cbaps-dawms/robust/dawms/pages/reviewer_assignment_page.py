from playwright.sync_api import Page
from loguru import logger
from typing import List

class ReviewerAssignmentPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.role_dropdown = page.locator("#reviewerRole")
        self.name_input = page.locator("#reviewerName")
        self.assign_btn = page.locator("button:has-text('Assign')")
        self.continue_btn = page.locator("button:has-text('Route to Signature')")
        self.pw.wait_for_selector("#reviewerRole")
    
    def assign_reviewer(self, data):
        logger.info(f"👤 Assigning: {data.name}")
        self.pw.select_dropdown(self.role_dropdown, data.role)
        self.pw.enter_text(self.name_input, data.name)
        self.pw.click_element(self.assign_btn)
        return self
    
    def assign_multiple_reviewers(self, reviewers: List):
        for reviewer in reviewers:
            self.assign_reviewer(reviewer)
        return self
    
    def route_to_signature(self):
        from .signature_routing_page import SignatureRoutingPage
        self.pw.click_element(self.continue_btn)
        return SignatureRoutingPage(self.page, self.pw)
