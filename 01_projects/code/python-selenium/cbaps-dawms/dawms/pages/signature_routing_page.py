from selenium.webdriver.common.by import By
from loguru import logger

class SignatureRoutingPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.signer_dropdown = (By.ID, "signer")
        self.submit_btn = (By.XPATH, "//button[contains(text(), 'Submit for Signature')]")
        self.selenium.wait_for_element_visible(self.signer_dropdown)
    
    def submit_for_signature(self, signer: str):
        from .milestone_status_page import MilestoneStatusPage
        logger.info(f"✍️ Submitting: {signer}")
        self.selenium.select_dropdown(self.signer_dropdown, signer)
        self.selenium.click_element(self.submit_btn)
        return MilestoneStatusPage(self.driver, self.selenium)
