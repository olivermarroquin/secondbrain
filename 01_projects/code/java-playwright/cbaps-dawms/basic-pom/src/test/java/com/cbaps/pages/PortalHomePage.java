package com.cbaps.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.cbaps.library.PlaywrightManager;

/**
 * PortalHomePage: Shared entry point for CBAPS and DAWMS applications
 * User selects which application to access from portal
 */
public class PortalHomePage {

	private static final Logger log = LoggerFactory.getLogger(PortalHomePage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator cbapsLink;
	private final Locator dawmsLink;

	public PortalHomePage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Locators for application links
		this.cbapsLink = page.locator("a:has-text('CBAPS')");
		this.dawmsLink = page.locator("a:has-text('DAWMS')");

		// Stability anchor: wait for portal to load
		pwm.waitVisible("text=Application Portal");
		log.info("Portal Home Page loaded successfully.");
	}

	/**
	 * Navigate to portal homepage
	 */
	public PortalHomePage navigateToPortal(String portalUrl) {
		page.navigate(portalUrl);
		pwm.waitVisible("text=Application Portal");
		log.info("Navigated to Portal: " + portalUrl);
		return this;
	}

	/**
	 * Open CBAPS application from portal
	 * @return CBAPSDashboardPage
	 */
	public CBAPSDashboardPage openCBAPS() {
		pwm.click(cbapsLink);
		log.info("Clicked CBAPS link from portal.");
		return new CBAPSDashboardPage(page, pwm);
	}

	/**
	 * Get portal page title
	 */
	public String getTitle() {
		return page.title();
	}
}
