/**
 * CBAPSDashboardPage: Enhanced CBAPS main dashboard with analytics methods
 * Provides navigation and dashboard data retrieval
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { RequisitionPage } from './RequisitionPage';

export interface DashboardMetrics {
  totalRequisitions: number;
  pendingApprovals: number;
  completedToday: number;
  budgetUtilization: string;
}

export class CBAPSDashboardPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  // Locators
  readonly createRequisitionBtn: Locator;
  readonly dashboardHeader: Locator;
  readonly searchRequisitionInput: Locator;
  readonly recentRequisitionsTable: Locator;
  readonly totalRequisitionsCard: Locator;
  readonly pendingApprovalsCard: Locator;
  readonly completedTodayCard: Locator;
  readonly budgetUtilizationCard: Locator;
  readonly quickActionsMenu: Locator;
  readonly notificationsPanel: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    // Initialize locators
    this.createRequisitionBtn = page.locator("button:has-text('Create Requisition')");
    this.dashboardHeader = page.locator('.dashboard-header');
    this.searchRequisitionInput = page.locator('#search-requisitions');
    this.recentRequisitionsTable = page.locator('#recent-requisitions-table');
    this.totalRequisitionsCard = page.locator('[data-metric="total-requisitions"]');
    this.pendingApprovalsCard = page.locator('[data-metric="pending-approvals"]');
    this.completedTodayCard = page.locator('[data-metric="completed-today"]');
    this.budgetUtilizationCard = page.locator('[data-metric="budget-utilization"]');
    this.quickActionsMenu = page.locator('#quick-actions');
    this.notificationsPanel = page.locator('#notifications-panel');

    // Stability anchor
    this.pwManager.waitVisible('text=CBAPS Dashboard', 'CBAPS Dashboard loaded');
    console.log('✓ CBAPS Dashboard Page initialized');
  }

  /**
   * Navigate to Create Requisition page
   */
  async goToCreateRequisition(): Promise<RequisitionPage> {
    await this.pwManager.click(this.createRequisitionBtn);
    console.log('✓ Navigating to Create Requisition page');
    return new RequisitionPage(this.page, this.pwManager);
  }

  /**
   * Get dashboard metrics
   */
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    const metrics: DashboardMetrics = {
      totalRequisitions: 0,
      pendingApprovals: 0,
      completedToday: 0,
      budgetUtilization: '0%'
    };

    try {
      if (await this.pwManager.isVisible(this.totalRequisitionsCard)) {
        const text = await this.pwManager.getText(this.totalRequisitionsCard.locator('.metric-value'));
        metrics.totalRequisitions = parseInt(text) || 0;
      }

      if (await this.pwManager.isVisible(this.pendingApprovalsCard)) {
        const text = await this.pwManager.getText(this.pendingApprovalsCard.locator('.metric-value'));
        metrics.pendingApprovals = parseInt(text) || 0;
      }

      if (await this.pwManager.isVisible(this.completedTodayCard)) {
        const text = await this.pwManager.getText(this.completedTodayCard.locator('.metric-value'));
        metrics.completedToday = parseInt(text) || 0;
      }

      if (await this.pwManager.isVisible(this.budgetUtilizationCard)) {
        metrics.budgetUtilization = await this.pwManager.getText(
          this.budgetUtilizationCard.locator('.metric-value')
        );
      }

      console.log('✓ Dashboard metrics retrieved:', metrics);
    } catch (error) {
      console.warn('⚠️  Could not retrieve all dashboard metrics');
    }

    return metrics;
  }

  /**
   * Search for requisition by ID or title
   */
  async searchRequisition(query: string): Promise<void> {
    if (await this.pwManager.isVisible(this.searchRequisitionInput)) {
      await this.pwManager.type(this.searchRequisitionInput, query);
      await this.pwManager.pressKey(this.searchRequisitionInput, 'Enter');
      console.log(`✓ Searched for requisition: "${query}"`);
      await this.pwManager.wait(1000); // Wait for results
    }
  }

  /**
   * Get count of recent requisitions
   */
  async getRecentRequisitionsCount(): Promise<number> {
    if (await this.pwManager.isVisible(this.recentRequisitionsTable)) {
      const rows = await this.recentRequisitionsTable.locator('tbody tr').count();
      console.log(`✓ Found ${rows} recent requisitions`);
      return rows;
    }
    return 0;
  }

  /**
   * Validate dashboard is loaded correctly
   */
  async validateDashboardLoaded(): Promise<boolean> {
    const isHeaderVisible = await this.pwManager.isVisible(this.dashboardHeader);
    const isCreateBtnVisible = await this.pwManager.isVisible(this.createRequisitionBtn);

    const isValid = isHeaderVisible && isCreateBtnVisible;
    
    if (isValid) {
      console.log('✓ Dashboard validation passed');
    } else {
      console.warn('⚠️  Dashboard validation failed');
    }

    return isValid;
  }

  /**
   * Check if there are pending notifications
   */
  async hasPendingNotifications(): Promise<boolean> {
    if (await this.pwManager.isVisible(this.notificationsPanel)) {
      const badge = this.notificationsPanel.locator('.notification-badge');
      return await badge.isVisible();
    }
    return false;
  }

  /**
   * Get notification count
   */
  async getNotificationCount(): Promise<number> {
    if (await this.hasPendingNotifications()) {
      const badge = this.notificationsPanel.locator('.notification-badge');
      const text = await this.pwManager.getText(badge);
      return parseInt(text) || 0;
    }
    return 0;
  }

  /**
   * Wait for dashboard to fully load
   */
  async waitForDashboardReady(): Promise<void> {
    await this.pwManager.waitVisible('text=CBAPS Dashboard');
    await this.pwManager.wait(1000); // Wait for metrics to load
    console.log('✓ Dashboard is ready');
  }
}
