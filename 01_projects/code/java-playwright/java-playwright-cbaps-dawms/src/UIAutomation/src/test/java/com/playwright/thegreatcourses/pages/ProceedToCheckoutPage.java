package com.playwright.thegreatcourses.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Page;
import com.playwright.week5.library.PlaywrightManager;

public class ProceedToCheckoutPage {

	private static final Logger log = LoggerFactory.getLogger(ProceedToCheckoutPage.class);

	private PlaywrightManager myPlaywright;
	private Page page;
	
	public ProceedToCheckoutPage(Page _page, PlaywrightManager _myPlaywright) {
		this.myPlaywright = _myPlaywright;
		this.page = _page;		
		myPlaywright.waitUntilElementVisible("a.ml-2.btn.btn-fill-success");
		log.info("Proceed to Checkout Page load is successfully.");
	}

	public CheckOutPage clickProceedToCheckoutBtn() {
		myPlaywright.clickElement(page.locator("a.ml-2.btn.btn-fill-success"));
		
		return new CheckOutPage(page, myPlaywright);
	}
}














