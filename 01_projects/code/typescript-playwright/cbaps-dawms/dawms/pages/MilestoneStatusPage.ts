/**
 * MilestoneStatusPage: Final milestone and status tracking
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { SubmissionStatus, MilestoneType, WorkflowResult } from '../library/types';

export class MilestoneStatusPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  readonly milestoneLabel: Locator;
  readonly statusLabel: Locator;
  readonly submissionIdLabel: Locator;
  readonly timestampLabel: Locator;
  readonly reviewHistoryPanel: Locator;
  readonly nextStepsPanel: Locator;
  readonly backToSubmissionLink: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    this.milestoneLabel = page.locator('#milestone');
    this.statusLabel = page.locator('#status');
    this.submissionIdLabel = page.locator('#submissionId');
    this.timestampLabel = page.locator('#statusTimestamp');
    this.reviewHistoryPanel = page.locator('#review-history');
    this.nextStepsPanel = page.locator('#next-steps');
    this.backToSubmissionLink = page.locator("a:has-text('Back to Submission')");

    this.pwManager.waitVisible('#status', 'Status page loaded');
    console.log('✓ Milestone Status Page initialized');
  }

  async getMilestone(): Promise<string> {
    const milestone = await this.pwManager.getText(this.milestoneLabel);
    console.log(`✓ Current milestone: ${milestone}`);
    return milestone;
  }

  async getStatus(): Promise<string> {
    const status = await this.pwManager.getText(this.statusLabel);
    console.log(`✓ Current status: ${status}`);
    return status;
  }

  async getSubmissionId(): Promise<string> {
    if (await this.pwManager.isVisible(this.submissionIdLabel)) {
      return await this.pwManager.getText(this.submissionIdLabel);
    }
    return '';
  }

  async validateStatus(expectedStatus: SubmissionStatus | string): Promise<boolean> {
    const actualStatus = await this.getStatus();
    const isValid = actualStatus === expectedStatus;

    if (isValid) {
      console.log(`✅ Status validation passed: ${expectedStatus}`);
    } else {
      console.error(`❌ Status mismatch: Expected "${expectedStatus}", got "${actualStatus}"`);
    }

    return isValid;
  }

  async validateMilestone(expectedMilestone: MilestoneType | string): Promise<boolean> {
    const actualMilestone = await this.getMilestone();
    const isValid = actualMilestone === expectedMilestone;

    if (isValid) {
      console.log(`✅ Milestone validation passed: ${expectedMilestone}`);
    } else {
      console.error(`❌ Milestone mismatch: Expected "${expectedMilestone}", got "${actualMilestone}"`);
    }

    return isValid;
  }

  async getWorkflowResult(): Promise<WorkflowResult> {
    const result: WorkflowResult = {
      status: await this.getStatus(),
      milestone: await this.getMilestone(),
      timestamp: new Date(),
      submissionId: await this.getSubmissionId()
    };

    console.log('✓ Workflow result retrieved:', result);
    return result;
  }

  async hasReviewHistory(): Promise<boolean> {
    return await this.pwManager.isVisible(this.reviewHistoryPanel);
  }

  async getReviewHistoryCount(): Promise<number> {
    if (await this.hasReviewHistory()) {
      const items = this.reviewHistoryPanel.locator('.history-item');
      return await items.count();
    }
    return 0;
  }

  async validateWorkflow(expectedStatus: string, expectedMilestone: string): Promise<boolean> {
    const statusValid = await this.validateStatus(expectedStatus);
    const milestoneValid = await this.validateMilestone(expectedMilestone);

    return statusValid && milestoneValid;
  }
}
