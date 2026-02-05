package com.cbaps.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.cbaps.library.PlaywrightManager;

/**
 * RoutingApprovalPage: Route requisition to approvers
 * Select approver and submit routing
 */
public class RoutingApprovalPage {

	private static final Logger log = LoggerFactory.getLogger(RoutingApprovalPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator selectApproverDropdown;
	private final Locator submitRoutingButton;

	public RoutingApprovalPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Initialize locators
		this.selectApproverDropdown = page.locator("#approver");
		this.submitRoutingButton = page.locator("button:has-text('Submit Routing')");

		// Stability anchor: wait for routing page to load
		pwm.waitVisible("text=Routing");
		log.info("Routing Approval Page loaded successfully.");
	}

	/**
	 * Submit requisition for approval to selected approver
	 * @param approver - Approver name/role
	 * @return StatusTrackerPage
	 */
	public StatusTrackerPage submitForApproval(String approver) {
		selectApproverDropdown.selectOption(approver);
		log.info("Selected approver: " + approver);
		
		pwm.click(submitRoutingButton);
		log.info("Clicked 'Submit Routing' button.");
		
		return new StatusTrackerPage(page, pwm);
	}
}
