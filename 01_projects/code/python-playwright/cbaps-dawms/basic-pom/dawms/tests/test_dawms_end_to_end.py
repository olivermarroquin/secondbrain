"""
DAWMS End-to-End Test: Complete workflow test
Tests: Portal → DAWMS Dashboard → Intake → Assign Reviewer → Signature → Milestone
"""

import logging
import pytest
from dawms.library.base import Base
from dawms.pages.portal_home_page import PortalHomePage
from dawms.pages.dawms_dashboard_page import DAWMSDashboardPage
from dawms.pages.submission_intake_page import SubmissionIntakePage
from dawms.pages.reviewer_assignment_page import ReviewerAssignmentPage
from dawms.pages.signature_routing_page import SignatureRoutingPage
from dawms.pages.milestone_status_page import MilestoneStatusPage

logger = logging.getLogger(__name__)


class TestDAWMSEndToEnd(Base):
    """
    DAWMS End-to-End test class.
    This is the Python equivalent of the Java DAWMS_EndToEnd_Test class.
    """
    
    def test_dawms_intake_assign_route_signature_verify_milestone(
        self, page, playwright_manager
    ):
        """
        Test complete DAWMS workflow:
        Portal → Dashboard → Intake → Assign Reviewer → Signature → Milestone
        
        Args:
            page: Playwright Page fixture
            playwright_manager: PlaywrightManager fixture
        """
        logger.info("Starting DAWMS E2E test: Intake → Assign → Signature → Milestone")
        
        # Step 1: Navigate to Portal Home Page
        portal = PortalHomePage(page, playwright_manager)
        portal.navigate_to_portal("https://dawms-portal.example.com")
        self.add_step_to_report("Step 1: Navigated to Portal Home Page.")
        
        # Step 2: Open DAWMS Dashboard
        dashboard = portal.open_dawms()
        self.add_step_to_report("Step 2: Opened DAWMS Dashboard.")
        
        # Step 3: Navigate to Submission Intake Page
        intake = dashboard.go_to_submission_intake()
        self.add_step_to_report("Step 3: Navigated to Submission Intake page.")
        
        # Step 4: Create Submission
        assignment = intake.create_submission("NDA", "123456")
        self.add_step_to_report(
            "Step 4: Created submission intake record with type 'NDA' and number '123456'."
        )
        
        # Step 5: Assign Reviewer and Route to Signature
        signature = assignment.assign_reviewer(
            "Clinical Reviewer", "Jane Doe"
        ).route_to_signature_step()
        self.add_step_to_report(
            "Step 5: Assigned 'Clinical Reviewer: Jane Doe' and routed to signature step."
        )
        
        # Step 6: Submit for Signature
        status = signature.submit_for_signature("Division Director")
        self.add_step_to_report(
            "Step 6: Submitted workflow for signature to 'Division Director'."
        )
        
        # Step 7: Verify Status Transition
        actual_status = status.get_status()
        assert actual_status == "Pending Signature", \
            f"Expected 'Pending Signature', got '{actual_status}'"
        self.add_step_to_report(
            f"Step 7: Verified status is 'Pending Signature'. Actual: {actual_status}"
        )
        
        # Step 8: Verify Milestone Update
        actual_milestone = status.get_milestone()
        assert actual_milestone == "Signature Routing", \
            f"Expected 'Signature Routing', got '{actual_milestone}'"
        self.add_step_to_report(
            f"Step 8: Verified milestone is 'Signature Routing'. Actual: {actual_milestone}"
        )
        
        logger.info("DAWMS end-to-end test completed successfully.")
    
    def test_dawms_multiple_reviewers_signature_verify_workflow(
        self, page, playwright_manager
    ):
        """
        Test DAWMS workflow with multiple reviewers:
        Portal → Dashboard → Intake → Multiple Reviewers → Signature → Milestone
        
        Args:
            page: Playwright Page fixture
            playwright_manager: PlaywrightManager fixture
        """
        logger.info("Starting DAWMS E2E test: Multiple Reviewers Assignment Workflow")
        
        # Navigate to Portal
        portal = PortalHomePage(page, playwright_manager)
        portal.navigate_to_portal("https://dawms-portal.example.com")
        self.add_step_to_report("Step 1: Navigated to Portal Home Page.")
        
        # Open DAWMS
        dashboard = portal.open_dawms()
        self.add_step_to_report("Step 2: Opened DAWMS Dashboard.")
        
        # Create Submission
        intake = dashboard.go_to_submission_intake()
        assignment = intake.create_submission("BLA", "789012")
        self.add_step_to_report("Step 3: Created BLA submission with number 789012.")
        
        # Assign Multiple Reviewers
        signature = assignment.assign_reviewer("Clinical Reviewer", "Dr. Smith") \
                              .assign_reviewer("Pharmacologist", "Dr. Johnson") \
                              .assign_reviewer("Statistical Reviewer", "Dr. Williams") \
                              .route_to_signature_step()
        self.add_step_to_report(
            "Step 4: Assigned three reviewers (Clinical, Pharmacologist, Statistical)."
        )
        
        # Route for Signature
        status = signature.submit_for_signature("Center Director")
        self.add_step_to_report("Step 5: Routed for signature to Center Director.")
        
        # Verify Status and Milestone
        actual_status = status.get_status()
        actual_milestone = status.get_milestone()
        
        assert actual_status == "Pending Signature", \
            f"Expected 'Pending Signature', got '{actual_status}'"
        assert actual_milestone == "Signature Routing", \
            f"Expected 'Signature Routing', got '{actual_milestone}'"
        
        self.add_step_to_report(
            "Step 6: Verified status is 'Pending Signature' and milestone is 'Signature Routing'."
        )
        logger.info("Multiple reviewers workflow test completed successfully.")


# Pytest markers for test organization
pytestmark = [
    pytest.mark.dawms,
    pytest.mark.end_to_end
]
