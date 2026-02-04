package com.dawms.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.dawms.library.PlaywrightManager;

/**
 * ReviewerAssignmentPage: Assign reviewers to drug submissions
 * Handles reviewer role selection, reviewer assignment, and routing to signature
 */
public class ReviewerAssignmentPage {

	private static final Logger log = LoggerFactory.getLogger(ReviewerAssignmentPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator reviewerRoleDropdown;
	private final Locator reviewerNameInput;
	private final Locator assignReviewerButton;
	private final Locator continueToSignatureButton;

	public ReviewerAssignmentPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Initialize locators
		this.reviewerRoleDropdown = page.locator("#reviewerRole");
		this.reviewerNameInput = page.locator("#reviewerName");
		this.assignReviewerButton = page.locator("button:has-text('Assign')");
		this.continueToSignatureButton = page.locator("button:has-text('Route to Signature')");

		// Stability anchor: wait for page to load
		pwm.waitVisible("text=Reviewer Assignment");
		log.info("Reviewer Assignment Page loaded successfully.");
	}

	/**
	 * Assign a reviewer with specified role and name
	 * @param role - Reviewer role (Clinical Reviewer, Pharmacologist, etc.)
	 * @param reviewerName - Name of reviewer
	 * @return this (for method chaining)
	 */
	public ReviewerAssignmentPage assignReviewer(String role, String reviewerName) {
		reviewerRoleDropdown.selectOption(role);
		log.info("Selected reviewer role: " + role);
		
		pwm.type(reviewerNameInput, reviewerName);
		log.info("Entered reviewer name: " + reviewerName);
		
		pwm.click(assignReviewerButton);
		log.info("Clicked 'Assign' button.");
		
		return this;
	}

	/**
	 * Continue to Signature Routing step
	 * @return SignatureRoutingPage
	 */
	public SignatureRoutingPage routeToSignatureStep() {
		pwm.click(continueToSignatureButton);
		log.info("Clicked 'Route to Signature' button.");
		return new SignatureRoutingPage(page, pwm);
	}
}
