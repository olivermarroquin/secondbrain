package com.cbaps.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.cbaps.library.PlaywrightManager;

/**
 * StatusTrackerPage: Final status validation page
 * Displays current requisition status after routing
 */
public class StatusTrackerPage {

	private static final Logger log = LoggerFactory.getLogger(StatusTrackerPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator statusBadge;

	public StatusTrackerPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Initialize locator
		this.statusBadge = page.locator("#reqStatus");

		// Stability anchor: wait for status to be visible
		pwm.waitVisible("#reqStatus");
		log.info("Status Tracker Page loaded successfully.");
	}

	/**
	 * Get current requisition status
	 * @return Status text
	 */
	public String getStatus() {
		String status = statusBadge.textContent();
		log.info("Retrieved status: " + status);
		return status;
	}
}
