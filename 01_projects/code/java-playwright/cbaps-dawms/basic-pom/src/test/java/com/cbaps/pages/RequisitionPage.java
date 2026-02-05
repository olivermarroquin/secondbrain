package com.cbaps.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.cbaps.library.PlaywrightManager;

/**
 * RequisitionPage: Create and manage requisitions in CBAPS
 * Handles requisition title, fund type, and navigation to funding lines
 */
public class RequisitionPage {

	private static final Logger log = LoggerFactory.getLogger(RequisitionPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	// Locators
	private final Locator titleInput;
	private final Locator fundTypeDropdown;
	private final Locator submitButton;
	private final Locator statusBadge;
	private final Locator goToFundingLink;
	private final Locator routeForApprovalButton;

	public RequisitionPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Initialize locators
		this.titleInput = page.locator("#requisitionTitle");
		this.fundTypeDropdown = page.locator("#fundType");
		this.submitButton = page.locator("button:has-text('Submit')");
		this.statusBadge = page.locator("#reqStatus");
		this.goToFundingLink = page.locator("a:has-text('Funding Lines')");
		this.routeForApprovalButton = page.locator("button:has-text('Route for Approval')");

		// Stability anchor: wait for page to be ready
		pwm.waitVisible("#requisitionTitle");
		log.info("Requisition Page loaded successfully.");
	}

	/**
	 * Create a new requisition with title and fund type
	 * @param title - Requisition title
	 * @param fundType - Fund type selection
	 */
	public void createRequisition(String title, String fundType) {
		pwm.type(titleInput, title);
		log.info("Entered requisition title: " + title);
		
		fundTypeDropdown.selectOption(fundType);
		log.info("Selected fund type: " + fundType);
		
		pwm.click(submitButton);
		log.info("Clicked Submit button.");
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

	/**
	 * Navigate to Funding Lines page
	 * @return FundingLinesPage
	 */
	public FundingLinesPage goToFundingLines() {
		pwm.click(goToFundingLink);
		log.info("Navigated to Funding Lines page.");
		return new FundingLinesPage(page, pwm);
	}

	/**
	 * Route requisition for approval
	 * @return RoutingApprovalPage
	 */
	public RoutingApprovalPage routeForApproval() {
		pwm.click(routeForApprovalButton);
		log.info("Clicked 'Route for Approval' button.");
		return new RoutingApprovalPage(page, pwm);
	}
}
