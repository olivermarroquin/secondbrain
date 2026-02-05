/**
 * PlaywrightManager: Enhanced TypeScript wrapper for Playwright
 * Manages browser lifecycle and provides type-safe interaction methods
 */

import { Browser, BrowserContext, Page, Locator, chromium, firefox, webkit } from '@playwright/test';
import { BrowserConfig } from './types';
import * as fs from 'fs';
import * as path from 'path';

export class PlaywrightManager {
  private browser: Browser | null = null;
  private context: BrowserContext | null = null;
  public page: Page | null = null;
  
  private config: BrowserConfig = {
    browserType: 'chromium',
    headless: false,
    viewport: { width: 1280, height: 720 },
    slowMo: 0,
    video: true,
    screenshot: true
  };

  constructor(customConfig?: Partial<BrowserConfig>) {
    if (customConfig) {
      this.config = { ...this.config, ...customConfig };
    }
    this.ensureDirectories();
  }

  /**
   * Ensure output directories exist
   */
  private ensureDirectories(): void {
    const dirs = ['target/screenshots', 'target/videos', 'target/traces', 'target/reports'];
    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }

  /**
   * Initialize Playwright with browser and context
   */
  async initPlaywright(): Promise<void> {
    try {
      // Select browser type
      const browserType = this.config.browserType === 'firefox' ? firefox
        : this.config.browserType === 'webkit' ? webkit
        : chromium;

      // Launch browser
      this.browser = await browserType.launch({
        headless: this.config.headless,
        slowMo: this.config.slowMo,
        args: ['--start-maximized']
      });

      // Create context with options
      this.context = await this.browser.newContext({
        viewport: this.config.headless ? this.config.viewport : null,
        recordVideo: this.config.video ? {
          dir: 'target/videos/',
          size: { width: 1280, height: 720 }
        } : undefined,
        ignoreHTTPSErrors: true
      });

      // Enable tracing for debugging
      await this.context.tracing.start({ screenshots: true, snapshots: true });

      console.log(`✓ Playwright initialized with ${this.config.browserType} browser`);
    } catch (error) {
      console.error('Failed to initialize Playwright:', error);
      throw error;
    }
  }

  /**
   * Open a new browser page
   */
  async openNewPage(): Promise<Page> {
    if (!this.context) {
      throw new Error('Browser context not initialized. Call initPlaywright() first.');
    }

    this.page = await this.context.newPage();
    console.log('✓ New browser page opened');
    return this.page;
  }

  /**
   * Close the current page
   */
  async closePage(): Promise<void> {
    if (this.page) {
      await this.page.close();
      console.log('✓ Browser page closed');
    }
  }

  /**
   * Close Playwright completely
   */
  async closePlaywright(): Promise<void> {
    try {
      if (this.context) {
        await this.context.tracing.stop({ path: `target/traces/trace-${Date.now()}.zip` });
        await this.context.close();
      }
      if (this.browser) {
        await this.browser.close();
      }
      console.log('✓ Playwright session closed');
    } catch (error) {
      console.error('Error closing Playwright:', error);
      throw error;
    }
  }

  // ============ Enhanced Action Methods ============

  /**
   * Type-safe click with retry logic
   */
  async click(locator: Locator, options?: { timeout?: number; force?: boolean }): Promise<void> {
    try {
      await this.highlightElement(locator);
      await locator.click({ timeout: options?.timeout || 30000, force: options?.force });
      console.log('✓ Element clicked');
    } catch (error) {
      console.error('Click failed:', error);
      throw error;
    }
  }

  /**
   * Type text with clear and validation
   */
  async type(locator: Locator, text: string, options?: { clear?: boolean; delay?: number }): Promise<void> {
    try {
      await this.highlightElement(locator);
      
      if (options?.clear !== false) {
        await locator.clear();
      }
      
      await locator.fill(text, { timeout: 30000 });
      
      // Validate the text was entered correctly
      const value = await locator.inputValue();
      if (value !== text) {
        console.warn(`Warning: Expected "${text}" but got "${value}"`);
      }
      
      console.log(`✓ Typed: "${text}"`);
    } catch (error) {
      console.error('Type failed:', error);
      throw error;
    }
  }

  /**
   * Wait for element to be visible with custom message
   */
  async waitVisible(selector: string, message?: string, timeout: number = 30000): Promise<void> {
    try {
      if (!this.page) throw new Error('Page not initialized');
      
      await this.page.waitForSelector(selector, { state: 'visible', timeout });
      const locator = this.page.locator(selector);
      await this.highlightElement(locator);
      
      console.log(`✓ ${message || 'Element visible'}: ${selector}`);
    } catch (error) {
      console.error(`Element not visible: ${selector}`, error);
      throw error;
    }
  }

  /**
   * Wait for element to be hidden
   */
  async waitHidden(selector: string, timeout: number = 30000): Promise<void> {
    if (!this.page) throw new Error('Page not initialized');
    await this.page.waitForSelector(selector, { state: 'hidden', timeout });
    console.log(`✓ Element hidden: ${selector}`);
  }

  /**
   * Select dropdown option with validation
   */
  async selectDropdown(locator: Locator, value: string): Promise<void> {
    try {
      await this.highlightElement(locator);
      await locator.selectOption(value);
      
      // Validate selection
      const selectedValue = await locator.inputValue();
      if (selectedValue !== value) {
        console.warn(`Warning: Expected "${value}" to be selected but got "${selectedValue}"`);
      }
      
      console.log(`✓ Selected dropdown option: "${value}"`);
    } catch (error) {
      console.error('Dropdown selection failed:', error);
      throw error;
    }
  }

  /**
   * Get text content from locator
   */
  async getText(locator: Locator): Promise<string> {
    const text = await locator.textContent() || '';
    console.log(`✓ Retrieved text: "${text}"`);
    return text.trim();
  }

  /**
   * Check if element is visible
   */
  async isVisible(locator: Locator): Promise<boolean> {
    try {
      return await locator.isVisible();
    } catch {
      return false;
    }
  }

  /**
   * Check if element is enabled
   */
  async isEnabled(locator: Locator): Promise<boolean> {
    try {
      return await locator.isEnabled();
    } catch {
      return false;
    }
  }

  /**
   * Highlight element for visual feedback (optional demo mode)
   */
  private async highlightElement(locator: Locator): Promise<void> {
    if (this.config.slowMo && this.config.slowMo > 0) {
      try {
        await locator.evaluate((el: HTMLElement) => {
          const originalStyle = el.style.cssText;
          el.style.border = '3px solid red';
          el.style.backgroundColor = 'yellow';
          setTimeout(() => {
            el.style.cssText = originalStyle;
          }, 500);
        });
      } catch {
        // Ignore highlight errors
      }
    }
  }

  /**
   * Take screenshot with custom name
   */
  async screenshot(name: string, fullPage: boolean = true): Promise<string> {
    if (!this.page) throw new Error('Page not initialized');
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${name}-${timestamp}.png`;
    const filepath = path.join('target/screenshots', filename);
    
    await this.page.screenshot({ path: filepath, fullPage });
    console.log(`✓ Screenshot saved: ${filepath}`);
    return filepath;
  }

  /**
   * Take screenshot as base64
   */
  async screenshotBase64(): Promise<string> {
    if (!this.page) throw new Error('Page not initialized');
    
    const buffer = await this.page.screenshot({ fullPage: true });
    return buffer.toString('base64');
  }

  /**
   * Navigate to URL with wait
   */
  async navigateTo(url: string, waitUntil: 'load' | 'domcontentloaded' | 'networkidle' = 'load'): Promise<void> {
    if (!this.page) throw new Error('Page not initialized');
    
    await this.page.goto(url, { waitUntil, timeout: 60000 });
    console.log(`✓ Navigated to: ${url}`);
  }

  /**
   * Wait for specified time (use sparingly)
   */
  async wait(milliseconds: number): Promise<void> {
    await new Promise(resolve => setTimeout(resolve, milliseconds));
  }

  /**
   * Press keyboard key
   */
  async pressKey(locator: Locator, key: string): Promise<void> {
    await locator.press(key);
    console.log(`✓ Pressed key: ${key}`);
  }

  /**
   * Scroll element into view
   */
  async scrollToElement(locator: Locator): Promise<void> {
    await locator.scrollIntoViewIfNeeded();
    console.log('✓ Scrolled element into view');
  }

  /**
   * Get page title
   */
  async getTitle(): Promise<string> {
    if (!this.page) throw new Error('Page not initialized');
    return await this.page.title();
  }

  /**
   * Get current URL
   */
  async getCurrentUrl(): Promise<string> {
    if (!this.page) throw new Error('Page not initialized');
    return this.page.url();
  }
}
