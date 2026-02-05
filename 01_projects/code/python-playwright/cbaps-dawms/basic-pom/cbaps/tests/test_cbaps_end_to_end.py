"""
CBAPS End-to-End Test: Complete workflow test
Tests: Portal → CBAPS Dashboard → Requisition → Funding → Routing → Status
"""

import logging
import pytest
from cbaps.library.base import Base
from cbaps.pages.portal_home_page import PortalHomePage
from cbaps.pages.cbaps_dashboard_page import CBAPSDashboardPage
from cbaps.pages.requisition_page import RequisitionPage
from cbaps.pages.funding_lines_page import FundingLinesPage
from cbaps.pages.routing_approval_page import RoutingApprovalPage
from cbaps.pages.status_tracker_page import StatusTrackerPage

logger = logging.getLogger(__name__)


class TestCBAPSEndToEnd(Base):
    """
    CBAPS End-to-End test class.
    This is the Python equivalent of the Java CBAPS_EndToEnd_Test class.
    """
    
    def test_cbaps_create_req_add_funding_route_verify_status(
        self, page, playwright_manager
    ):
        """
        Test complete CBAPS workflow:
        Portal → Dashboard → Requisition → Funding → Routing → Status
        
        Args:
            page: Playwright Page fixture
            playwright_manager: PlaywrightManager fixture
        """
        logger.info("Starting CBAPS E2E test: Create Req → Funding → Routing → Status")
        
        # Step 1: Navigate to Portal Home Page
        portal = PortalHomePage(page, playwright_manager)
        portal.navigate_to_portal("https://cbaps-portal.example.com")
        self.add_step_to_report("Step 1: Navigated to Portal Home Page.")
        
        # Step 2: Open CBAPS Dashboard
        dashboard = portal.open_cbaps()
        self.add_step_to_report("Step 2: Opened CBAPS Dashboard.")
        
        # Step 3: Navigate to Create Requisition Page
        req_page = dashboard.go_to_create_requisition()
        self.add_step_to_report("Step 3: Navigated to Create Requisition page.")
        
        # Step 4: Create Requisition
        req_page.create_requisition("FY26 Cloud Infrastructure Tools", "Operations")
        self.add_step_to_report(
            "Step 4: Created requisition with title 'FY26 Cloud Infrastructure Tools'."
        )
        
        # Step 5: Navigate to Funding Lines Page
        funding_page = req_page.go_to_funding_lines()
        self.add_step_to_report("Step 5: Navigated to Funding Lines page.")
        
        # Step 6: Add Funding Line
        funding_page.add_funding_line("5000")
        self.add_step_to_report("Step 6: Added funding line with amount $5000.")
        
        # Step 7: Continue to Routing
        routing_page = funding_page.continue_to_routing()
        self.add_step_to_report("Step 7: Continued to Routing/Approval page.")
        
        # Step 8: Submit for Approval
        status_page = routing_page.submit_for_approval("Branch Chief")
        self.add_step_to_report(
            "Step 8: Submitted requisition for approval to 'Branch Chief'."
        )
        
        # Step 9: Verify Status Transition
        actual_status = status_page.get_status()
        assert actual_status == "Submitted", f"Expected 'Submitted', got '{actual_status}'"
        self.add_step_to_report(
            f"Step 9: Verified workflow status is 'Submitted'. Actual: {actual_status}"
        )
        
        logger.info("CBAPS end-to-end test completed successfully.")
    
    def test_cbaps_create_req_multiple_funding_lines_route_verify_status(
        self, page, playwright_manager
    ):
        """
        Test CBAPS workflow with multiple funding lines:
        Portal → Dashboard → Requisition → Multiple Funding Lines → Routing → Status
        
        Args:
            page: Playwright Page fixture
            playwright_manager: PlaywrightManager fixture
        """
        logger.info("Starting CBAPS E2E test: Multiple Funding Lines Workflow")
        
        # Navigate to Portal
        portal = PortalHomePage(page, playwright_manager)
        portal.navigate_to_portal("https://cbaps-portal.example.com")
        self.add_step_to_report("Step 1: Navigated to Portal Home Page.")
        
        # Open CBAPS
        dashboard = portal.open_cbaps()
        self.add_step_to_report("Step 2: Opened CBAPS Dashboard.")
        
        # Create Requisition
        req_page = dashboard.go_to_create_requisition()
        req_page.create_requisition("FY26 IT Hardware Procurement", "Technology")
        self.add_step_to_report("Step 3: Created requisition for IT Hardware.")
        
        # Add Multiple Funding Lines
        funding_page = req_page.go_to_funding_lines()
        funding_page.add_funding_line("10000") \
                    .add_funding_line("7500") \
                    .add_funding_line("2500")
        self.add_step_to_report("Step 4: Added three funding lines totaling $20,000.")
        
        # Route for Approval
        routing_page = funding_page.continue_to_routing()
        status_page = routing_page.submit_for_approval("Division Director")
        self.add_step_to_report("Step 5: Routed for approval to Division Director.")
        
        # Verify Status
        status = status_page.get_status()
        assert status == "Submitted", f"Expected 'Submitted', got '{status}'"
        self.add_step_to_report(f"Step 6: Verified status is 'Submitted'. Actual: {status}")
        
        logger.info("Multiple funding lines test completed successfully.")


# Pytest markers for test organization
pytestmark = [
    pytest.mark.cbaps,
    pytest.mark.end_to_end
]
