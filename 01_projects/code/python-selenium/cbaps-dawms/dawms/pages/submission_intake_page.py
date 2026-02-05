from selenium.webdriver.common.by import By
from loguru import logger

class SubmissionIntakePage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.type_dropdown = (By.ID, "submissionType")
        self.app_number_input = (By.ID, "applicationNumber")
        self.create_btn = (By.XPATH, "//button[contains(text(), 'Create Submission')]")
        self.selenium.wait_for_element_visible(self.type_dropdown)
    
    def create_submission(self, data):
        logger.info(f"📝 Creating submission: {data.application_number}")
        self.selenium.select_dropdown(self.type_dropdown, data.submission_type)
        self.selenium.enter_text(self.app_number_input, data.application_number)
        self.selenium.click_element(self.create_btn)
        from .reviewer_assignment_page import ReviewerAssignmentPage
        return ReviewerAssignmentPage(self.driver, self.selenium)
