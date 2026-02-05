package com.cbaps.tests;

import static org.assertj.core.api.Assertions.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.Test;

import com.aventstack.extentreports.Status;
import com.cbaps.library.Base;
import com.cbaps.pages.CBAPSDashboardPage;
import com.cbaps.pages.FundingLinesPage;
import com.cbaps.pages.PortalHomePage;
import com.cbaps.pages.RequisitionPage;
import com.cbaps.pages.RoutingApprovalPage;
import com.cbaps.pages.StatusTrackerPage;

/**
 * CBAPS_EndToEnd_Test: Complete end-to-end workflow test
 * Tests: Portal → CBAPS Dashboard → Requisition → Funding → Routing → Status
 */
public class CBAPS_EndToEnd_Test extends Base {

	private static final Logger log = LoggerFactory.getLogger(CBAPS_EndToEnd_Test.class);

	@Test
	public void cbaps_createReq_addFunding_route_verifyStatus() {

		// Create test node in ExtentReports
		test = extent.createTest("CBAPS E2E: Create Req → Funding → Routing → Status");

		// Step 1: Navigate to Portal Home Page
		PortalHomePage portal = new PortalHomePage(page, myPlaywright);
		portal.navigateToPortal("https://cbaps-portal.example.com");
		addStepToReport("Step 1: Navigated to Portal Home Page.");

		// Step 2: Open CBAPS Dashboard
		CBAPSDashboardPage dashboard = portal.openCBAPS();
		addStepToReport("Step 2: Opened CBAPS Dashboard.");

		// Step 3: Navigate to Create Requisition Page
		RequisitionPage reqPage = dashboard.goToCreateRequisition();
		addStepToReport("Step 3: Navigated to Create Requisition page.");

		// Step 4: Create Requisition with title and fund type
		reqPage.createRequisition("FY26 Cloud Infrastructure Tools", "Operations");
		addStepToReport("Step 4: Created requisition with title 'FY26 Cloud Infrastructure Tools' and fund type 'Operations'.");

		// Step 5: Navigate to Funding Lines Page
		FundingLinesPage fundingPage = reqPage.goToFundingLines();
		addStepToReport("Step 5: Navigated to Funding Lines page.");

		// Step 6: Add Funding Line
		fundingPage.addFundingLine("5000");
		addStepToReport("Step 6: Added funding line with amount $5000.");

		// Step 7: Continue to Routing
		RoutingApprovalPage routingPage = fundingPage.continueToRouting();
		addStepToReport("Step 7: Continued to Routing/Approval page.");

		// Step 8: Submit for Approval
		StatusTrackerPage statusPage = routingPage.submitForApproval("Branch Chief");
		addStepToReport("Step 8: Submitted requisition for approval to 'Branch Chief'.");

		// Step 9: Verify Status Transition
		String actualStatus = statusPage.getStatus();
		assertThat(actualStatus).as("Status should transition to 'Submitted'").isEqualTo("Submitted");
		addStepToReport("Step 9: Verified workflow status transitioned to 'Submitted'. Actual: " + actualStatus);

		log.info("CBAPS end-to-end test completed successfully.");
	}

	@Test
	public void cbaps_createReq_multipleF​undingLines_route_verifyStatus() {

		test = extent.createTest("CBAPS E2E: Multiple Funding Lines Workflow");

		// Navigate to Portal
		PortalHomePage portal = new PortalHomePage(page, myPlaywright);
		portal.navigateToPortal("https://cbaps-portal.example.com");
		addStepToReport("Step 1: Navigated to Portal Home Page.");

		// Open CBAPS
		CBAPSDashboardPage dashboard = portal.openCBAPS();
		addStepToReport("Step 2: Opened CBAPS Dashboard.");

		// Create Requisition
		RequisitionPage reqPage = dashboard.goToCreateRequisition();
		reqPage.createRequisition("FY26 IT Hardware Procurement", "Technology");
		addStepToReport("Step 3: Created requisition for IT Hardware.");

		// Add Multiple Funding Lines
		FundingLinesPage fundingPage = reqPage.goToFundingLines();
		fundingPage.addFundingLine("10000")
		           .addFundingLine("7500")
		           .addFundingLine("2500");
		addStepToReport("Step 4: Added three funding lines totaling $20,000.");

		// Route for Approval
		RoutingApprovalPage routingPage = fundingPage.continueToRouting();
		StatusTrackerPage statusPage = routingPage.submitForApproval("Division Director");
		addStepToReport("Step 5: Routed for approval to Division Director.");

		// Verify Status
		String status = statusPage.getStatus();
		assertThat(status).as("Status verification").isEqualTo("Submitted");
		addStepToReport("Step 6: Verified status is 'Submitted'. Actual: " + status);

		log.info("Multiple funding lines test completed successfully.");
	}
}
