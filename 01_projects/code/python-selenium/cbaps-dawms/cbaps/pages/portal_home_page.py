from selenium.webdriver.common.by import By
from loguru import logger

class PortalHomePage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.cbaps_link = (By.LINK_TEXT, "CBAPS")
    
    def navigate_to_portal(self, url: str):
        self.selenium.navigate_to(url)
        self.selenium.wait_for_element_visible(self.cbaps_link)
    
    def open_cbaps(self):
        from .cbaps_dashboard_page import CBAPSDashboardPage
        self.selenium.click_element(self.cbaps_link)
        logger.info("➡️ Opening CBAPS")
        return CBAPSDashboardPage(self.driver, self.selenium)
