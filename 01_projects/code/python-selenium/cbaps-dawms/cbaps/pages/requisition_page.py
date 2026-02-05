from selenium.webdriver.common.by import By
from loguru import logger
from typing import Optional

class RequisitionPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.title_input = (By.ID, "requisitionTitle")
        self.fund_type_dropdown = (By.ID, "fundType")
        self.submit_button = (By.XPATH, "//button[contains(text(), 'Submit')]")
        self.status_badge = (By.ID, "reqStatus")
        self.req_id_label = (By.ID, "requisitionId")
        self.funding_link = (By.LINK_TEXT, "Funding Lines")
        self.selenium.wait_for_element_visible(self.title_input)
    
    def create_requisition(self, data):
        logger.info(f"📝 Creating: {data.title}")
        self.selenium.enter_text(self.title_input, data.title)
        self.selenium.select_dropdown(self.fund_type_dropdown, data.fund_type)
        self.selenium.click_element(self.submit_button)
    
    def get_requisition_id(self) -> Optional[str]:
        return self.selenium.get_text(self.req_id_label) if self.selenium.is_visible(self.req_id_label) else None
    
    def get_status(self) -> str:
        return self.selenium.get_text(self.status_badge)
    
    def validate_status(self, expected: str) -> bool:
        return self.get_status() == expected
    
    def go_to_funding_lines(self):
        from .funding_lines_page import FundingLinesPage
        self.selenium.click_element(self.funding_link)
        return FundingLinesPage(self.driver, self.selenium)
