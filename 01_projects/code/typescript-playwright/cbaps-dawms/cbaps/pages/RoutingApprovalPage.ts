/**
 * RoutingApprovalPage: Enhanced approval routing with multi-level approvals
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { ApproverData } from '../library/types';
import { StatusTrackerPage } from './StatusTrackerPage';

export class RoutingApprovalPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  // Locators
  readonly selectApproverDropdown: Locator;
  readonly approverLevelDropdown: Locator;
  readonly commentsTextarea: Locator;
  readonly submitRoutingButton: Locator;
  readonly addApproverButton: Locator;
  readonly approvalChainList: Locator;
  readonly estimatedApprovalTime: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    // Initialize locators
    this.selectApproverDropdown = page.locator('#approver');
    this.approverLevelDropdown = page.locator('#approverLevel');
    this.commentsTextarea = page.locator('#routingComments');
    this.submitRoutingButton = page.locator("button:has-text('Submit Routing')");
    this.addApproverButton = page.locator("button:has-text('Add Approver')");
    this.approvalChainList = page.locator('#approval-chain');
    this.estimatedApprovalTime = page.locator('#estimatedTime');

    // Stability anchor
    this.pwManager.waitVisible('text=Routing', 'Routing page loaded');
    console.log('✓ Routing Approval Page initialized');
  }

  /**
   * Submit for approval with approver and optional comments
   */
  async submitForApproval(
    approver: string,
    comments?: string
  ): Promise<StatusTrackerPage> {
    console.log(`📤 Submitting for approval to: ${approver}`);

    // Select approver
    await this.pwManager.selectDropdown(this.selectApproverDropdown, approver);

    // Add comments if provided
    if (comments) {
      await this.pwManager.type(this.commentsTextarea, comments);
    }

    // Submit
    await this.pwManager.click(this.submitRoutingButton);
    console.log('✓ Routing submitted successfully');

    return new StatusTrackerPage(this.page, this.pwManager);
  }

  /**
   * Get estimated approval time
   */
  async getEstimatedApprovalTime(): Promise<string> {
    if (await this.pwManager.isVisible(this.estimatedApprovalTime)) {
      return await this.pwManager.getText(this.estimatedApprovalTime);
    }
    return '';
  }

  /**
   * Validate approver is selected
   */
  async validateApproverSelected(): Promise<boolean> {
    const value = await this.selectApproverDropdown.inputValue();
    return value !== '' && value !== null;
  }
}
