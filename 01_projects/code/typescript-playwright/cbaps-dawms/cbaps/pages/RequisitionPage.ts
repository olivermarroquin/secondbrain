/**
 * RequisitionPage: Comprehensive requisition creation and management
 * Enhanced with validation, getters, and utility methods
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { RequisitionData, RequisitionStatus, FundType, ValidationResult } from '../library/types';
import { FundingLinesPage } from './FundingLinesPage';
import { RoutingApprovalPage } from './RoutingApprovalPage';

export class RequisitionPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  // Form Locators
  readonly titleInput: Locator;
  readonly descriptionTextarea: Locator;
  readonly fundTypeDropdown: Locator;
  readonly priorityDropdown: Locator;
  readonly submitButton: Locator;
  readonly saveAsDraftButton: Locator;
  readonly cancelButton: Locator;

  // Status and Navigation Locators
  readonly statusBadge: Locator;
  readonly requisitionIdLabel: Locator;
  readonly goToFundingLink: Locator;
  readonly routeForApprovalButton: Locator;
  readonly editButton: Locator;
  readonly deleteButton: Locator;

  // Validation Locators
  readonly titleError: Locator;
  readonly fundTypeError: Locator;
  readonly formErrorsPanel: Locator;
  readonly successMessage: Locator;

  // Info Locators
  readonly createdByLabel: Locator;
  readonly createdDateLabel: Locator;
  readonly lastModifiedLabel: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    // Initialize form locators
    this.titleInput = page.locator('#requisitionTitle');
    this.descriptionTextarea = page.locator('#requisitionDescription');
    this.fundTypeDropdown = page.locator('#fundType');
    this.priorityDropdown = page.locator('#priority');
    this.submitButton = page.locator("button:has-text('Submit')");
    this.saveAsDraftButton = page.locator("button:has-text('Save as Draft')");
    this.cancelButton = page.locator("button:has-text('Cancel')");

    // Initialize status and navigation locators
    this.statusBadge = page.locator('#reqStatus');
    this.requisitionIdLabel = page.locator('#requisitionId');
    this.goToFundingLink = page.locator("a:has-text('Funding Lines')");
    this.routeForApprovalButton = page.locator("button:has-text('Route for Approval')");
    this.editButton = page.locator("button:has-text('Edit')");
    this.deleteButton = page.locator("button:has-text('Delete')");

    // Initialize validation locators
    this.titleError = page.locator('#titleError');
    this.fundTypeError = page.locator('#fundTypeError');
    this.formErrorsPanel = page.locator('.form-errors');
    this.successMessage = page.locator('.success-message');

    // Initialize info locators
    this.createdByLabel = page.locator('#createdBy');
    this.createdDateLabel = page.locator('#createdDate');
    this.lastModifiedLabel = page.locator('#lastModified');

    // Stability anchor
    this.pwManager.waitVisible('#requisitionTitle', 'Requisition page loaded');
    console.log('✓ Requisition Page initialized');
  }

  /**
   * Create a new requisition with comprehensive data
   */
  async createRequisition(data: RequisitionData): Promise<void> {
    console.log('📝 Creating requisition with data:', data);

    // Enter title
    await this.pwManager.type(this.titleInput, data.title);

    // Enter description if provided
    if (data.description) {
      await this.pwManager.type(this.descriptionTextarea, data.description);
    }

    // Select fund type
    await this.pwManager.selectDropdown(this.fundTypeDropdown, data.fundType);

    // Select priority if provided
    if (data.priority) {
      await this.pwManager.selectDropdown(this.priorityDropdown, data.priority);
    }

    // Submit the form
    await this.pwManager.click(this.submitButton);
    console.log('✓ Requisition created successfully');

    // Wait for success message
    await this.waitForSuccessMessage();
  }

  /**
   * Fill requisition form without submitting
   */
  async fillRequisitionForm(data: RequisitionData): Promise<void> {
    await this.pwManager.type(this.titleInput, data.title);
    
    if (data.description) {
      await this.pwManager.type(this.descriptionTextarea, data.description);
    }
    
    await this.pwManager.selectDropdown(this.fundTypeDropdown, data.fundType);
    
    if (data.priority) {
      await this.pwManager.selectDropdown(this.priorityDropdown, data.priority);
    }

    console.log('✓ Requisition form filled');
  }

  /**
   * Save requisition as draft
   */
  async saveAsDraft(data: RequisitionData): Promise<void> {
    await this.fillRequisitionForm(data);
    await this.pwManager.click(this.saveAsDraftButton);
    console.log('✓ Requisition saved as draft');
    await this.waitForSuccessMessage();
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
  async validateStatus(expectedStatus: RequisitionStatus): Promise<boolean> {
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
   * Navigate to Funding Lines page
   */
  async goToFundingLines(): Promise<FundingLinesPage> {
    await this.pwManager.click(this.goToFundingLink);
    console.log('✓ Navigating to Funding Lines page');
    return new FundingLinesPage(this.page, this.pwManager);
  }

  /**
   * Route requisition for approval
   */
  async routeForApproval(): Promise<RoutingApprovalPage> {
    await this.pwManager.click(this.routeForApprovalButton);
    console.log('✓ Routing requisition for approval');
    return new RoutingApprovalPage(this.page, this.pwManager);
  }

  /**
   * Validate form before submission
   */
  async validateForm(): Promise<ValidationResult> {
    const errors: string[] = [];

    // Check title
    const title = await this.titleInput.inputValue();
    if (!title || title.trim().length === 0) {
      errors.push('Title is required');
    }

    // Check fund type
    const fundType = await this.fundTypeDropdown.inputValue();
    if (!fundType) {
      errors.push('Fund type is required');
    }

    // Check for displayed validation errors
    if (await this.pwManager.isVisible(this.titleError)) {
      const errorText = await this.pwManager.getText(this.titleError);
      errors.push(`Title error: ${errorText}`);
    }

    if (await this.pwManager.isVisible(this.fundTypeError)) {
      const errorText = await this.pwManager.getText(this.fundTypeError);
      errors.push(`Fund type error: ${errorText}`);
    }

    const result: ValidationResult = {
      isValid: errors.length === 0,
      errors
    };

    if (result.isValid) {
      console.log('✅ Form validation passed');
    } else {
      console.warn('⚠️  Form validation failed:', errors);
    }

    return result;
  }

  /**
   * Check if edit button is visible/enabled
   */
  async canEdit(): Promise<boolean> {
    return await this.pwManager.isVisible(this.editButton) && 
           await this.pwManager.isEnabled(this.editButton);
  }

  /**
   * Check if delete button is visible/enabled
   */
  async canDelete(): Promise<boolean> {
    return await this.pwManager.isVisible(this.deleteButton) && 
           await this.pwManager.isEnabled(this.deleteButton);
  }

  /**
   * Get requisition metadata
   */
  async getRequisitionMetadata(): Promise<{
    id: string;
    status: string;
    createdBy?: string;
    createdDate?: string;
    lastModified?: string;
  }> {
    const metadata: any = {
      id: await this.getRequisitionId(),
      status: await this.getStatus()
    };

    if (await this.pwManager.isVisible(this.createdByLabel)) {
      metadata.createdBy = await this.pwManager.getText(this.createdByLabel);
    }

    if (await this.pwManager.isVisible(this.createdDateLabel)) {
      metadata.createdDate = await this.pwManager.getText(this.createdDateLabel);
    }

    if (await this.pwManager.isVisible(this.lastModifiedLabel)) {
      metadata.lastModified = await this.pwManager.getText(this.lastModifiedLabel);
    }

    console.log('✓ Requisition metadata retrieved:', metadata);
    return metadata;
  }

  /**
   * Wait for success message to appear
   */
  private async waitForSuccessMessage(timeout: number = 10000): Promise<void> {
    try {
      await this.page.waitForSelector('.success-message', { state: 'visible', timeout });
      console.log('✓ Success message displayed');
    } catch {
      console.warn('⚠️  Success message did not appear');
    }
  }

  /**
   * Clear form
   */
  async clearForm(): Promise<void> {
    await this.titleInput.clear();
    await this.descriptionTextarea.clear();
    console.log('✓ Form cleared');
  }

  /**
   * Cancel requisition creation
   */
  async cancel(): Promise<void> {
    await this.pwManager.click(this.cancelButton);
    console.log('✓ Requisition creation cancelled');
  }

  /**
   * Check if routing button is available
   */
  async isRoutingAvailable(): Promise<boolean> {
    return await this.pwManager.isVisible(this.routeForApprovalButton) &&
           await this.pwManager.isEnabled(this.routeForApprovalButton);
  }

  /**
   * Check if funding link is available
   */
  async isFundingAvailable(): Promise<boolean> {
    return await this.pwManager.isVisible(this.goToFundingLink);
  }
}
