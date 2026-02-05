package com.cbaps.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.cbaps.library.PlaywrightManager;

/**
 * FundingLinesPage: Add and manage funding lines for a requisition
 * Allows adding multiple funding lines and continuing to routing
 */
public class FundingLinesPage {

	private static final Logger log = LoggerFactory.getLogger(FundingLinesPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator addLineButton;
	private final Locator amountInput;
	private final Locator saveLineButton;
	private final Locator continueToRoutingButton;

	public FundingLinesPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Initialize locators
		this.addLineButton = page.locator("button:has-text('Add Line')");
		this.amountInput = page.locator("#fundAmount");
		this.saveLineButton = page.locator("button:has-text('Save')");
		this.continueToRoutingButton = page.locator("button:has-text('Continue to Routing')");

		// Stability anchor: wait for page to load
		pwm.waitVisible("text=Funding Lines");
		log.info("Funding Lines Page loaded successfully.");
	}

	/**
	 * Add a funding line with specified amount
	 * @param amount - Funding amount
	 * @return this (for method chaining)
	 */
	public FundingLinesPage addFundingLine(String amount) {
		pwm.click(addLineButton);
		log.info("Clicked 'Add Line' button.");
		
		pwm.type(amountInput, amount);
		log.info("Entered funding amount: " + amount);
		
		pwm.click(saveLineButton);
		log.info("Clicked 'Save' button for funding line.");
		
		return this;
	}

	/**
	 * Continue to Routing/Approval step
	 * @return RoutingApprovalPage
	 */
	public RoutingApprovalPage continueToRouting() {
		pwm.click(continueToRoutingButton);
		log.info("Clicked 'Continue to Routing' button.");
		return new RoutingApprovalPage(page, pwm);
	}
}
