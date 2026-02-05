from playwright.sync_api import Page
from loguru import logger

class PortalHomePage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.dawms_link = page.locator("a:has-text('DAWMS')")
    
    def navigate_to_portal(self, url: str):
        self.pw.navigate_to(url)
        self.pw.wait_for_selector("a:has-text('DAWMS')")
    
    def open_dawms(self):
        from .dawms_dashboard_page import DAWMSDashboardPage
        self.pw.click_element(self.dawms_link)
        logger.info("➡️ Opening DAWMS")
        return DAWMSDashboardPage(self.page, self.pw)
