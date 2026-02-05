/**
 * SubmissionIntakePage: Drug submission intake with validation
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { SubmissionData, ValidationResult, SubmissionType } from '../library/types';
import { ReviewerAssignmentPage } from './ReviewerAssignmentPage';

export class SubmissionIntakePage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  readonly submissionTypeDropdown: Locator;
  readonly applicationNumberInput: Locator;
  readonly sponsorNameInput: Locator;
  readonly drugNameInput: Locator;
  readonly priorityDropdown: Locator;
  readonly createSubmissionButton: Locator;
  readonly saveAsDraftButton: Locator;
  readonly submissionIdLabel: Locator;
  readonly statusBadge: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    this.submissionTypeDropdown = page.locator('#submissionType');
    this.applicationNumberInput = page.locator('#applicationNumber');
    this.sponsorNameInput = page.locator('#sponsorName');
    this.drugNameInput = page.locator('#drugName');
    this.priorityDropdown = page.locator('#priority');
    this.createSubmissionButton = page.locator("button:has-text('Create Submission')");
    this.saveAsDraftButton = page.locator("button:has-text('Save as Draft')");
    this.submissionIdLabel = page.locator('#submissionId');
    this.statusBadge = page.locator('#submissionStatus');

    this.pwManager.waitVisible('#submissionType', 'Submission Intake page loaded');
    console.log('✓ Submission Intake Page initialized');
  }

  async createSubmission(data: SubmissionData): Promise<ReviewerAssignmentPage> {
    console.log('📝 Creating submission with data:', data);

    await this.pwManager.selectDropdown(this.submissionTypeDropdown, data.submissionType);
    await this.pwManager.type(this.applicationNumberInput, data.applicationNumber);

    if (data.sponsorName) {
      await this.pwManager.type(this.sponsorNameInput, data.sponsorName);
    }

    if (data.drugName) {
      await this.pwManager.type(this.drugNameInput, data.drugName);
    }

    if (data.priority) {
      await this.pwManager.selectDropdown(this.priorityDropdown, data.priority);
    }

    await this.pwManager.click(this.createSubmissionButton);
    console.log('✓ Submission created successfully');

    return new ReviewerAssignmentPage(this.page, this.pwManager);
  }

  async fillSubmissionForm(data: SubmissionData): Promise<void> {
    await this.pwManager.selectDropdown(this.submissionTypeDropdown, data.submissionType);
    await this.pwManager.type(this.applicationNumberInput, data.applicationNumber);

    if (data.sponsorName) {
      await this.pwManager.type(this.sponsorNameInput, data.sponsorName);
    }

    if (data.drugName) {
      await this.pwManager.type(this.drugNameInput, data.drugName);
    }

    console.log('✓ Submission form filled');
  }

  async validateForm(): Promise<ValidationResult> {
    const errors: string[] = [];

    const submissionType = await this.submissionTypeDropdown.inputValue();
    if (!submissionType) {
      errors.push('Submission type is required');
    }

    const appNumber = await this.applicationNumberInput.inputValue();
    if (!appNumber || appNumber.trim().length === 0) {
      errors.push('Application number is required');
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

  async getSubmissionId(): Promise<string> {
    if (await this.pwManager.isVisible(this.submissionIdLabel)) {
      return await this.pwManager.getText(this.submissionIdLabel);
    }
    return '';
  }

  async getStatus(): Promise<string> {
    if (await this.pwManager.isVisible(this.statusBadge)) {
      return await this.pwManager.getText(this.statusBadge);
    }
    return '';
  }

  async saveAsDraft(data: SubmissionData): Promise<void> {
    await this.fillSubmissionForm(data);
    await this.pwManager.click(this.saveAsDraftButton);
    console.log('✓ Submission saved as draft');
  }
}
