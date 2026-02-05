from selenium.webdriver.common.by import By
from loguru import logger
from typing import List

class FundingLinesPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.add_btn = (By.XPATH, "//button[contains(text(), 'Add Line')]")
        self.amount_input = (By.ID, "fundAmount")
        self.year_input = (By.ID, "fiscalYear")
        self.save_btn = (By.XPATH, "//button[contains(text(), 'Save')]")
        self.total_label = (By.ID, "totalAmount")
        self.continue_btn = (By.XPATH, "//button[contains(text(), 'Continue to Routing')]")
        self.funding_table = (By.ID, "fundingLinesTable")
        self.selenium.wait_for_element_visible(self.add_btn)
    
    def add_funding_line(self, data):
        logger.info(f"💰 Adding: ${data.amount}")
        self.selenium.click_element(self.add_btn)
        self.selenium.enter_text(self.amount_input, data.amount)
        self.selenium.enter_text(self.year_input, data.fiscal_year)
        self.selenium.click_element(self.save_btn)
        return self
    
    def add_multiple_lines(self, lines: List):
        for line in lines:
            self.add_funding_line(line)
        return self
    
    def get_total_amount(self) -> float:
        text = self.selenium.get_text(self.total_label)
        return float(text.replace("$", "").replace(",", ""))
    
    def get_line_count(self) -> int:
        return self.selenium.get_element_count((By.XPATH, "//table[@id='fundingLinesTable']//tbody/tr"))
    
    def validate_total(self, expected: float) -> bool:
        return abs(self.get_total_amount() - expected) < 0.01
    
    def validate_count(self, expected: int) -> bool:
        return self.get_line_count() == expected
    
    def continue_to_routing(self):
        from .routing_approval_page import RoutingApprovalPage
        self.selenium.click_element(self.continue_btn)
        return RoutingApprovalPage(self.driver, self.selenium)
