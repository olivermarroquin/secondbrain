package com.dawms.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.dawms.library.PlaywrightManager;

/**
 * MilestoneStatusPage: Final milestone and status validation page
 * Displays current submission milestone and status
 */
public class MilestoneStatusPage {

	private static final Logger log = LoggerFactory.getLogger(MilestoneStatusPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator milestoneLabel;
	private final Locator statusLabel;

	public MilestoneStatusPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Initialize locators
		this.milestoneLabel = page.locator("#milestone");
		this.statusLabel = page.locator("#status");

		// Stability anchor: wait for status to be visible
		pwm.waitVisible("#status");
		log.info("Milestone Status Page loaded successfully.");
	}

	/**
	 * Get current submission milestone
	 * @return Milestone text
	 */
	public String getMilestone() {
		String milestone = milestoneLabel.textContent();
		log.info("Retrieved milestone: " + milestone);
		return milestone;
	}

	/**
	 * Get current submission status
	 * @return Status text
	 */
	public String getStatus() {
		String status = statusLabel.textContent();
		log.info("Retrieved status: " + status);
		return status;
	}
}
