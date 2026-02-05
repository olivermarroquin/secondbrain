"""CBAPS End-to-End Tests - 7 Comprehensive Scenarios"""
import pytest
from shared.base_test import BaseTest
from shared.config import CBAPS_URL
from cbaps.pages.portal_home_page import PortalHomePage
from cbaps.models.requisition_data import RequisitionData
from cbaps.models.funding_line_data import FundingLineData

@pytest.mark.cbaps
class TestCBAPSEndToEnd(BaseTest):
    
    @pytest.mark.smoke
    def test_complete_workflow_with_multiple_funding_lines(self):
        """Test 1: Complete workflow - Portal → Dashboard → Requisition → Funding → Routing → Status"""
        self.log_step("Step 1: Navigate to Portal")
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(CBAPS_URL)
        assert "CBAPS" in self.selenium.get_title()
        self.log_pass("Portal loaded")
        
        self.log_step("Step 2: Open CBAPS Dashboard")
        dashboard = portal.open_cbaps()
        self.log_pass("Dashboard loaded")
        
        self.log_step("Step 3: Create Requisition")
        req_page = dashboard.go_to_create_requisition()
        req_data = RequisitionData(
            title=f"FY26 Project {self.selenium.get_random_text(10)}",
            fund_type="Operations",
            description="Automation test",
            priority="High"
        )
        req_page.create_requisition(req_data)
        req_id = req_page.get_requisition_id()
        assert req_id is not None
        self.log_pass(f"Requisition created: {req_id}")
        
        self.log_step("Step 4: Add multiple funding lines")
        funding_page = req_page.go_to_funding_lines()
        funding_page.add_multiple_lines([
            FundingLineData("25000", "2026"),
            FundingLineData("15000", "2026"),
            FundingLineData("10000", "2026")
        ])
        assert funding_page.validate_count(3)
        assert funding_page.validate_total(50000.0)
        self.log_pass("3 funding lines added, total: $50,000")
        
        self.log_step("Step 5: Route for approval")
        routing_page = funding_page.continue_to_routing()
        status_page = routing_page.submit_for_approval("Branch Chief")
        
        self.log_step("Step 6: Validate final status")
        assert status_page.validate_status("Submitted")
        self.log_pass("Complete workflow passed!")
    
    def test_single_funding_line_workflow(self):
        """Test 2: Simplified workflow with single funding line"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(CBAPS_URL)
        dashboard = portal.open_cbaps()
        req_page = dashboard.go_to_create_requisition()
        
        req_data = RequisitionData("Single Line Test", "Operations")
        req_page.create_requisition(req_data)
        
        funding_page = req_page.go_to_funding_lines()
        funding_page.add_funding_line(FundingLineData("30000", "2026"))
        
        assert funding_page.validate_count(1)
        assert funding_page.validate_total(30000.0)
        self.log_pass("Single funding line test passed")
    
    def test_complex_funding_calculations(self):
        """Test 3: Complex funding amounts validation"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(CBAPS_URL)
        dashboard = portal.open_cbaps()
        req_page = dashboard.go_to_create_requisition()
        
        req_data = RequisitionData("Complex Calculation Test", "Operations")
        req_page.create_requisition(req_data)
        
        funding_page = req_page.go_to_funding_lines()
        funding_page.add_multiple_lines([
            FundingLineData("12345.67", "2026"),
            FundingLineData("23456.78", "2026"),
            FundingLineData("34567.89", "2026"),
            FundingLineData("9876.54", "2026")
        ])
        
        assert funding_page.validate_count(4)
        assert funding_page.validate_total(80246.88)
        self.log_pass("Complex calculations validated: $80,246.88")
    
    def test_status_validation_at_each_step(self):
        """Test 4: Validate status transitions"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(CBAPS_URL)
        dashboard = portal.open_cbaps()
        req_page = dashboard.go_to_create_requisition()
        
        req_data = RequisitionData("Status Validation Test", "Operations")
        req_page.create_requisition(req_data)
        
        assert req_page.validate_status("Draft")
        self.log_pass("Status after creation: Draft")
        
        funding_page = req_page.go_to_funding_lines()
        funding_page.add_funding_line(FundingLineData("20000", "2026"))
        
        routing_page = funding_page.continue_to_routing()
        status_page = routing_page.submit_for_approval("Director")
        
        assert status_page.validate_status("Submitted")
        self.log_pass("Final status: Submitted")
    
    def test_requisition_id_generation(self):
        """Test 5: Validate requisition ID is generated"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(CBAPS_URL)
        dashboard = portal.open_cbaps()
        req_page = dashboard.go_to_create_requisition()
        
        req_data = RequisitionData("ID Generation Test", "Operations")
        req_page.create_requisition(req_data)
        
        req_id = req_page.get_requisition_id()
        assert req_id is not None
        assert len(req_id) > 0
        self.log_pass(f"Requisition ID generated: {req_id}")
    
    @pytest.mark.parametrize("fund_type", ["Operations", "Capital", "Grant"])
    def test_different_fund_types(self, fund_type):
        """Test 6: Data-driven test with different fund types"""
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(CBAPS_URL)
        dashboard = portal.open_cbaps()
        req_page = dashboard.go_to_create_requisition()
        
        req_data = RequisitionData(f"{fund_type} Test", fund_type)
        req_page.create_requisition(req_data)
        
        assert req_page.get_requisition_id() is not None
        self.log_pass(f"Fund type '{fund_type}' validated")
    
    def test_full_navigation_flow(self):
        """Test 7: Validate full navigation flow"""
        self.log_step("Test: Full navigation flow")
        
        portal = PortalHomePage(self.driver, self.selenium)
        portal.navigate_to_portal(CBAPS_URL)
        self.log_pass("Portal loaded")
        
        dashboard = portal.open_cbaps()
        self.log_pass("Dashboard loaded")
        
        req_page = dashboard.go_to_create_requisition()
        self.log_pass("Requisition page loaded")
        
        req_page.create_requisition(RequisitionData("Nav Test", "Operations"))
        self.log_pass("Requisition created")
        
        funding_page = req_page.go_to_funding_lines()
        self.log_pass("Funding page loaded")
        
        funding_page.add_funding_line(FundingLineData("15000", "2026"))
        self.log_pass("Funding added")
        
        routing_page = funding_page.continue_to_routing()
        self.log_pass("Routing page loaded")
        
        status_page = routing_page.submit_for_approval("Manager")
        self.log_pass("Status page loaded")
        
        assert status_page.validate_status("Submitted")
        self.log_pass("Full navigation flow completed!")
