from playwright.sync_api import Page
from loguru import logger

class CBAPSDashboardPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.create_req_btn = page.locator("button:has-text('Create Requisition')")
        self.pw.wait_for_selector("button:has-text('Create Requisition')")
        logger.info("✅ CBAPS Dashboard loaded")
    
    def go_to_create_requisition(self):
        from .requisition_page import RequisitionPage
        self.pw.click_element(self.create_req_btn)
        logger.info("➡️ Create Requisition")
        return RequisitionPage(self.page, self.pw)
