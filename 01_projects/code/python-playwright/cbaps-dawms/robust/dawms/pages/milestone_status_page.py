from playwright.sync_api import Page
from loguru import logger

class MilestoneStatusPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.milestone_label = page.locator("#milestone")
        self.status_badge = page.locator("#status")
        self.pw.wait_for_selector("#status")
    
    def get_milestone(self) -> str:
        return self.pw.get_text(self.milestone_label)
    
    def get_status(self) -> str:
        return self.pw.get_text(self.status_badge)
    
    def validate_status(self, expected: str) -> bool:
        actual = self.get_status()
        valid = actual == expected
        if valid:
            logger.info(f"✅ Status: {expected}")
        return valid
    
    def validate_milestone(self, expected: str) -> bool:
        actual = self.get_milestone()
        return actual == expected
