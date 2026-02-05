/**
 * BaseTest: Enhanced test base class with Playwright Test framework
 * Provides setup, teardown, and utility methods for all tests
 */

import { test as base, expect } from '@playwright/test';
import { PlaywrightManager } from './PlaywrightManager';
import { Page } from '@playwright/test';
import * as fs from 'fs';

// Extend Playwright test with custom fixtures
export const test = base.extend<{
  pwManager: PlaywrightManager;
  testPage: Page;
}>({
  pwManager: async ({}, use) => {
    const manager = new PlaywrightManager({
      browserType: 'chromium',
      headless: false,
      video: true
    });
    
    await manager.initPlaywright();
    await use(manager);
    await manager.closePlaywright();
  },

  testPage: async ({ pwManager }, use, testInfo) => {
    const page = await pwManager.openNewPage();
    
    // Use the page in the test
    await use(page);
    
    // Capture screenshot on failure
    if (testInfo.status !== testInfo.expectedStatus) {
      const screenshot = await pwManager.screenshotBase64();
      await testInfo.attach('screenshot', {
        body: Buffer.from(screenshot, 'base64'),
        contentType: 'image/png'
      });
    }
    
    // Save video path
    const videoPath = await page.video()?.path();
    if (videoPath) {
      await testInfo.attach('video', {
        path: videoPath,
        contentType: 'video/webm'
      });
    }
    
    await pwManager.closePage();
  }
});

export { expect };

/**
 * Base test utilities
 */
export class TestUtils {
  /**
   * Add step to test report
   */
  static logStep(step: string): void {
    console.log(`\n📋 ${step}`);
  }

  /**
   * Log info message
   */
  static logInfo(message: string): void {
    console.log(`ℹ️  ${message}`);
  }

  /**
   * Log success message
   */
  static logSuccess(message: string): void {
    console.log(`✅ ${message}`);
  }

  /**
   * Log warning message
   */
  static logWarning(message: string): void {
    console.warn(`⚠️  ${message}`);
  }

  /**
   * Log error message
   */
  static logError(message: string): void {
    console.error(`❌ ${message}`);
  }

  /**
   * Generate timestamp
   */
  static timestamp(): string {
    return new Date().toISOString();
  }

  /**
   * Generate random email
   */
  static randomEmail(): string {
    const timestamp = Date.now();
    return `test.user.${timestamp}@cbaps-automation.com`;
  }

  /**
   * Generate random string
   */
  static randomString(length: number = 10): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  /**
   * Generate random number in range
   */
  static randomNumber(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  /**
   * Format currency
   */
  static formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }

  /**
   * Wait with reason
   */
  static async waitFor(milliseconds: number, reason?: string): Promise<void> {
    if (reason) {
      console.log(`⏳ Waiting ${milliseconds}ms: ${reason}`);
    }
    await new Promise(resolve => setTimeout(resolve, milliseconds));
  }

  /**
   * Retry action with exponential backoff
   */
  static async retryAction<T>(
    action: () => Promise<T>,
    maxRetries: number = 3,
    delayMs: number = 1000
  ): Promise<T> {
    let lastError: Error | undefined;
    
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await action();
      } catch (error) {
        lastError = error as Error;
        if (i < maxRetries - 1) {
          const waitTime = delayMs * Math.pow(2, i);
          console.log(`⚠️  Retry attempt ${i + 1}/${maxRetries} after ${waitTime}ms...`);
          await this.waitFor(waitTime);
        }
      }
    }
    
    throw lastError;
  }
}
