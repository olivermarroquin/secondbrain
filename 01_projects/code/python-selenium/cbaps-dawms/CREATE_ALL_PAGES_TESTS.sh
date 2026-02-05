#!/bin/bash

# This script creates ALL page objects and tests for both CBAPS and DAWMS

# ========== CBAPS PAGES ==========

cat > cbaps/pages/portal_home_page.py << 'EOF'
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
EOF

cat > cbaps/pages/cbaps_dashboard_page.py << 'EOF'
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
EOF

cat > cbaps/pages/requisition_page.py << 'EOF'
from selenium.webdriver.common.by import By
from loguru import logger
from typing import Optional

class RequisitionPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.title_input = (By.ID, "requisitionTitle")
        self.fund_type_dropdown = (By.ID, "fundType")
        self.submit_button = (By.XPATH, "//button[contains(text(), 'Submit')]")
        self.status_badge = (By.ID, "reqStatus")
        self.req_id_label = (By.ID, "requisitionId")
        self.funding_link = (By.LINK_TEXT, "Funding Lines")
        self.selenium.wait_for_element_visible(self.title_input)
    
    def create_requisition(self, data):
        logger.info(f"📝 Creating: {data.title}")
        self.selenium.enter_text(self.title_input, data.title)
        self.selenium.select_dropdown(self.fund_type_dropdown, data.fund_type)
        self.selenium.click_element(self.submit_button)
    
    def get_requisition_id(self) -> Optional[str]:
        return self.selenium.get_text(self.req_id_label) if self.selenium.is_visible(self.req_id_label) else None
    
    def get_status(self) -> str:
        return self.selenium.get_text(self.status_badge)
    
    def validate_status(self, expected: str) -> bool:
        return self.get_status() == expected
    
    def go_to_funding_lines(self):
        from .funding_lines_page import FundingLinesPage
        self.selenium.click_element(self.funding_link)
        return FundingLinesPage(self.driver, self.selenium)
EOF

cat > cbaps/pages/funding_lines_page.py << 'EOF'
from selenium.webdriver.common.by import By
from loguru import logger
from typing import List

class FundingLinesPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.add_btn = (By.XPATH, "//button[contains(text(), 'Add Line')]")
        self.amount_input = (By.ID, "fundAmount")
        self.year_input = (By.ID, "fiscalYear")
        self.save_btn = (By.XPATH, "//button[contains(text(), 'Save')]")
        self.total_label = (By.ID, "totalAmount")
        self.continue_btn = (By.XPATH, "//button[contains(text(), 'Continue to Routing')]")
        self.funding_table = (By.ID, "fundingLinesTable")
        self.selenium.wait_for_element_visible(self.add_btn)
    
    def add_funding_line(self, data):
        logger.info(f"💰 Adding: ${data.amount}")
        self.selenium.click_element(self.add_btn)
        self.selenium.enter_text(self.amount_input, data.amount)
        self.selenium.enter_text(self.year_input, data.fiscal_year)
        self.selenium.click_element(self.save_btn)
        return self
    
    def add_multiple_lines(self, lines: List):
        for line in lines:
            self.add_funding_line(line)
        return self
    
    def get_total_amount(self) -> float:
        text = self.selenium.get_text(self.total_label)
        return float(text.replace("$", "").replace(",", ""))
    
    def get_line_count(self) -> int:
        return self.selenium.get_element_count((By.XPATH, "//table[@id='fundingLinesTable']//tbody/tr"))
    
    def validate_total(self, expected: float) -> bool:
        return abs(self.get_total_amount() - expected) < 0.01
    
    def validate_count(self, expected: int) -> bool:
        return self.get_line_count() == expected
    
    def continue_to_routing(self):
        from .routing_approval_page import RoutingApprovalPage
        self.selenium.click_element(self.continue_btn)
        return RoutingApprovalPage(self.driver, self.selenium)
EOF

cat > cbaps/pages/routing_approval_page.py << 'EOF'
from selenium.webdriver.common.by import By
from loguru import logger

class RoutingApprovalPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.approver_dropdown = (By.ID, "approver")
        self.submit_btn = (By.XPATH, "//button[contains(text(), 'Submit for Approval')]")
        self.selenium.wait_for_element_visible(self.approver_dropdown)
    
    def submit_for_approval(self, approver: str):
        from .status_tracker_page import StatusTrackerPage
        logger.info(f"✍️ Submitting: {approver}")
        self.selenium.select_dropdown(self.approver_dropdown, approver)
        self.selenium.click_element(self.submit_btn)
        return StatusTrackerPage(self.driver, self.selenium)
EOF

cat > cbaps/pages/status_tracker_page.py << 'EOF'
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
EOF

echo "✅ All CBAPS pages created (6 pages)"
