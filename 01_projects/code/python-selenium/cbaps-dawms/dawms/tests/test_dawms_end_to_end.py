"""DAWMS End-to-End Tests - 7 Comprehensive Scenarios"""
import pytest
from shared.base_test import BaseTest
from shared.config import DAWMS_URL
from dawms.pages.portal_home_page import PortalHomePage
from dawms.models.submission_data import SubmissionData
from dawms.models.reviewer_data import ReviewerData

@pytest.mark.dawms
class TestDAWMSEndToEnd(BaseTest):
    
    @pytest.mark.smoke
    def test_complete_submission_workflow(self):
        """Test 1: Complete workflow - Portal → Dashboard → Intake → Reviewers → Signature → Status"""
        self.log_step("Step 1: Navigate to Portal")
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(DAWMS_URL)
        assert "DAWMS" in self.selenium.get_title()
        self.log_pass("Portal loaded")
        
        self.log_step("Step 2: Open DAWMS Dashboard")
        dashboard = portal.open_dawms()
        self.log_pass("Dashboard loaded")
        
        self.log_step("Step 3: Create submission intake")
        intake_page = dashboard.go_to_submission_intake()
        sub_data = SubmissionData(
            "NDA",
            f"APP-{self.selenium.get_random_text(10)}",
            "PharmaCorp",
            "DrugX"
        )
        reviewer_page = intake_page.create_submission(sub_data)
        self.log_pass("Submission created")
        
        self.log_step("Step 4: Assign multiple reviewers")
        reviewer_page.assign_multiple_reviewers([
            ReviewerData("Dr. Smith", "Clinical Reviewer", "Cardiology"),
            ReviewerData("Dr. Johnson", "Statistical Reviewer", "Biostatistics")
        ])
        self.log_pass("2 reviewers assigned")
        
        self.log_step("Step 5: Route to signature")
        signature_page = reviewer_page.route_to_signature()
        status_page = signature_page.submit_for_signature("Division Director")
        
        self.log_step("Step 6: Validate final milestone and status")
        assert status_page.validate_status("Pending Signature")
        assert status_page.validate_milestone("Signature Routing")
        self.log_pass("Complete DAWMS workflow passed!")
    
    def test_single_reviewer_workflow(self):
        """Test 2: Simplified workflow with single reviewer"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(DAWMS_URL)
        dashboard = portal.open_dawms()
        intake_page = dashboard.go_to_submission_intake()
        
        sub_data = SubmissionData("NDA", "APP-SINGLE-123")
        reviewer_page = intake_page.create_submission(sub_data)
        reviewer_page.assign_reviewer(ReviewerData("Dr. Brown", "Clinical Reviewer"))
        
        signature_page = reviewer_page.route_to_signature()
        status_page = signature_page.submit_for_signature("Director")
        
        assert status_page.validate_status("Pending Signature")
        self.log_pass("Single reviewer workflow passed")
    
    def test_multiple_reviewers_with_specialties(self):
        """Test 3: Multiple reviewers with different specialties"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(DAWMS_URL)
        dashboard = portal.open_dawms()
        intake_page = dashboard.go_to_submission_intake()
        
        sub_data = SubmissionData("BLA", "APP-MULTI-456", "BioPharma", "BioX")
        reviewer_page = intake_page.create_submission(sub_data)
        
        reviewer_page.assign_multiple_reviewers([
            ReviewerData("Dr. Lee", "Clinical", "Oncology"),
            ReviewerData("Dr. Chen", "Statistical", "Epidemiology"),
            ReviewerData("Dr. Patel", "Pharmacology", "Toxicology")
        ])
        
        signature_page = reviewer_page.route_to_signature()
        status_page = signature_page.submit_for_signature("Director")
        
        assert status_page.validate_milestone("Signature Routing")
        self.log_pass("Multiple reviewers with specialties validated")
    
    @pytest.mark.parametrize("sub_type", ["NDA", "BLA", "ANDA"])
    def test_different_submission_types(self, sub_type):
        """Test 4: Data-driven test with different submission types"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(DAWMS_URL)
        dashboard = portal.open_dawms()
        intake_page = dashboard.go_to_submission_intake()
        
        sub_data = SubmissionData(sub_type, f"APP-{sub_type}-789")
        reviewer_page = intake_page.create_submission(sub_data)
        
        reviewer_page.assign_reviewer(ReviewerData("Dr. Test", "Clinical"))
        signature_page = reviewer_page.route_to_signature()
        status_page = signature_page.submit_for_signature("Manager")
        
        assert status_page.validate_status("Pending Signature")
        self.log_pass(f"Submission type '{sub_type}' validated")
    
    def test_milestone_validation_at_each_step(self):
        """Test 5: Validate milestones at each workflow step"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(DAWMS_URL)
        dashboard = portal.open_dawms()
        
        intake_page = dashboard.go_to_submission_intake()
        self.log_pass("Milestone: Intake")
        
        sub_data = SubmissionData("NDA", "APP-MILESTONE-123")
        reviewer_page = intake_page.create_submission(sub_data)
        self.log_pass("Milestone: Reviewer Assignment")
        
        reviewer_page.assign_reviewer(ReviewerData("Dr. Test", "Clinical"))
        signature_page = reviewer_page.route_to_signature()
        self.log_pass("Milestone: Signature Routing")
        
        status_page = signature_page.submit_for_signature("Director")
        assert status_page.validate_milestone("Signature Routing")
        self.log_pass("All milestones validated")
    
    def test_full_navigation_flow_dawms(self):
        """Test 6: Validate full navigation through all DAWMS pages"""
        self.log_step("Test: Full DAWMS navigation")
        
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(DAWMS_URL)
        self.log_pass("Portal loaded")
        
        dashboard = portal.open_dawms()
        self.log_pass("Dashboard loaded")
        
        intake_page = dashboard.go_to_submission_intake()
        self.log_pass("Intake page loaded")
        
        reviewer_page = intake_page.create_submission(
            SubmissionData("NDA", "APP-NAV-999")
        )
        self.log_pass("Reviewer page loaded")
        
        reviewer_page.assign_reviewer(ReviewerData("Dr. Nav", "Clinical"))
        self.log_pass("Reviewer assigned")
        
        signature_page = reviewer_page.route_to_signature()
        self.log_pass("Signature page loaded")
        
        status_page = signature_page.submit_for_signature("Manager")
        self.log_pass("Status page loaded")
        
        assert status_page.validate_status("Pending Signature")
        self.log_pass("Full DAWMS navigation completed!")
    
    def test_status_and_milestone_combination(self):
        """Test 7: Validate status and milestone combination"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(DAWMS_URL)
        dashboard = portal.open_dawms()
        intake_page = dashboard.go_to_submission_intake()
        
        sub_data = SubmissionData("BLA", "APP-COMBO-777", "TestCorp", "TestDrug")
        reviewer_page = intake_page.create_submission(sub_data)
        reviewer_page.assign_reviewer(ReviewerData("Dr. Combo", "Clinical", "Cardiology"))
        
        signature_page = reviewer_page.route_to_signature()
        status_page = signature_page.submit_for_signature("Division Director")
        
        assert status_page.validate_status("Pending Signature")
        assert status_page.validate_milestone("Signature Routing")
        self.log_pass("Status and milestone combination validated")
