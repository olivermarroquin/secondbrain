from selenium.webdriver.common.by import By
from loguru import logger

class MilestoneStatusPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.milestone_label = (By.ID, "milestone")
        self.status_badge = (By.ID, "status")
        self.selenium.wait_for_element_visible(self.status_badge)
    
    def get_milestone(self) -> str:
        return self.selenium.get_text(self.milestone_label)
    
    def get_status(self) -> str:
        return self.selenium.get_text(self.status_badge)
    
    def validate_status(self, expected: str) -> bool:
        return self.get_status() == expected
    
    def validate_milestone(self, expected: str) -> bool:
        return self.get_milestone() == expected
