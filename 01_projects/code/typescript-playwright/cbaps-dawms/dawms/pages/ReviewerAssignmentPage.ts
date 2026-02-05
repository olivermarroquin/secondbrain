/**
 * ReviewerAssignmentPage: Assign reviewers to drug submissions
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { ReviewerData } from '../library/types';
import { SignatureRoutingPage } from './SignatureRoutingPage';

export class ReviewerAssignmentPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  readonly reviewerRoleDropdown: Locator;
  readonly reviewerNameInput: Locator;
  readonly specialtyDropdown: Locator;
  readonly assignReviewerButton: Locator;
  readonly continueToSignatureButton: Locator;
  readonly reviewersTable: Locator;
  readonly reviewerCountLabel: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    this.reviewerRoleDropdown = page.locator('#reviewerRole');
    this.reviewerNameInput = page.locator('#reviewerName');
    this.specialtyDropdown = page.locator('#specialty');
    this.assignReviewerButton = page.locator("button:has-text('Assign')");
    this.continueToSignatureButton = page.locator("button:has-text('Route to Signature')");
    this.reviewersTable = page.locator('#reviewers-table');
    this.reviewerCountLabel = page.locator('#reviewerCount');

    this.pwManager.waitVisible('text=Reviewer Assignment', 'Reviewer Assignment page loaded');
    console.log('✓ Reviewer Assignment Page initialized');
  }

  async assignReviewer(data: ReviewerData): Promise<this> {
    console.log('👤 Assigning reviewer:', data);

    await this.pwManager.selectDropdown(this.reviewerRoleDropdown, data.role);
    await this.pwManager.type(this.reviewerNameInput, data.name);

    if (data.specialty) {
      await this.pwManager.selectDropdown(this.specialtyDropdown, data.specialty);
    }

    await this.pwManager.click(this.assignReviewerButton);
    console.log('✓ Reviewer assigned successfully');

    await this.pwManager.wait(500);
    return this;
  }

  async assignMultipleReviewers(reviewers: ReviewerData[]): Promise<this> {
    console.log(`👥 Assigning ${reviewers.length} reviewers`);

    for (const reviewer of reviewers) {
      await this.assignReviewer(reviewer);
    }

    console.log(`✓ Assigned ${reviewers.length} reviewers`);
    return this;
  }

  async getReviewerCount(): Promise<number> {
    if (await this.pwManager.isVisible(this.reviewersTable)) {
      const count = await this.reviewersTable.locator('tbody tr').count();
      console.log(`✓ Reviewer count: ${count}`);
      return count;
    }
    return 0;
  }

  async validateReviewerCount(expectedCount: number): Promise<boolean> {
    const actualCount = await this.getReviewerCount();
    const isValid = actualCount === expectedCount;

    if (isValid) {
      console.log(`✅ Reviewer count validation passed: ${actualCount}`);
    } else {
      console.error(`❌ Reviewer count mismatch: Expected ${expectedCount}, got ${actualCount}`);
    }

    return isValid;
  }

  async routeToSignatureStep(): Promise<SignatureRoutingPage> {
    await this.pwManager.click(this.continueToSignatureButton);
    console.log('✓ Routing to signature step');
    return new SignatureRoutingPage(this.page, this.pwManager);
  }

  async canContinueToSignature(): Promise<boolean> {
    return await this.pwManager.isVisible(this.continueToSignatureButton) &&
           await this.pwManager.isEnabled(this.continueToSignatureButton);
  }
}

/**
 * SignatureRoutingPage: Route submission for signature approval
 */

export class SignatureRoutingPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  readonly signerDropdown: Locator;
  readonly routeForSignatureButton: Locator;
  readonly commentsTextarea: Locator;
  readonly urgencyCheckbox: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    this.signerDropdown = page.locator('#signer');
    this.routeForSignatureButton = page.locator("button:has-text('Submit for Signature')");
    this.commentsTextarea = page.locator('#signatureComments');
    this.urgencyCheckbox = page.locator('#urgentSignature');

    this.pwManager.waitVisible('text=Signature Routing', 'Signature Routing page loaded');
    console.log('✓ Signature Routing Page initialized');
  }

  async submitForSignature(signer: string, comments?: string, urgent: boolean = false): Promise<any> {
    console.log(`✍️  Submitting for signature to: ${signer}`);

    await this.pwManager.selectDropdown(this.signerDropdown, signer);

    if (comments) {
      await this.pwManager.type(this.commentsTextarea, comments);
    }

    if (urgent) {
      if (await this.pwManager.isVisible(this.urgencyCheckbox)) {
        await this.pwManager.click(this.urgencyCheckbox);
      }
    }

    await this.pwManager.click(this.routeForSignatureButton);
    console.log('✓ Routing submitted successfully');

    // Return MilestoneStatusPage (import at top if needed)
    const { MilestoneStatusPage } = await import('./MilestoneStatusPage');
    return new MilestoneStatusPage(this.page, this.pwManager);
  }
}
