from selenium.webdriver.common.by import By
from loguru import logger
from typing import List

class ReviewerAssignmentPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.role_dropdown = (By.ID, "reviewerRole")
        self.name_input = (By.ID, "reviewerName")
        self.assign_btn = (By.XPATH, "//button[contains(text(), 'Assign')]")
        self.continue_btn = (By.XPATH, "//button[contains(text(), 'Route to Signature')]")
        self.selenium.wait_for_element_visible(self.role_dropdown)
    
    def assign_reviewer(self, data):
        logger.info(f"👤 Assigning: {data.name}")
        self.selenium.select_dropdown(self.role_dropdown, data.role)
        self.selenium.enter_text(self.name_input, data.name)
        self.selenium.click_element(self.assign_btn)
        return self
    
    def assign_multiple_reviewers(self, reviewers: List):
        for reviewer in reviewers:
            self.assign_reviewer(reviewer)
        return self
    
    def route_to_signature(self):
        from .signature_routing_page import SignatureRoutingPage
        self.selenium.click_element(self.continue_btn)
        return SignatureRoutingPage(self.driver, self.selenium)
