from playwright.sync_api import Page
from loguru import logger
from typing import List

class FundingLinesPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.add_btn = page.locator("button:has-text('Add Line')")
        self.amount_input = page.locator("#fundAmount")
        self.year_input = page.locator("#fiscalYear")
        self.save_btn = page.locator("button:has-text('Save')")
        self.total_label = page.locator("#totalAmount")
        self.continue_btn = page.locator("button:has-text('Continue to Routing')")
        self.funding_table = page.locator("#fundingLinesTable")
        self.pw.wait_for_selector("button:has-text('Add Line')")
    
    def add_funding_line(self, data):
        logger.info(f"💰 Adding: ${data.amount}")
        self.pw.click_element(self.add_btn)
        self.pw.enter_text(self.amount_input, data.amount)
        self.pw.enter_text(self.year_input, data.fiscal_year)
        self.pw.click_element(self.save_btn)
        return self
    
    def add_multiple_lines(self, lines: List):
        for line in lines:
            self.add_funding_line(line)
        return self
    
    def get_total_amount(self) -> float:
        text = self.pw.get_text(self.total_label)
        return float(text.replace("$", "").replace(",", ""))
    
    def get_line_count(self) -> int:
        return self.pw.get_count(self.funding_table.locator("tbody tr"))
    
    def validate_total(self, expected: float) -> bool:
        return abs(self.get_total_amount() - expected) < 0.01
    
    def validate_count(self, expected: int) -> bool:
        return self.get_line_count() == expected
    
    def continue_to_routing(self):
        from .routing_approval_page import RoutingApprovalPage
        self.pw.click_element(self.continue_btn)
        return RoutingApprovalPage(self.page, self.pw)
