/**
 * StatusTrackerPage: Final validation page with comprehensive status tracking
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { RequisitionStatus, WorkflowResult } from '../library/types';

export class StatusTrackerPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  // Locators
  readonly statusBadge: Locator;
  readonly requisitionIdLabel: Locator;
  readonly timestampLabel: Locator;
  readonly approvalHistoryPanel: Locator;
  readonly nextActionsPanel: Locator;
  readonly backToRequisitionLink: Locator;
  readonly printRequisitionButton: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    // Initialize locators
    this.statusBadge = page.locator('#reqStatus');
    this.requisitionIdLabel = page.locator('#requisitionId');
    this.timestampLabel = page.locator('#statusTimestamp');
    this.approvalHistoryPanel = page.locator('#approval-history');
    this.nextActionsPanel = page.locator('#next-actions');
    this.backToRequisitionLink = page.locator("a:has-text('Back to Requisition')");
    this.printRequisitionButton = page.locator("button:has-text('Print')");

    // Stability anchor
    this.pwManager.waitVisible('#reqStatus', 'Status page loaded');
    console.log('✓ Status Tracker Page initialized');
  }

  /**
   * Get current requisition status
   */
  async getStatus(): Promise<string> {
    const status = await this.pwManager.getText(this.statusBadge);
    console.log(`✓ Current status: ${status}`);
    return status;
  }

  /**
   * Get requisition ID
   */
  async getRequisitionId(): Promise<string> {
    if (await this.pwManager.isVisible(this.requisitionIdLabel)) {
      return await this.pwManager.getText(this.requisitionIdLabel);
    }
    return '';
  }

  /**
   * Validate status matches expected
   */
  async validateStatus(expectedStatus: RequisitionStatus | string): Promise<boolean> {
    const actualStatus = await this.getStatus();
    const isValid = actualStatus === expectedStatus;

    if (isValid) {
      console.log(`✅ Status validation passed: ${expectedStatus}`);
    } else {
      console.error(`❌ Status mismatch: Expected "${expectedStatus}", got "${actualStatus}"`);
    }

    return isValid;
  }

  /**
   * Get workflow result with all details
   */
  async getWorkflowResult(): Promise<WorkflowResult> {
    const result: WorkflowResult = {
      status: await this.getStatus(),
      timestamp: new Date(),
      requisitionId: await this.getRequisitionId()
    };

    console.log('✓ Workflow result retrieved:', result);
    return result;
  }

  /**
   * Check if approval history is visible
   */
  async hasApprovalHistory(): Promise<boolean> {
    return await this.pwManager.isVisible(this.approvalHistoryPanel);
  }

  /**
   * Get approval history count
   */
  async getApprovalHistoryCount(): Promise<number> {
    if (await this.hasApprovalHistory()) {
      const items = this.approvalHistoryPanel.locator('.history-item');
      return await items.count();
    }
    return 0;
  }

  /**
   * Print requisition
   */
  async printRequisition(): Promise<void> {
    if (await this.pwManager.isVisible(this.printRequisitionButton)) {
      await this.pwManager.click(this.printRequisitionButton);
      console.log('✓ Print dialog opened');
    }
  }
}
