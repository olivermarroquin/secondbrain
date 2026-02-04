package com.cbaps.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.cbaps.library.PlaywrightManager;

/**
 * CBAPSDashboardPage: Main dashboard for CBAPS application
 * Provides navigation to key CBAPS workflows like Requisition creation
 */
public class CBAPSDashboardPage {

	private static final Logger log = LoggerFactory.getLogger(CBAPSDashboardPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator createRequisitionBtn;

	public CBAPSDashboardPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Locator for Create Requisition button
		this.createRequisitionBtn = page.locator("button:has-text('Create Requisition')");

		// Stability anchor: wait for dashboard to load
		pwm.waitVisible("text=CBAPS Dashboard");
		log.info("CBAPS Dashboard Page loaded successfully.");
	}

	/**
	 * Navigate to Create Requisition page
	 * @return RequisitionPage
	 */
	public RequisitionPage goToCreateRequisition() {
		pwm.click(createRequisitionBtn);
		log.info("Clicked 'Create Requisition' button.");
		return new RequisitionPage(page, pwm);
	}
}
