package com.dawms.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.dawms.library.PlaywrightManager;

/**
 * SignatureRoutingPage: Route submission for signature approval
 * Select signer and submit for signature
 */
public class SignatureRoutingPage {

	private static final Logger log = LoggerFactory.getLogger(SignatureRoutingPage.class);
	private final Page page;
	private final PlaywrightManager pwm;

	private final Locator signerDropdown;
	private final Locator routeForSignatureButton;

	public SignatureRoutingPage(Page page, PlaywrightManager pwm) {
		this.page = page;
		this.pwm = pwm;

		// Initialize locators
		this.signerDropdown = page.locator("#signer");
		this.routeForSignatureButton = page.locator("button:has-text('Submit for Signature')");

		// Stability anchor: wait for signature routing page to load
		pwm.waitVisible("text=Signature Routing");
		log.info("Signature Routing Page loaded successfully.");
	}

	/**
	 * Submit submission for signature to selected signer
	 * @param signerRoleOrName - Signer role or name
	 * @return MilestoneStatusPage
	 */
	public MilestoneStatusPage submitForSignature(String signerRoleOrName) {
		signerDropdown.selectOption(signerRoleOrName);
		log.info("Selected signer: " + signerRoleOrName);
		
		pwm.click(routeForSignatureButton);
		log.info("Clicked 'Submit for Signature' button.");
		
		return new MilestoneStatusPage(page, pwm);
	}
}
