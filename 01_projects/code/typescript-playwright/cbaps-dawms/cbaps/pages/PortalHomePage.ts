/**
 * PortalHomePage: Enhanced portal entry point with validation methods
 * Provides navigation to CBAPS and DAWMS applications
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { CBAPSDashboardPage } from './CBAPSDashboardPage';

export class PortalHomePage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  // Locators
  readonly cbapsLink: Locator;
  readonly dawmsLink: Locator;
  readonly headerLogo: Locator;
  readonly userProfileMenu: Locator;
  readonly searchBox: Locator;
  readonly notificationsBell: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    // Initialize locators
    this.cbapsLink = page.locator("a:has-text('CBAPS')");
    this.dawmsLink = page.locator("a:has-text('DAWMS')");
    this.headerLogo = page.locator('.portal-logo');
    this.userProfileMenu = page.locator('#user-profile-menu');
    this.searchBox = page.locator('#global-search');
    this.notificationsBell = page.locator('#notifications');

    // Stability anchor
    this.pwManager.waitVisible('text=Application Portal', 'Portal page loaded');
    console.log('✓ Portal Home Page initialized');
  }

  /**
   * Navigate to portal URL
   */
  async navigateToPortal(url: string): Promise<this> {
    await this.pwManager.navigateTo(url);
    await this.pwManager.waitVisible('text=Application Portal', 'Waiting for portal to load');
    return this;
  }

  /**
   * Open CBAPS application
   */
  async openCBAPS(): Promise<CBAPSDashboardPage> {
    await this.pwManager.click(this.cbapsLink);
    console.log('✓ Clicked CBAPS link');
    return new CBAPSDashboardPage(this.page, this.pwManager);
  }

  /**
   * Open DAWMS application (placeholder for DAWMS pages)
   */
  async openDAWMS(): Promise<any> {
    await this.pwManager.click(this.dawmsLink);
    console.log('✓ Clicked DAWMS link');
    // Return DAWMS dashboard page when created
    return null;
  }

  /**
   * Get page title
   */
  async getTitle(): Promise<string> {
    return await this.pwManager.getTitle();
  }

  /**
   * Validate portal is loaded correctly
   */
  async validatePortalLoaded(): Promise<boolean> {
    const isCbapsVisible = await this.pwManager.isVisible(this.cbapsLink);
    const isDawmsVisible = await this.pwManager.isVisible(this.dawmsLink);
    const isLogoVisible = await this.pwManager.isVisible(this.headerLogo);

    const isValid = isCbapsVisible && isDawmsVisible && isLogoVisible;
    
    if (isValid) {
      console.log('✓ Portal validation passed');
    } else {
      console.warn('⚠️  Portal validation failed');
    }

    return isValid;
  }

  /**
   * Search in global search box
   */
  async search(query: string): Promise<void> {
    if (await this.pwManager.isVisible(this.searchBox)) {
      await this.pwManager.type(this.searchBox, query);
      await this.pwManager.pressKey(this.searchBox, 'Enter');
      console.log(`✓ Searched for: "${query}"`);
    }
  }

  /**
   * Check if user is logged in
   */
  async isUserLoggedIn(): Promise<boolean> {
    return await this.pwManager.isVisible(this.userProfileMenu);
  }

  /**
   * Get notification count
   */
  async getNotificationCount(): Promise<number> {
    if (await this.pwManager.isVisible(this.notificationsBell)) {
      const badge = this.page.locator('#notifications .badge');
      if (await badge.isVisible()) {
        const text = await this.pwManager.getText(badge);
        return parseInt(text) || 0;
      }
    }
    return 0;
  }

  /**
   * Wait for portal to be ready
   */
  async waitForPortalReady(): Promise<void> {
    await this.pwManager.waitVisible('text=Application Portal');
    await this.pwManager.wait(500); // Small wait for JS to settle
    console.log('✓ Portal is ready');
  }
}
