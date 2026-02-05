#!/bin/bash

# ========== DAWMS PAGES ==========

cat > dawms/pages/portal_home_page.py << 'EOF'
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
EOF

cat > dawms/pages/dawms_dashboard_page.py << 'EOF'
from selenium.webdriver.common.by import By
from loguru import logger

class DAWMSDashboardPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.intake_btn = (By.XPATH, "//button[contains(text(), 'Submission Intake')]")
        self.selenium.wait_for_element_visible(self.intake_btn)
        logger.info("✅ DAWMS Dashboard loaded")
    
    def go_to_submission_intake(self):
        from .submission_intake_page import SubmissionIntakePage
        self.selenium.click_element(self.intake_btn)
        logger.info("➡️ Submission Intake")
        return SubmissionIntakePage(self.driver, self.selenium)
EOF

cat > dawms/pages/submission_intake_page.py << 'EOF'
from selenium.webdriver.common.by import By
from loguru import logger

class SubmissionIntakePage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.type_dropdown = (By.ID, "submissionType")
        self.app_number_input = (By.ID, "applicationNumber")
        self.create_btn = (By.XPATH, "//button[contains(text(), 'Create Submission')]")
        self.selenium.wait_for_element_visible(self.type_dropdown)
    
    def create_submission(self, data):
        logger.info(f"📝 Creating submission: {data.application_number}")
        self.selenium.select_dropdown(self.type_dropdown, data.submission_type)
        self.selenium.enter_text(self.app_number_input, data.application_number)
        self.selenium.click_element(self.create_btn)
        from .reviewer_assignment_page import ReviewerAssignmentPage
        return ReviewerAssignmentPage(self.driver, self.selenium)
EOF

cat > dawms/pages/reviewer_assignment_page.py << 'EOF'
from selenium.webdriver.common.by import By
from loguru import logger
from typing import List

class ReviewerAssignmentPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.role_dropdown = (By.ID, "reviewerRole")
        self.name_input = (By.ID, "reviewerName")
        self.assign_btn = (By.XPATH, "//button[contains(text(), 'Assign')]")
        self.continue_btn = (By.XPATH, "//button[contains(text(), 'Route to Signature')]")
        self.selenium.wait_for_element_visible(self.role_dropdown)
    
    def assign_reviewer(self, data):
        logger.info(f"👤 Assigning: {data.name}")
        self.selenium.select_dropdown(self.role_dropdown, data.role)
        self.selenium.enter_text(self.name_input, data.name)
        self.selenium.click_element(self.assign_btn)
        return self
    
    def assign_multiple_reviewers(self, reviewers: List):
        for reviewer in reviewers:
            self.assign_reviewer(reviewer)
        return self
    
    def route_to_signature(self):
        from .signature_routing_page import SignatureRoutingPage
        self.selenium.click_element(self.continue_btn)
        return SignatureRoutingPage(self.driver, self.selenium)
EOF

cat > dawms/pages/signature_routing_page.py << 'EOF'
from selenium.webdriver.common.by import By
from loguru import logger

class SignatureRoutingPage:
    def __init__(self, driver, selenium):
        self.driver = driver
        self.selenium = selenium
        self.signer_dropdown = (By.ID, "signer")
        self.submit_btn = (By.XPATH, "//button[contains(text(), 'Submit for Signature')]")
        self.selenium.wait_for_element_visible(self.signer_dropdown)
    
    def submit_for_signature(self, signer: str):
        from .milestone_status_page import MilestoneStatusPage
        logger.info(f"✍️ Submitting: {signer}")
        self.selenium.select_dropdown(self.signer_dropdown, signer)
        self.selenium.click_element(self.submit_btn)
        return MilestoneStatusPage(self.driver, self.selenium)
EOF

cat > dawms/pages/milestone_status_page.py << 'EOF'
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
EOF

echo "✅ All DAWMS pages created (6 pages)"

# ========== API FILES ==========

cat > cbaps/api/api_helper.py << 'EOF'
import requests
from loguru import logger
from shared.config import CBAPS_API

class APIHelper:
    @staticmethod
    def get(endpoint: str):
        url = f"{CBAPS_API}{endpoint}"
        logger.info(f"📡 GET: {url}")
        return requests.get(url)
    
    @staticmethod
    def post(endpoint: str, data: dict):
        url = f"{CBAPS_API}{endpoint}"
        logger.info(f"📡 POST: {url}")
        return requests.post(url, json=data)
EOF

cat > cbaps/api/test_cbaps_api.py << 'EOF'
import pytest
from .api_helper import APIHelper

@pytest.mark.api
class TestCBAPSAPI:
    def test_get_requisitions(self):
        response = APIHelper.get("/requisitions")
        assert response.status_code == 200
    
    def test_create_requisition_via_api(self):
        data = {"title": "API Test", "fund_type": "Operations"}
        response = APIHelper.post("/requisitions", data)
        assert response.status_code == 201
EOF

cat > dawms/api/api_helper.py << 'EOF'
import requests
from loguru import logger
from shared.config import DAWMS_API

class APIHelper:
    @staticmethod
    def get(endpoint: str):
        url = f"{DAWMS_API}{endpoint}"
        logger.info(f"📡 GET: {url}")
        return requests.get(url)
    
    @staticmethod
    def post(endpoint: str, data: dict):
        url = f"{DAWMS_API}{endpoint}"
        logger.info(f"📡 POST: {url}")
        return requests.post(url, json=data)
EOF

cat > dawms/api/test_dawms_api.py << 'EOF'
import pytest
from .api_helper import APIHelper

@pytest.mark.api
class TestDAWMSAPI:
    def test_get_submissions(self):
        response = APIHelper.get("/submissions")
        assert response.status_code == 200
    
    def test_create_submission_via_api(self):
        data = {"type": "NDA", "app_number": "APP-123"}
        response = APIHelper.post("/submissions", data)
        assert response.status_code == 201
EOF

echo "✅ API files created"
