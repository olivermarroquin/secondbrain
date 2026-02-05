from selenium.webdriver.common.by import By
from loguru import logger

class StatusTrackerPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.status_badge = (By.ID, "reqStatus")
        self.selenium.wait_for_element_visible(self.status_badge)
    
    def get_status(self) -> str:
        return self.selenium.get_text(self.status_badge)
    
    def validate_status(self, expected: str) -> bool:
        actual = self.get_status()
        valid = actual == expected
        if valid:
            logger.info(f"✅ Status: {expected}")
        return valid
