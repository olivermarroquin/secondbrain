package com.automation.cbaps.tests;

import org.testng.Assert;
import org.testng.annotations.Test;
import com.automation.cbaps.library.Base;
import com.automation.cbaps.models.RequisitionData;
import com.automation.cbaps.models.FundingLineData;
import com.automation.cbaps.pages.*;
import java.util.Arrays;
import java.util.List;

/**
 * CBAPS End-to-End Tests - Comprehensive test scenarios
 * Demonstrates TypeScript-level robustness with 6+ test scenarios
 */
public class CBAPSEndToEndTests extends Base {
    
    private static final String PORTAL_URL = "https://cbaps-portal.example.com";
    
    @Test(priority = 1, description = "Complete CBAPS workflow with all validations")
    public void completeWorkflowTest() {
        addStepToReport("Step 1: Navigate to CBAPS portal");
        gs.gotoWebsite(PORTAL_URL);
        
        String title = gs.getWebsiteTitle();
        Assert.assertTrue(title.contains("CBAPS"), "Portal title validation");
        addPassToReport("Portal loaded successfully");
        
        addStepToReport("Step 2: Create new requisition");
        RequisitionData reqData = new RequisitionData(
            "FY26 Cloud Infrastructure - " + System.currentTimeMillis(),
            "Cloud services for modernization",
            "Operations",
            "High"
        );
        
        RequisitionPage reqPage = new RequisitionPage(driver, gs);
        reqPage.createRequisition(reqData);
        addPassToReport("Requisition created");
        
        String reqId = reqPage.getRequisitionId();
        Assert.assertNotNull(reqId, "Requisition ID should not be null");
        addPassToReport("Requisition ID: " + reqId);
        
        addStepToReport("Step 3: Add multiple funding lines");
        FundingLinesPage fundingPage = reqPage.goToFundingLines();
        
        List<FundingLineData> fundingLines = Arrays.asList(
            new FundingLineData("25000", "2026"),
            new FundingLineData("15000", "2026"),
            new FundingLineData("10000", "2026")
        );
        
        fundingPage.addMultipleFundingLines(fundingLines);
        addPassToReport("Added " + fundingLines.size() + " funding lines");
        
        addStepToReport("Step 4: Validate funding calculations");
        int lineCount = fundingPage.getFundingLineCount();
        Assert.assertEquals(lineCount, 3, "Funding line count should be 3");
        
        double expectedTotal = 50000.0;
        boolean isTotalValid = fundingPage.validateTotalAmount(expectedTotal);
        Assert.assertTrue(isTotalValid, "Total amount should be $50,000");
        addPassToReport("Funding calculations validated");
        
        addStepToReport("Step 5: Route for approval");
        RoutingApprovalPage routingPage = fundingPage.continueToRouting();
        StatusTrackerPage statusPage = routingPage.submitForApproval("Branch Chief");
        
        addStepToReport("Step 6: Validate final status");
        boolean isStatusValid = statusPage.validateStatus("Submitted");
        Assert.assertTrue(isStatusValid, "Status should be 'Submitted'");
        addPassToReport("Complete workflow test passed!");
    }
    
    @Test(priority = 2, description = "Single funding line simplified flow")
    public void singleFundingLineTest() {
        addStepToReport("Test: Single funding line workflow");
        gs.gotoWebsite(PORTAL_URL);
        
        RequisitionData reqData = new RequisitionData(
            "Single Line Test - " + System.currentTimeMillis(),
            "Operations"
        );
        
        RequisitionPage reqPage = new RequisitionPage(driver, gs);
        reqPage.createRequisition(reqData);
        
        FundingLinesPage fundingPage = reqPage.goToFundingLines();
        fundingPage.addFundingLine(new FundingLineData("50000", "2026"));
        
        Assert.assertEquals(fundingPage.getFundingLineCount(), 1);
        Assert.assertTrue(fundingPage.validateTotalAmount(50000.0));
        
        addPassToReport("Single funding line test passed");
    }
    
    @Test(priority = 3, description = "Save requisition as draft")
    public void draftSaveTest() {
        addStepToReport("Test: Save requisition as draft");
        gs.gotoWebsite(PORTAL_URL);
        
        RequisitionData draftData = new RequisitionData(
            "Draft Requisition - " + System.currentTimeMillis(),
            "Draft for later completion",
            "Research",
            "Medium"
        );
        
        RequisitionPage reqPage = new RequisitionPage(driver, gs);
        reqPage.saveAsDraft(draftData);
        
        String status = reqPage.getStatus();
        Assert.assertEquals(status, "Draft", "Status should be 'Draft'");
        
        String reqId = reqPage.getRequisitionId();
        Assert.assertNotNull(reqId, "Draft should have an ID");
        
        Assert.assertTrue(reqPage.canEdit(), "Draft should be editable");
        addPassToReport("Draft save test passed - ID: " + reqId);
    }
    
    @Test(priority = 4, description = "Form validation test")
    public void formValidationTest() {
        addStepToReport("Test: Form validation");
        gs.gotoWebsite(PORTAL_URL);
        
        RequisitionPage reqPage = new RequisitionPage(driver, gs);
        
        // Test with partial data
        RequisitionData partialData = new RequisitionData("Test Req", "Operations");
        reqPage.fillRequisitionForm(partialData);
        
        boolean isValid = reqPage.validateForm();
        Assert.assertTrue(isValid, "Partial form should be valid");
        
        addPassToReport("Form validation test passed");
    }
    
    @Test(priority = 5, description = "Multiple funding lines with complex calculations")
    public void complexFundingCalculationsTest() {
        addStepToReport("Test: Complex funding calculations");
        gs.gotoWebsite(PORTAL_URL);
        
        RequisitionData reqData = new RequisitionData(
            "Complex Calc Test - " + System.currentTimeMillis(),
            "Facilities"
        );
        
        RequisitionPage reqPage = new RequisitionPage(driver, gs);
        reqPage.createRequisition(reqData);
        
        FundingLinesPage fundingPage = reqPage.goToFundingLines();
        
        List<FundingLineData> complexLines = Arrays.asList(
            new FundingLineData("12345.67", "2026"),
            new FundingLineData("23456.78", "2026"),
            new FundingLineData("34567.89", "2027"),
            new FundingLineData("9876.54", "2027")
        );
        
        fundingPage.addMultipleFundingLines(complexLines);
        
        double expectedTotal = 80246.88;
        Assert.assertTrue(fundingPage.validateLineCount(4));
        Assert.assertTrue(fundingPage.validateTotalAmount(expectedTotal));
        
        addPassToReport("Complex calculations validated");
    }
    
    @Test(priority = 6, description = "Verify routing availability")
    public void routingAvailabilityTest() {
        addStepToReport("Test: Routing availability check");
        gs.gotoWebsite(PORTAL_URL);
        
        RequisitionData reqData = new RequisitionData(
            "Routing Test - " + System.currentTimeMillis(),
            "Training"
        );
        
        RequisitionPage reqPage = new RequisitionPage(driver, gs);
        reqPage.createRequisition(reqData);
        
        FundingLinesPage fundingPage = reqPage.goToFundingLines();
        fundingPage.addFundingLine(new FundingLineData("25000", "2026"));
        
        Assert.assertTrue(fundingPage.canContinueToRouting(), "Should be able to continue to routing");
        addPassToReport("Routing availability test passed");
    }
}
