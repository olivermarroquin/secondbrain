/**
 * CBAPS End-to-End Tests: Comprehensive workflow testing
 * Tests complete workflows with validation, error handling, and multiple scenarios
 */

import { test, expect, TestUtils } from '../library/BaseTest';
import { PortalHomePage } from '../pages/PortalHomePage';
import { RequisitionData, RequisitionStatus, FundType, FundingLineData } from '../library/types';

test.describe('CBAPS End-to-End Workflow Tests', () => {
  const PORTAL_URL = 'https://cbaps-portal.example.com';

  test.beforeEach(async ({ testPage, pwManager }) => {
    TestUtils.logInfo('Starting new CBAPS test');
  });

  test('Complete CBAPS workflow: Requisition → Funding → Routing → Status', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Step 1: Navigate to Portal and validate');
    
    // Initialize portal page
    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);
    
    // Validate portal loaded correctly
    const isPortalValid = await portal.validatePortalLoaded();
    expect(isPortalValid).toBeTruthy();
    
    const title = await portal.getTitle();
    expect(title).toContain('Portal');
    TestUtils.logSuccess('Portal loaded and validated');

    // ====== Step 2: Navigate to CBAPS Dashboard ======
    TestUtils.logStep('Step 2: Open CBAPS Dashboard and validate');
    
    const dashboard = await portal.openCBAPS();
    const isDashboardValid = await dashboard.validateDashboardLoaded();
    expect(isDashboardValid).toBeTruthy();
    
    // Get dashboard metrics for reporting
    const metrics = await dashboard.getDashboardMetrics();
    TestUtils.logInfo(`Dashboard metrics - Total: ${metrics.totalRequisitions}, Pending: ${metrics.pendingApprovals}`);
    TestUtils.logSuccess('Dashboard validated');

    // ====== Step 3: Create Requisition ======
    TestUtils.logStep('Step 3: Navigate to Create Requisition page');
    
    const reqPage = await dashboard.goToCreateRequisition();
    
    TestUtils.logStep('Step 4: Create new requisition with validation');
    
    const requisitionData: RequisitionData = {
      title: `FY26 Cloud Infrastructure - ${TestUtils.timestamp()}`,
      description: 'Cloud services and infrastructure for modernization initiative',
      fundType: FundType.Operations,
      priority: 'High'
    };
    
    // Fill and validate form before submission
    await reqPage.fillRequisitionForm(requisitionData);
    const formValidation = await reqPage.validateForm();
    expect(formValidation.isValid).toBeTruthy();
    
    // Submit requisition
    await reqPage.createRequisition(requisitionData);
    
    // Get and validate requisition ID
    const reqId = await reqPage.getRequisitionId();
    expect(reqId).toBeTruthy();
    TestUtils.logSuccess(`Requisition created with ID: ${reqId}`);

    // ====== Step 5: Add Funding Lines ======
    TestUtils.logStep('Step 5: Navigate to Funding Lines');
    
    const fundingPage = await reqPage.goToFundingLines();
    await fundingPage.waitForTableReady();
    
    TestUtils.logStep('Step 6: Add multiple funding lines');
    
    const fundingLines: FundingLineData[] = [
      { amount: '25000', fiscalYear: '2026', category: 'Infrastructure', description: 'Cloud hosting' },
      { amount: '15000', fiscalYear: '2026', category: 'Software', description: 'Licenses' },
      { amount: '10000', fiscalYear: '2026', category: 'Services', description: 'Support' }
    ];
    
    await fundingPage.addMultipleFundingLines(fundingLines);
    
    // Validate funding line count
    const lineCount = await fundingPage.getFundingLineCount();
    expect(lineCount).toBe(fundingLines.length);
    TestUtils.logSuccess(`Added ${lineCount} funding lines`);
    
    // Validate total amount
    const expectedTotal = fundingLines.reduce((sum, line) => sum + parseFloat(line.amount), 0);
    const actualTotal = await fundingPage.getTotalAmount();
    expect(actualTotal).toBe(expectedTotal);
    TestUtils.logSuccess(`Total amount validated: $${actualTotal}`);
    
    // Verify calculation
    const isCalculationValid = await fundingPage.verifyTotalCalculation();
    expect(isCalculationValid).toBeTruthy();

    // ====== Step 7: Route for Approval ======
    TestUtils.logStep('Step 7: Continue to Routing/Approval');
    
    const canContinue = await fundingPage.canContinueToRouting();
    expect(canContinue).toBeTruthy();
    
    const routingPage = await fundingPage.continueToRouting();
    
    TestUtils.logStep('Step 8: Submit routing for approval');
    
    const approverComments = 'Urgent approval needed for Q1 2026 initiative';
    const statusPage = await routingPage.submitForApproval('Branch Chief', approverComments);

    // ====== Step 9: Validate Status ======
    TestUtils.logStep('Step 9: Validate workflow status and results');
    
    const finalStatus = await statusPage.getStatus();
    expect(finalStatus).toBe(RequisitionStatus.Submitted);
    TestUtils.logSuccess(`Final status: ${finalStatus}`);
    
    // Get complete workflow result
    const workflowResult = await statusPage.getWorkflowResult();
    expect(workflowResult.status).toBe(RequisitionStatus.Submitted);
    expect(workflowResult.requisitionId).toBeTruthy();
    
    TestUtils.logSuccess('✅ Complete CBAPS workflow test passed');
  });

  test('CBAPS workflow with single funding line - simplified flow', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Single funding line workflow');
    
    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);
    
    const dashboard = await portal.openCBAPS();
    const reqPage = await dashboard.goToCreateRequisition();
    
    // Create requisition
    const requisitionData: RequisitionData = {
      title: `Single Line Test - ${TestUtils.randomString(6)}`,
      fundType: FundType.Technology
    };
    
    await reqPage.createRequisition(requisitionData);
    
    // Add single funding line
    const fundingPage = await reqPage.goToFundingLines();
    await fundingPage.addFundingLine({ amount: '50000', fiscalYear: '2026' });
    
    // Validate
    const total = await fundingPage.getTotalAmount();
    expect(total).toBe(50000);
    
    const count = await fundingPage.getFundingLineCount();
    expect(count).toBe(1);
    
    // Route and verify
    const routingPage = await fundingPage.continueToRouting();
    const statusPage = await routingPage.submitForApproval('Division Director');
    
    const status = await statusPage.validateStatus(RequisitionStatus.Submitted);
    expect(status).toBeTruthy();
    
    TestUtils.logSuccess('✅ Single funding line workflow test passed');
  });

  test('CBAPS workflow with draft save and resume', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Save as draft and resume workflow');
    
    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);
    
    const dashboard = await portal.openCBAPS();
    const reqPage = await dashboard.goToCreateRequisition();
    
    // Save as draft
    const draftData: RequisitionData = {
      title: `Draft Requisition - ${TestUtils.timestamp()}`,
      description: 'This is a draft for later completion',
      fundType: FundType.Research,
      priority: 'Medium'
    };
    
    await reqPage.saveAsDraft(draftData);
    
    // Validate draft status
    const status = await reqPage.getStatus();
    expect(status).toBe(RequisitionStatus.Draft);
    
    // Get metadata
    const metadata = await reqPage.getRequisitionMetadata();
    expect(metadata.status).toBe(RequisitionStatus.Draft);
    expect(metadata.id).toBeTruthy();
    
    TestUtils.logSuccess(`✅ Draft saved with ID: ${metadata.id}`);
    
    // Verify edit capability
    const canEdit = await reqPage.canEdit();
    expect(canEdit).toBeTruthy();
    
    TestUtils.logSuccess('✅ Draft save workflow test passed');
  });

  test('CBAPS workflow validation - form validation tests', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Form validation checks');
    
    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);
    
    const dashboard = await portal.openCBAPS();
    const reqPage = await dashboard.goToCreateRequisition();
    
    // Test empty form validation
    const emptyValidation = await reqPage.validateForm();
    expect(emptyValidation.isValid).toBeFalsy();
    expect(emptyValidation.errors.length).toBeGreaterThan(0);
    TestUtils.logInfo(`Empty form errors: ${emptyValidation.errors.join(', ')}`);
    
    // Fill partial form
    await reqPage.fillRequisitionForm({
      title: 'Test Requisition',
      fundType: FundType.Operations
    });
    
    // Validate again
    const partialValidation = await reqPage.validateForm();
    expect(partialValidation.isValid).toBeTruthy();
    
    TestUtils.logSuccess('✅ Form validation test passed');
  });

  test('CBAPS workflow - funding lines calculation validation', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Complex funding lines calculations');
    
    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);
    
    const dashboard = await portal.openCBAPS();
    const reqPage = await dashboard.goToCreateRequisition();
    
    // Create requisition
    await reqPage.createRequisition({
      title: `Calculation Test - ${TestUtils.randomString(6)}`,
      fundType: FundType.Facilities
    });
    
    const fundingPage = await reqPage.goToFundingLines();
    
    // Add multiple lines with various amounts
    const complexLines: FundingLineData[] = [
      { amount: '12345.67', fiscalYear: '2026', category: 'Equipment' },
      { amount: '23456.78', fiscalYear: '2026', category: 'Services' },
      { amount: '34567.89', fiscalYear: '2027', category: 'Maintenance' },
      { amount: '9876.54', fiscalYear: '2027', category: 'Training' }
    ];
    
    await fundingPage.addMultipleFundingLines(complexLines);
    
    // Calculate expected total
    const expectedTotal = complexLines.reduce((sum, line) => sum + parseFloat(line.amount), 0);
    
    // Validate count
    await fundingPage.validateLineCount(complexLines.length);
    
    // Validate total with tolerance
    await fundingPage.validateTotalAmount(expectedTotal, 0.01);
    
    // Verify calculation matches
    const isValid = await fundingPage.verifyTotalCalculation();
    expect(isValid).toBeTruthy();
    
    // Get all amounts and verify
    const amounts = await fundingPage.getAllFundingAmounts();
    expect(amounts.length).toBe(complexLines.length);
    
    TestUtils.logSuccess('✅ Funding calculations test passed');
  });

  test('CBAPS workflow - dashboard metrics verification', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Dashboard metrics and search functionality');
    
    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);
    
    const dashboard = await portal.openCBAPS();
    
    // Get initial metrics
    const initialMetrics = await dashboard.getDashboardMetrics();
    TestUtils.logInfo('Initial dashboard metrics:', JSON.stringify(initialMetrics));
    
    // Validate metrics structure
    expect(initialMetrics).toHaveProperty('totalRequisitions');
    expect(initialMetrics).toHaveProperty('pendingApprovals');
    expect(initialMetrics).toHaveProperty('completedToday');
    expect(initialMetrics).toHaveProperty('budgetUtilization');
    
    // Test search functionality
    await dashboard.searchRequisition('Test');
    await TestUtils.waitFor(1000, 'Waiting for search results');
    
    // Get recent requisitions count
    const recentCount = await dashboard.getRecentRequisitionsCount();
    TestUtils.logInfo(`Recent requisitions count: ${recentCount}`);
    
    // Check notifications
    const hasNotifications = await dashboard.hasPendingNotifications();
    TestUtils.logInfo(`Has pending notifications: ${hasNotifications}`);
    
    if (hasNotifications) {
      const notificationCount = await dashboard.getNotificationCount();
      TestUtils.logInfo(`Notification count: ${notificationCount}`);
    }
    
    TestUtils.logSuccess('✅ Dashboard metrics test passed');
  });
});
