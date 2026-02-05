from selenium.webdriver.common.by import By
from loguru import logger

class RoutingApprovalPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.approver_dropdown = (By.ID, "approver")
        self.submit_btn = (By.XPATH, "//button[contains(text(), 'Submit for Approval')]")
        self.selenium.wait_for_element_visible(self.approver_dropdown)
    
    def submit_for_approval(self, approver: str):
        from .status_tracker_page import StatusTrackerPage
        logger.info(f"✍️ Submitting: {approver}")
        self.selenium.select_dropdown(self.approver_dropdown, approver)
        self.selenium.click_element(self.submit_btn)
        return StatusTrackerPage(self.driver, self.selenium)
