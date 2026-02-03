package com.playwright.thegreatcourses.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.AriaRole;
import com.playwright.week5.library.PlaywrightManager;

public class ProductTypePage {

	private static final Logger log = LoggerFactory.getLogger(ProductTypePage.class);

	private PlaywrightManager myPlaywright;
	private Page page;

	
	public ProductTypePage(Page _page, PlaywrightManager _myPlaywright) {
		this.myPlaywright = _myPlaywright;
		this.page = _page;			
		myPlaywright.waitUntilElementVisible("div > section.ProductPage-Purchase");		
	}
	
	public void selectProductType(ProductTypes productType ) {
		
		switch(productType) {
		case DVD:
			myPlaywright.clickElement(page.locator("label:has-text('DVD')"));
			break;
			
		case Instant_Video:
			myPlaywright.clickElement(page.locator("label:has-text('Instant Video')"));
			break;
			
		case Instant_Audio:
			myPlaywright.clickElement(page.locator("label:has-text('Instant Audio')"));
			break;
			
		default:
			throw new IllegalArgumentException("Unsupported product type: " + productType);
		}		
	}
	
	public ProceedToCheckoutPage clickAddToCartButton() {
		// this action will navigate to new webpage
		Locator addToCartButton = page.getByRole(AriaRole.BUTTON, new Page
				.GetByRoleOptions().setName("Add to Cart"));
		myPlaywright.clickElement(addToCartButton.first());
		
		return new ProceedToCheckoutPage(page, myPlaywright);
	}
	
	
}














