package com.dawms.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.dawms.library.PlaywrightManager;

/**
 * DAWMSDashboardPage: Main dashboard for DAWMS application
 * Provides navigation to key DAWMS workflows like Submission Intake
 */
public class DAWMSDashboardPage {

	private static final Logger log = LoggerFactory.getLogger(DAWMSDashboardPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator submissionIntakeBtn;

	public DAWMSDashboardPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Locator for Submission Intake button
		this.submissionIntakeBtn = page.locator("button:has-text('Submission Intake')");

		// Stability anchor: wait for dashboard to load
		pwm.waitVisible("text=DAWMS Dashboard");
		log.info("DAWMS Dashboard Page loaded successfully.");
	}

	/**
	 * Navigate to Submission Intake page
	 * @return SubmissionIntakePage
	 */
	public SubmissionIntakePage goToSubmissionIntake() {
		pwm.click(submissionIntakeBtn);
		log.info("Clicked 'Submission Intake' button.");
		return new SubmissionIntakePage(page, pwm);
	}
}
