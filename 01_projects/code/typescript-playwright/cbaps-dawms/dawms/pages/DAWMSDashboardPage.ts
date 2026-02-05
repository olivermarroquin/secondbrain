/**
 * DAWMSDashboardPage: Main DAWMS dashboard with metrics
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { SubmissionIntakePage } from './SubmissionIntakePage';

export interface DashboardMetrics {
  totalSubmissions: number;
  pendingReviews: number;
  completedToday: number;
  activeReviewers: number;
}

export class DAWMSDashboardPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  readonly submissionIntakeBtn: Locator;
  readonly searchSubmissionInput: Locator;
  readonly totalSubmissionsCard: Locator;
  readonly pendingReviewsCard: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    this.submissionIntakeBtn = page.locator("button:has-text('Submission Intake')");
    this.searchSubmissionInput = page.locator('#search-submissions');
    this.totalSubmissionsCard = page.locator('[data-metric="total-submissions"]');
    this.pendingReviewsCard = page.locator('[data-metric="pending-reviews"]');

    this.pwManager.waitVisible('text=DAWMS Dashboard', 'DAWMS Dashboard loaded');
    console.log('✓ DAWMS Dashboard Page initialized');
  }

  async goToSubmissionIntake(): Promise<SubmissionIntakePage> {
    await this.pwManager.click(this.submissionIntakeBtn);
    console.log('✓ Navigating to Submission Intake');
    return new SubmissionIntakePage(this.page, this.pwManager);
  }

  async getDashboardMetrics(): Promise<DashboardMetrics> {
    const metrics: DashboardMetrics = {
      totalSubmissions: 0,
      pendingReviews: 0,
      completedToday: 0,
      activeReviewers: 0
    };

    try {
      if (await this.pwManager.isVisible(this.totalSubmissionsCard)) {
        const text = await this.pwManager.getText(this.totalSubmissionsCard.locator('.metric-value'));
        metrics.totalSubmissions = parseInt(text) || 0;
      }

      if (await this.pwManager.isVisible(this.pendingReviewsCard)) {
        const text = await this.pwManager.getText(this.pendingReviewsCard.locator('.metric-value'));
        metrics.pendingReviews = parseInt(text) || 0;
      }

      console.log('✓ Dashboard metrics retrieved:', metrics);
    } catch (error) {
      console.warn('⚠️  Could not retrieve all metrics');
    }

    return metrics;
  }

  async validateDashboardLoaded(): Promise<boolean> {
    return await this.pwManager.isVisible(this.submissionIntakeBtn);
  }

  async searchSubmission(query: string): Promise<void> {
    if (await this.pwManager.isVisible(this.searchSubmissionInput)) {
      await this.pwManager.type(this.searchSubmissionInput, query);
      await this.pwManager.pressKey(this.searchSubmissionInput, 'Enter');
      console.log(`✓ Searched for: "${query}"`);
    }
  }
}
