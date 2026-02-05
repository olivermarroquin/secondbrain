from playwright.sync_api import Page
from loguru import logger

class RequisitionPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.title_input = page.locator("#requisitionTitle")
        self.fund_type_dropdown = page.locator("#fundType")
        self.submit_button = page.locator("button:has-text('Submit')")
        self.status_badge = page.locator("#reqStatus")
        self.req_id_label = page.locator("#requisitionId")
        self.funding_link = page.locator("a:has-text('Funding Lines')")
        self.pw.wait_for_selector("#requisitionTitle")
    
    def create_requisition(self, data):
        logger.info(f"📝 Creating: {data.title}")
        self.pw.enter_text(self.title_input, data.title)
        self.pw.select_dropdown(self.fund_type_dropdown, data.fund_type)
        self.pw.click_element(self.submit_button)
    
    def get_requisition_id(self) -> str:
        return self.pw.get_text(self.req_id_label) if self.pw.is_visible(self.req_id_label) else None
    
    def get_status(self) -> str:
        return self.pw.get_text(self.status_badge)
    
    def validate_status(self, expected: str) -> bool:
        return self.get_status() == expected
    
    def go_to_funding_lines(self):
        from .funding_lines_page import FundingLinesPage
        self.pw.click_element(self.funding_link)
        return FundingLinesPage(self.page, self.pw)
