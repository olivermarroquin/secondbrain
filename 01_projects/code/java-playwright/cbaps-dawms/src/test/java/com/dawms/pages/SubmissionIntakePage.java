package com.dawms.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.dawms.library.PlaywrightManager;

/**
 * SubmissionIntakePage: Create and manage drug submissions in DAWMS
 * Handles submission type, application number, and navigation to reviewer assignment
 */
public class SubmissionIntakePage {

	private static final Logger log = LoggerFactory.getLogger(SubmissionIntakePage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator submissionTypeDropdown;
	private final Locator applicationNumberInput;
	private final Locator createSubmissionButton;

	public SubmissionIntakePage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Initialize locators
		this.submissionTypeDropdown = page.locator("#submissionType");
		this.applicationNumberInput = page.locator("#applicationNumber");
		this.createSubmissionButton = page.locator("button:has-text('Create Submission')");

		// Stability anchor: wait for page to be ready
		pwm.waitVisible("#submissionType");
		log.info("Submission Intake Page loaded successfully.");
	}

	/**
	 * Create a new submission with type and application number
	 * @param submissionType - Type of submission (NDA, ANDA, BLA, etc.)
	 * @param appNumber - Application number
	 * @return ReviewerAssignmentPage
	 */
	public ReviewerAssignmentPage createSubmission(String submissionType, String appNumber) {
		submissionTypeDropdown.selectOption(submissionType);
		log.info("Selected submission type: " + submissionType);
		
		pwm.type(applicationNumberInput, appNumber);
		log.info("Entered application number: " + appNumber);
		
		pwm.click(createSubmissionButton);
		log.info("Clicked 'Create Submission' button.");
		
		return new ReviewerAssignmentPage(page, pwm);
	}
}
