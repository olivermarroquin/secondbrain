from selenium.webdriver.common.by import By
from loguru import logger

class CBAPSDashboardPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.create_req_btn = (By.XPATH, "//button[contains(text(), 'Create Requisition')]")
        self.selenium.wait_for_element_visible(self.create_req_btn)
        logger.info("✅ CBAPS Dashboard loaded")
    
    def go_to_create_requisition(self):
        from .requisition_page import RequisitionPage
        self.selenium.click_element(self.create_req_btn)
        logger.info("➡️ Create Requisition")
        return RequisitionPage(self.driver, self.selenium)
