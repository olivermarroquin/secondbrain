/**
 * PortalHomePage: Portal entry point for DAWMS
 */

import { Page, Locator } from '@playwright/test';
import { PlaywrightManager } from '../library/PlaywrightManager';
import { DAWMSDashboardPage } from './DAWMSDashboardPage';

export class PortalHomePage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;

  readonly dawmsLink: Locator;
  readonly headerLogo: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    this.page = page;
    this.pwManager = pwManager;

    this.dawmsLink = page.locator("a:has-text('DAWMS')");
    this.headerLogo = page.locator('.portal-logo');

    this.pwManager.waitVisible('text=Application Portal', 'Portal page loaded');
    console.log('✓ Portal Home Page initialized');
  }

  async navigateToPortal(url: string): Promise<this> {
    await this.pwManager.navigateTo(url);
    await this.pwManager.waitVisible('text=Application Portal', 'Waiting for portal');
    return this;
  }

  async openDAWMS(): Promise<DAWMSDashboardPage> {
    await this.pwManager.click(this.dawmsLink);
    console.log('✓ Clicked DAWMS link');
    return new DAWMSDashboardPage(this.page, this.pwManager);
  }

  async validatePortalLoaded(): Promise<boolean> {
    const isDawmsVisible = await this.pwManager.isVisible(this.dawmsLink);
    const isLogoVisible = await this.pwManager.isVisible(this.headerLogo);
    return isDawmsVisible && isLogoVisible;
  }

  async getTitle(): Promise<string> {
    return await this.pwManager.getTitle();
  }
}
