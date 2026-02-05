from selenium.webdriver.common.by import By
from loguru import logger

class DAWMSDashboardPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.intake_btn = (By.XPATH, "//button[contains(text(), 'Submission Intake')]")
        self.selenium.wait_for_element_visible(self.intake_btn)
        logger.info("✅ DAWMS Dashboard loaded")
    
    def go_to_submission_intake(self):
        from .submission_intake_page import SubmissionIntakePage
        self.selenium.click_element(self.intake_btn)
        logger.info("➡️ Submission Intake")
        return SubmissionIntakePage(self.driver, self.selenium)
