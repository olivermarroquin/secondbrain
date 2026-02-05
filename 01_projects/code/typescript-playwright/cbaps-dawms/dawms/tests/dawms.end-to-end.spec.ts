/**
 * DAWMS End-to-End Tests: Comprehensive drug submission workflow testing
 * Tests complete DAWMS workflows with validation, error handling, and multiple scenarios
 */

import { test, expect, TestUtils } from '../library/BaseTest';
import { PortalHomePage } from '../pages/PortalHomePage';
import { SubmissionData, SubmissionStatus, SubmissionType, MilestoneType, ReviewerData } from '../library/types';

test.describe('DAWMS End-to-End Workflow Tests', () => {
  const PORTAL_URL = 'https://dawms-portal.example.com';

  test.beforeEach(async ({ testPage, pwManager }) => {
    TestUtils.logInfo('Starting new DAWMS test');
  });

  test('Complete DAWMS workflow: Intake → Reviewer Assignment → Signature → Milestone', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Step 1: Navigate to Portal and validate');

    // Initialize portal page
    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);

    // Validate portal
    const isPortalValid = await portal.validatePortalLoaded();
    expect(isPortalValid).toBeTruthy();

    const title = await portal.getTitle();
    expect(title).toContain('Portal');
    TestUtils.logSuccess('Portal loaded and validated');

    // ====== Step 2: Navigate to DAWMS Dashboard ======
    TestUtils.logStep('Step 2: Open DAWMS Dashboard and validate');

    const dashboard = await portal.openDAWMS();
    const isDashboardValid = await dashboard.validateDashboardLoaded();
    expect(isDashboardValid).toBeTruthy();

    // Get dashboard metrics
    const metrics = await dashboard.getDashboardMetrics();
    TestUtils.logInfo(`Dashboard metrics - Total: ${metrics.totalSubmissions}, Pending: ${metrics.pendingReviews}`);
    TestUtils.logSuccess('Dashboard validated');

    // ====== Step 3: Create Submission Intake ======
    TestUtils.logStep('Step 3: Navigate to Submission Intake page');

    const intakePage = await dashboard.goToSubmissionIntake();

    TestUtils.logStep('Step 4: Create new submission with validation');

    const submissionData: SubmissionData = {
      submissionType: SubmissionType.NDA,
      applicationNumber: `NDA-${TestUtils.randomNumber(100000, 999999)}`,
      sponsorName: 'PharmaTech Inc.',
      drugName: `TestDrug-${TestUtils.randomString(6)}`,
      priority: 'Priority'
    };

    // Validate form before submission
    await intakePage.fillSubmissionForm(submissionData);
    const formValidation = await intakePage.validateForm();
    expect(formValidation.isValid).toBeTruthy();

    // Create submission
    const assignmentPage = await intakePage.createSubmission(submissionData);

    TestUtils.logSuccess('Submission intake created successfully');

    // ====== Step 5: Assign Reviewers ======
    TestUtils.logStep('Step 5: Assign multiple reviewers');

    const reviewers: ReviewerData[] = [
      { role: 'Clinical Reviewer', name: 'Dr. Jane Smith', specialty: 'Cardiology' },
      { role: 'Pharmacologist', name: 'Dr. John Doe', specialty: 'Pharmacology' },
      { role: 'Statistical Reviewer', name: 'Dr. Sarah Williams', specialty: 'Biostatistics' }
    ];

    await assignmentPage.assignMultipleReviewers(reviewers);

    // Validate reviewer count
    const reviewerCount = await assignmentPage.getReviewerCount();
    expect(reviewerCount).toBe(reviewers.length);
    TestUtils.logSuccess(`Assigned ${reviewerCount} reviewers`);

    // Verify can continue
    const canContinue = await assignmentPage.canContinueToSignature();
    expect(canContinue).toBeTruthy();

    // ====== Step 6: Route for Signature ======
    TestUtils.logStep('Step 6: Route submission for signature');

    const signaturePage = await assignmentPage.routeToSignatureStep();

    TestUtils.logStep('Step 7: Submit for signature approval');

    const signerComments = 'Urgent review required for innovative therapy';
    const milestoneStatusPage = await signaturePage.submitForSignature(
      'Division Director',
      signerComments,
      true // urgent
    );

    // ====== Step 8: Validate Milestone and Status ======
    TestUtils.logStep('Step 8: Validate workflow milestone and status');

    const finalStatus = await milestoneStatusPage.getStatus();
    expect(finalStatus).toBe(SubmissionStatus.PendingSignature);
    TestUtils.logSuccess(`Final status: ${finalStatus}`);

    const finalMilestone = await milestoneStatusPage.getMilestone();
    expect(finalMilestone).toBe(MilestoneType.SignatureRouting);
    TestUtils.logSuccess(`Final milestone: ${finalMilestone}`);

    // Get complete workflow result
    const workflowResult = await milestoneStatusPage.getWorkflowResult();
    expect(workflowResult.status).toBe(SubmissionStatus.PendingSignature);
    expect(workflowResult.milestone).toBe(MilestoneType.SignatureRouting);
    expect(workflowResult.submissionId).toBeTruthy();

    // Validate both status and milestone together
    const isWorkflowValid = await milestoneStatusPage.validateWorkflow(
      SubmissionStatus.PendingSignature,
      MilestoneType.SignatureRouting
    );
    expect(isWorkflowValid).toBeTruthy();

    TestUtils.logSuccess('✅ Complete DAWMS workflow test passed');
  });

  test('DAWMS workflow with single reviewer - simplified flow', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Single reviewer assignment workflow');

    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);

    const dashboard = await portal.openDAWMS();
    const intakePage = await dashboard.goToSubmissionIntake();

    // Create simple submission
    const submissionData: SubmissionData = {
      submissionType: SubmissionType.ANDA,
      applicationNumber: `ANDA-${TestUtils.randomNumber(100000, 999999)}`
    };

    const assignmentPage = await intakePage.createSubmission(submissionData);

    // Assign single reviewer
    await assignmentPage.assignReviewer({
      role: 'Clinical Reviewer',
      name: 'Dr. Emily Johnson'
    });

    // Validate
    const count = await assignmentPage.getReviewerCount();
    expect(count).toBe(1);

    // Route and verify
    const signaturePage = await assignmentPage.routeToSignatureStep();
    const statusPage = await signaturePage.submitForSignature('Center Director');

    const status = await statusPage.validateStatus(SubmissionStatus.PendingSignature);
    expect(status).toBeTruthy();

    TestUtils.logSuccess('✅ Single reviewer workflow test passed');
  });

  test('DAWMS workflow with draft save', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Save submission as draft');

    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);

    const dashboard = await portal.openDAWMS();
    const intakePage = await dashboard.goToSubmissionIntake();

    // Save as draft
    const draftData: SubmissionData = {
      submissionType: SubmissionType.BLA,
      applicationNumber: `BLA-${TestUtils.randomNumber(100000, 999999)}`,
      sponsorName: 'BioTech Solutions',
      drugName: 'TestBiologic'
    };

    await intakePage.saveAsDraft(draftData);

    // Validate draft status
    const status = await intakePage.getStatus();
    expect(status).toContain('Draft');

    const submissionId = await intakePage.getSubmissionId();
    expect(submissionId).toBeTruthy();

    TestUtils.logSuccess(`✅ Draft saved with ID: ${submissionId}`);
  });

  test('DAWMS workflow validation - form validation tests', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Submission form validation');

    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);

    const dashboard = await portal.openDAWMS();
    const intakePage = await dashboard.goToSubmissionIntake();

    // Test empty form validation
    const emptyValidation = await intakePage.validateForm();
    expect(emptyValidation.isValid).toBeFalsy();
    expect(emptyValidation.errors.length).toBeGreaterThan(0);
    TestUtils.logInfo(`Empty form errors: ${emptyValidation.errors.join(', ')}`);

    // Fill partial form
    await intakePage.fillSubmissionForm({
      submissionType: SubmissionType.IND,
      applicationNumber: 'IND-123456'
    });

    // Validate again
    const partialValidation = await intakePage.validateForm();
    expect(partialValidation.isValid).toBeTruthy();

    TestUtils.logSuccess('✅ Form validation test passed');
  });

  test('DAWMS workflow - multiple reviewer assignment validation', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Complex reviewer assignment workflow');

    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);

    const dashboard = await portal.openDAWMS();
    const intakePage = await dashboard.goToSubmissionIntake();

    // Create submission
    const submissionData = await intakePage.createSubmission({
      submissionType: SubmissionType.NDA,
      applicationNumber: `NDA-${TestUtils.randomNumber(100000, 999999)}`,
      priority: 'Fast Track'
    });

    // Assign multiple reviewers with different specialties
    const complexReviewers: ReviewerData[] = [
      { role: 'Clinical Reviewer', name: 'Dr. Michael Chen', specialty: 'Oncology' },
      { role: 'Pharmacologist', name: 'Dr. Lisa Anderson', specialty: 'Clinical Pharmacology' },
      { role: 'Statistical Reviewer', name: 'Dr. Robert Martinez', specialty: 'Statistics' },
      { role: 'Safety Reviewer', name: 'Dr. Patricia Davis', specialty: 'Safety' },
      { role: 'Quality Reviewer', name: 'Dr. James Wilson', specialty: 'Quality Assurance' }
    ];

    await submissionData.assignMultipleReviewers(complexReviewers);

    // Validate count
    await submissionData.validateReviewerCount(complexReviewers.length);

    const actualCount = await submissionData.getReviewerCount();
    expect(actualCount).toBe(complexReviewers.length);

    TestUtils.logSuccess(`✅ Assigned and validated ${actualCount} reviewers`);
  });

  test('DAWMS workflow - dashboard search functionality', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Dashboard search and metrics');

    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);

    const dashboard = await portal.openDAWMS();

    // Get and validate metrics
    const metrics = await dashboard.getDashboardMetrics();
    TestUtils.logInfo('Dashboard metrics:', JSON.stringify(metrics));

    expect(metrics).toHaveProperty('totalSubmissions');
    expect(metrics).toHaveProperty('pendingReviews');

    // Test search
    await dashboard.searchSubmission('NDA-123456');
    await TestUtils.waitFor(1000, 'Waiting for search results');

    TestUtils.logSuccess('✅ Dashboard search test passed');
  });

  test('DAWMS end-to-end with workflow validation at each step', async ({ testPage, pwManager }) => {
    TestUtils.logStep('Test: Comprehensive validation at each workflow step');

    const portal = new PortalHomePage(testPage, pwManager);
    await portal.navigateToPortal(PORTAL_URL);

    // Validate portal
    expect(await portal.validatePortalLoaded()).toBeTruthy();

    const dashboard = await portal.openDAWMS();

    // Validate dashboard
    expect(await dashboard.validateDashboardLoaded()).toBeTruthy();

    const intakePage = await dashboard.goToSubmissionIntake();

    // Create and validate submission
    const submissionData: SubmissionData = {
      submissionType: SubmissionType.NDA,
      applicationNumber: `NDA-${Date.now()}`,
      sponsorName: 'Validation Test Co.',
      drugName: 'ValidDrug'
    };

    await intakePage.fillSubmissionForm(submissionData);
    expect((await intakePage.validateForm()).isValid).toBeTruthy();

    const assignmentPage = await intakePage.createSubmission(submissionData);

    // Assign and validate reviewers
    await assignmentPage.assignReviewer({
      role: 'Clinical Reviewer',
      name: 'Dr. Validation Tester'
    });

    expect(await assignmentPage.getReviewerCount()).toBe(1);
    expect(await assignmentPage.canContinueToSignature()).toBeTruthy();

    // Route and validate signature
    const signaturePage = await assignmentPage.routeToSignatureStep();
    const statusPage = await signaturePage.submitForSignature('Division Director');

    // Final validation
    const workflowValid = await statusPage.validateWorkflow(
      SubmissionStatus.PendingSignature,
      MilestoneType.SignatureRouting
    );
    expect(workflowValid).toBeTruthy();

    TestUtils.logSuccess('✅ Step-by-step validation test passed');
  });
});
