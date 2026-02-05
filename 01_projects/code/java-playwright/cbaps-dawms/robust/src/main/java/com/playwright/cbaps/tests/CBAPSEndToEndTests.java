package com.playwright.cbaps.tests;

import org.testng.Assert;
import org.testng.annotations.Test;
import com.playwright.cbaps.library.Base;
import com.playwright.cbaps.models.*;
import com.playwright.cbaps.pages.*;
import java.util.Arrays;

/**
 * CBAPS Comprehensive End-to-End Tests - 6+ Scenarios
 * Matches TypeScript version's robustness with full validation at each step
 */
public class CBAPSEndToEndTests extends Base {
    
    private static final String PORTAL_URL = "https://cbaps-portal.example.com";
    
    @Test(priority = 1, description = "Complete CBAPS workflow with comprehensive validations")
    public void completeWorkflowTest() {
        addStepToReport("Step 1: Navigate to CBAPS portal");
        pwm.navigateTo(PORTAL_URL);
        Assert.assertTrue(pwm.getTitle().contains("CBAPS"));
        addPassToReport("Portal loaded successfully");
        
        addStepToReport("Step 2: Create new requisition");
        RequisitionData reqData = new RequisitionData(
            "FY26 Cloud Infrastructure - " + System.currentTimeMillis(),
            "Cloud services modernization",
            "Operations",
            "High"
        );
        
        RequisitionPage reqPage = new RequisitionPage(page, pwm);
        reqPage.createRequisition(reqData);
        addPassToReport("Requisition created");
        
        String reqId = reqPage.getRequisitionId();
        Assert.assertNotNull(reqId, "Requisition ID should not be null");
        addPassToReport("Requisition ID: " + reqId);
        
        addStepToReport("Step 3: Add multiple funding lines");
        FundingLinesPage fundingPage = reqPage.goToFundingLines();
        fundingPage.addMultipleFundingLines(Arrays.asList(
            new FundingLineData("25000", "2026"),
            new FundingLineData("15000", "2026"),
            new FundingLineData("10000", "2026")
        ));
        addPassToReport("Added 3 funding lines");
        
        addStepToReport("Step 4: Validate funding calculations");
        Assert.assertEquals(fundingPage.getFundingLineCount(), 3);
        Assert.assertTrue(fundingPage.validateTotalAmount(50000.0));
        addPassToReport("Funding calculations validated");
        
        addStepToReport("Step 5: Route for approval");
        RoutingApprovalPage routingPage = fundingPage.continueToRouting();
        StatusTrackerPage statusPage = routingPage.submitForApproval("Branch Chief");
        
        addStepToReport("Step 6: Validate final status");
        Assert.assertTrue(statusPage.validateStatus("Submitted"));
        addPassToReport("Complete workflow test passed!");
    }
    
    @Test(priority = 2, description = "Single funding line simplified workflow")
    public void singleFundingLineTest() {
        addStepToReport("Test: Single funding line workflow");
        pwm.navigateTo(PORTAL_URL);
        
        RequisitionData reqData = new RequisitionData(
            "Single Line - " + System.currentTimeMillis(),
            "Operations"
        );
        
        RequisitionPage reqPage = new RequisitionPage(page, pwm);
        reqPage.createRequisition(reqData);
        
        FundingLinesPage fundingPage = reqPage.goToFundingLines();
        fundingPage.addFundingLine(new FundingLineData("50000", "2026"));
        
        Assert.assertEquals(fundingPage.getFundingLineCount(), 1);
        Assert.assertTrue(fundingPage.validateTotalAmount(50000.0));
        addPassToReport("Single funding line test passed");
    }
    
    @Test(priority = 3, description = "Save requisition as draft and validate metadata")
    public void draftSaveTest() {
        addStepToReport("Test: Draft save workflow");
        pwm.navigateTo(PORTAL_URL);
        
        RequisitionData draftData = new RequisitionData(
            "Draft - " + System.currentTimeMillis(),
            "Draft for later",
            "Research",
            "Medium"
        );
        
        RequisitionPage reqPage = new RequisitionPage(page, pwm);
        reqPage.saveAsDraft(draftData);
        
        Assert.assertEquals(reqPage.getStatus(), "Draft");
        Assert.assertNotNull(reqPage.getRequisitionId());
        Assert.assertTrue(reqPage.canEdit());
        
        String metadata = reqPage.getRequisitionMetadata();
        Assert.assertTrue(metadata.contains("Draft"));
        addPassToReport("Draft save test passed - " + metadata);
    }
    
    @Test(priority = 4, description = "Form validation tests")
    public void formValidationTest() {
        addStepToReport("Test: Form validation");
        pwm.navigateTo(PORTAL_URL);
        
        RequisitionPage reqPage = new RequisitionPage(page, pwm);
        
        // Test with valid partial data
        RequisitionData partialData = new RequisitionData("Test Req", "Operations");
        reqPage.fillRequisitionForm(partialData);
        
        Assert.assertTrue(reqPage.validateForm());
        Assert.assertTrue(reqPage.canSubmit());
        addPassToReport("Form validation test passed");
    }
    
    @Test(priority = 5, description = "Complex funding calculations with multiple lines")
    public void complexFundingCalculationsTest() {
        addStepToReport("Test: Complex funding calculations");
        pwm.navigateTo(PORTAL_URL);
        
        RequisitionData reqData = new RequisitionData(
            "Complex Calc - " + System.currentTimeMillis(),
            "Facilities"
        );
        
        RequisitionPage reqPage = new RequisitionPage(page, pwm);
        reqPage.createRequisition(reqData);
        
        FundingLinesPage fundingPage = reqPage.goToFundingLines();
        fundingPage.addMultipleFundingLines(Arrays.asList(
            new FundingLineData("12345.67", "2026"),
            new FundingLineData("23456.78", "2026"),
            new FundingLineData("34567.89", "2027"),
            new FundingLineData("9876.54", "2027")
        ));
        
        Assert.assertTrue(fundingPage.validateLineCount(4));
        Assert.assertTrue(fundingPage.validateTotalAmount(80246.88));
        addPassToReport("Complex calculations validated");
    }
    
    @Test(priority = 6, description = "Verify routing availability and state checks")
    public void routingAvailabilityTest() {
        addStepToReport("Test: Routing availability check");
        pwm.navigateTo(PORTAL_URL);
        
        RequisitionData reqData = new RequisitionData(
            "Routing Test - " + System.currentTimeMillis(),
            "Training"
        );
        
        RequisitionPage reqPage = new RequisitionPage(page, pwm);
        reqPage.createRequisition(reqData);
        
        Assert.assertTrue(reqPage.isFundingAvailable());
        
        FundingLinesPage fundingPage = reqPage.goToFundingLines();
        fundingPage.addFundingLine(new FundingLineData("25000", "2026"));
        
        Assert.assertTrue(fundingPage.canContinueToRouting());
        addPassToReport("Routing availability test passed");
    }
}
