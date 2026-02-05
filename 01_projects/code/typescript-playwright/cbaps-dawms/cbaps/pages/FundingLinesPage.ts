/**
 * FundingLinesPage: Enhanced funding lines management
 * Supports multiple funding lines with validation and calculations
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { FundingLineData } from '../library/types';
import { RoutingApprovalPage } from './RoutingApprovalPage';

export class FundingLinesPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  // Locators
  readonly addLineButton: Locator;
  readonly amountInput: Locator;
  readonly fiscalYearDropdown: Locator;
  readonly categoryDropdown: Locator;
  readonly descriptionInput: Locator;
  readonly saveLineButton: Locator;
  readonly continueToRoutingButton: Locator;
  readonly fundingLinesTable: Locator;
  readonly totalAmountLabel: Locator;
  readonly lineCountLabel: Locator;
  readonly deleteLineButton: (index: number) => Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    // Initialize locators
    this.addLineButton = page.locator("button:has-text('Add Line')");
    this.amountInput = page.locator('#fundAmount');
    this.fiscalYearDropdown = page.locator('#fiscalYear');
    this.categoryDropdown = page.locator('#category');
    this.descriptionInput = page.locator('#lineDescription');
    this.saveLineButton = page.locator("button:has-text('Save')");
    this.continueToRoutingButton = page.locator("button:has-text('Continue to Routing')");
    this.fundingLinesTable = page.locator('#funding-lines-table');
    this.totalAmountLabel = page.locator('#totalAmount');
    this.lineCountLabel = page.locator('#lineCount');
    
    // Dynamic locator for delete buttons
    this.deleteLineButton = (index: number) => 
      page.locator(`#funding-lines-table tbody tr:nth-child(${index + 1}) button.delete-line`);

    // Stability anchor
    this.pwManager.waitVisible('text=Funding Lines', 'Funding Lines page loaded');
    console.log('✓ Funding Lines Page initialized');
  }

  /**
   * Add a funding line with comprehensive data
   */
  async addFundingLine(data: FundingLineData): Promise<this> {
    console.log('💰 Adding funding line:', data);

    // Click add line button
    await this.pwManager.click(this.addLineButton);

    // Enter amount
    await this.pwManager.type(this.amountInput, data.amount);

    // Select fiscal year if provided
    if (data.fiscalYear) {
      await this.pwManager.selectDropdown(this.fiscalYearDropdown, data.fiscalYear);
    }

    // Select category if provided
    if (data.category) {
      await this.pwManager.selectDropdown(this.categoryDropdown, data.category);
    }

    // Enter description if provided
    if (data.description) {
      await this.pwManager.type(this.descriptionInput, data.description);
    }

    // Save the line
    await this.pwManager.click(this.saveLineButton);
    console.log('✓ Funding line added successfully');

    // Wait for table to update
    await this.pwManager.wait(500);

    return this;
  }

  /**
   * Add multiple funding lines
   */
  async addMultipleFundingLines(fundingLines: FundingLineData[]): Promise<this> {
    console.log(`💰 Adding ${fundingLines.length} funding lines`);

    for (const line of fundingLines) {
      await this.addFundingLine(line);
    }

    console.log(`✓ Added ${fundingLines.length} funding lines successfully`);
    return this;
  }

  /**
   * Get total funding amount
   */
  async getTotalAmount(): Promise<number> {
    if (await this.pwManager.isVisible(this.totalAmountLabel)) {
      const text = await this.pwManager.getText(this.totalAmountLabel);
      // Remove currency symbols and commas, parse as float
      const amount = parseFloat(text.replace(/[$,]/g, ''));
      console.log(`✓ Total amount: $${amount}`);
      return amount;
    }
    return 0;
  }

  /**
   * Get number of funding lines
   */
  async getFundingLineCount(): Promise<number> {
    if (await this.pwManager.isVisible(this.fundingLinesTable)) {
      const count = await this.fundingLinesTable.locator('tbody tr').count();
      console.log(`✓ Funding line count: ${count}`);
      return count;
    }
    return 0;
  }

  /**
   * Validate total amount matches expected
   */
  async validateTotalAmount(expectedAmount: number, tolerance: number = 0.01): Promise<boolean> {
    const actualAmount = await this.getTotalAmount();
    const isValid = Math.abs(actualAmount - expectedAmount) <= tolerance;

    if (isValid) {
      console.log(`✅ Total amount validation passed: $${actualAmount}`);
    } else {
      console.error(`❌ Total amount mismatch: Expected $${expectedAmount}, got $${actualAmount}`);
    }

    return isValid;
  }

  /**
   * Validate funding line count
   */
  async validateLineCount(expectedCount: number): Promise<boolean> {
    const actualCount = await this.getFundingLineCount();
    const isValid = actualCount === expectedCount;

    if (isValid) {
      console.log(`✅ Line count validation passed: ${actualCount}`);
    } else {
      console.error(`❌ Line count mismatch: Expected ${expectedCount}, got ${actualCount}`);
    }

    return isValid;
  }

  /**
   * Delete a funding line by index
   */
  async deleteFundingLine(index: number): Promise<void> {
    const deleteButton = this.deleteLineButton(index);
    if (await this.pwManager.isVisible(deleteButton)) {
      await this.pwManager.click(deleteButton);
      console.log(`✓ Deleted funding line at index ${index}`);
      await this.pwManager.wait(500); // Wait for table to update
    }
  }

  /**
   * Get all funding line amounts
   */
  async getAllFundingAmounts(): Promise<number[]> {
    const amounts: number[] = [];
    const rows = this.fundingLinesTable.locator('tbody tr');
    const count = await rows.count();

    for (let i = 0; i < count; i++) {
      const amountCell = rows.nth(i).locator('.amount-cell');
      const text = await this.pwManager.getText(amountCell);
      const amount = parseFloat(text.replace(/[$,]/g, ''));
      amounts.push(amount);
    }

    console.log('✓ Retrieved all funding amounts:', amounts);
    return amounts;
  }

  /**
   * Calculate sum of all funding lines
   */
  async calculateTotalFromLines(): Promise<number> {
    const amounts = await this.getAllFundingAmounts();
    const total = amounts.reduce((sum, amount) => sum + amount, 0);
    console.log(`✓ Calculated total from lines: $${total}`);
    return total;
  }

  /**
   * Verify calculated total matches displayed total
   */
  async verifyTotalCalculation(): Promise<boolean> {
    const calculatedTotal = await this.calculateTotalFromLines();
    const displayedTotal = await this.getTotalAmount();
    const isValid = Math.abs(calculatedTotal - displayedTotal) <= 0.01;

    if (isValid) {
      console.log('✅ Total calculation verified');
    } else {
      console.error(`❌ Total mismatch: Calculated $${calculatedTotal}, Displayed $${displayedTotal}`);
    }

    return isValid;
  }

  /**
   * Check if can continue to routing
   */
  async canContinueToRouting(): Promise<boolean> {
    const isVisible = await this.pwManager.isVisible(this.continueToRoutingButton);
    const isEnabled = await this.pwManager.isEnabled(this.continueToRoutingButton);
    return isVisible && isEnabled;
  }

  /**
   * Continue to Routing/Approval step
   */
  async continueToRouting(): Promise<RoutingApprovalPage> {
    await this.pwManager.click(this.continueToRoutingButton);
    console.log('✓ Continuing to Routing/Approval');
    return new RoutingApprovalPage(this.page, this.pwManager);
  }

  /**
   * Wait for funding lines table to be ready
   */
  async waitForTableReady(): Promise<void> {
    await this.pwManager.waitVisible('#funding-lines-table');
    await this.pwManager.wait(500);
    console.log('✓ Funding lines table ready');
  }
}
