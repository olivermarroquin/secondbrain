from playwright.sync_api import Page
from loguru import logger

class PortalHomePage:
    def __init__(self, page: Page, pw):
        self.page = page
        self.pw = pw
        self.cbaps_link = page.locator("a:has-text('CBAPS')")
    
    def navigate_to_portal(self, url: str):
        self.pw.navigate_to(url)
        self.pw.wait_for_selector("a:has-text('CBAPS')")
    
    def open_cbaps(self):
        from .cbaps_dashboard_page import CBAPSDashboardPage
        self.pw.click_element(self.cbaps_link)
        logger.info("➡️ Opening CBAPS")
        return CBAPSDashboardPage(self.page, self.pw)
