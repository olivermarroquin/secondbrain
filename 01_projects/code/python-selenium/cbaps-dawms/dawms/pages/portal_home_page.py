from selenium.webdriver.common.by import By
from loguru import logger

class PortalHomePage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.dawms_link = (By.LINK_TEXT, "DAWMS")
    
    def navigate_to_portal(self, url: str):
        self.selenium.navigate_to(url)
        self.selenium.wait_for_element_visible(self.dawms_link)
    
    def open_dawms(self):
        from .dawms_dashboard_page import DAWMSDashboardPage
        self.selenium.click_element(self.dawms_link)
        logger.info("➡️ Opening DAWMS")
        return DAWMSDashboardPage(self.driver, self.selenium)
