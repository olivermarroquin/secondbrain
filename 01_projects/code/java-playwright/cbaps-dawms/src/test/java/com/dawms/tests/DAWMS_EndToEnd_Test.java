package com.dawms.tests;

import static org.assertj.core.api.Assertions.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.Test;

import com.aventstack.extentreports.Status;
import com.dawms.library.Base;
import com.dawms.pages.DAWMSDashboardPage;
import com.dawms.pages.MilestoneStatusPage;
import com.dawms.pages.PortalHomePage;
import com.dawms.pages.ReviewerAssignmentPage;
import com.dawms.pages.SignatureRoutingPage;
import com.dawms.pages.SubmissionIntakePage;

/**
 * DAWMS_EndToEnd_Test: Complete end-to-end workflow test
 * Tests: Portal → DAWMS Dashboard → Intake → Assign Reviewer → Signature → Milestone
 */
public class DAWMS_EndToEnd_Test extends Base {

	private static final Logger log = LoggerFactory.getLogger(DAWMS_EndToEnd_Test.class);

	@Test
	public void dawms_intake_assign_routeSignature_verifyMilestone() {

		// Create test node in ExtentReports
		test = extent.createTest("DAWMS E2E: Intake → Assign Reviewer → Signature → Milestone");

		// Step 1: Navigate to Portal Home Page
		PortalHomePage portal = new PortalHomePage(page, myPlaywright);
		portal.navigateToPortal("https://dawms-portal.example.com");
		addStepToReport("Step 1: Navigated to Portal Home Page.");

		// Step 2: Open DAWMS Dashboard
		DAWMSDashboardPage dashboard = portal.openDAWMS();
		addStepToReport("Step 2: Opened DAWMS Dashboard.");

		// Step 3: Navigate to Submission Intake Page
		SubmissionIntakePage intake = dashboard.goToSubmissionIntake();
		addStepToReport("Step 3: Navigated to Submission Intake page.");

		// Step 4: Create Submission
		ReviewerAssignmentPage assignment = intake.createSubmission("NDA", "123456");
		addStepToReport("Step 4: Created submission intake record with type 'NDA' and application number '123456'.");

		// Step 5: Assign Reviewer and Route to Signature
		SignatureRoutingPage signature = assignment
				.assignReviewer("Clinical Reviewer", "Jane Doe")
				.routeToSignatureStep();
		addStepToReport("Step 5: Assigned 'Clinical Reviewer: Jane Doe' and routed to signature step.");

		// Step 6: Submit for Signature
		MilestoneStatusPage status = signature.submitForSignature("Division Director");
		addStepToReport("Step 6: Submitted workflow for signature to 'Division Director'.");

		// Step 7: Verify Status Transition
		String actualStatus = status.getStatus();
		assertThat(actualStatus).as("Status should transition to 'Pending Signature'")
				.isEqualTo("Pending Signature");
		addStepToReport("Step 7: Verified status transitioned to 'Pending Signature'. Actual: " + actualStatus);

		// Step 8: Verify Milestone Update
		String actualMilestone = status.getMilestone();
		assertThat(actualMilestone).as("Milestone should update to 'Signature Routing'")
				.isEqualTo("Signature Routing");
		addStepToReport("Step 8: Verified milestone updated to 'Signature Routing'. Actual: " + actualMilestone);

		log.info("DAWMS end-to-end test completed successfully.");
	}

	@Test
	public void dawms_multipleReviewers_signature_verifyWorkflow() {

		test = extent.createTest("DAWMS E2E: Multiple Reviewers Assignment Workflow");

		// Navigate to Portal
		PortalHomePage portal = new PortalHomePage(page, myPlaywright);
		portal.navigateToPortal("https://dawms-portal.example.com");
		addStepToReport("Step 1: Navigated to Portal Home Page.");

		// Open DAWMS
		DAWMSDashboardPage dashboard = portal.openDAWMS();
		addStepToReport("Step 2: Opened DAWMS Dashboard.");

		// Create Submission
		SubmissionIntakePage intake = dashboard.goToSubmissionIntake();
		ReviewerAssignmentPage assignment = intake.createSubmission("BLA", "789012");
		addStepToReport("Step 3: Created BLA submission with application number 789012.");

		// Assign Multiple Reviewers
		SignatureRoutingPage signature = assignment
				.assignReviewer("Clinical Reviewer", "Dr. Smith")
				.assignReviewer("Pharmacologist", "Dr. Johnson")
				.assignReviewer("Statistical Reviewer", "Dr. Williams")
				.routeToSignatureStep();
		addStepToReport("Step 4: Assigned three reviewers (Clinical, Pharmacologist, Statistical).");

		// Route for Signature
		MilestoneStatusPage status = signature.submitForSignature("Center Director");
		addStepToReport("Step 5: Routed for signature to Center Director.");

		// Verify Status and Milestone
		String actualStatus = status.getStatus();
		String actualMilestone = status.getMilestone();
		
		assertThat(actualStatus).as("Status verification").isEqualTo("Pending Signature");
		assertThat(actualMilestone).as("Milestone verification").isEqualTo("Signature Routing");
		
		addStepToReport("Step 6: Verified status is 'Pending Signature' and milestone is 'Signature Routing'.");
		log.info("Multiple reviewers workflow test completed successfully.");
	}
}
