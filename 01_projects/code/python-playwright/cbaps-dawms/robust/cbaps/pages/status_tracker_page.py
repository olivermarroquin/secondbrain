from playwright.sync_api import Page
from loguru import logger

class StatusTrackerPage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.status_badge = page.locator("#reqStatus")
        self.pw.wait_for_selector("#reqStatus")
    
    def get_status(self) -> str:
        return self.pw.get_text(self.status_badge)
    
    def validate_status(self, expected: str) -> bool:
        actual = self.get_status()
        valid = actual == expected
        if valid:
            logger.info(f"✅ Status: {expected}")
        return valid
