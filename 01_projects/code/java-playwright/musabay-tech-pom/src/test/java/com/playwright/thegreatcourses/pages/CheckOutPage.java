package com.playwright.thegreatcourses.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.AriaRole;
import com.playwright.week5.library.PlaywrightManager;

import net.datafaker.Faker;

public class CheckOutPage {

	private static final Logger log = LoggerFactory.getLogger(CheckOutPage.class);
	private PlaywrightManager myPlaywright;
	private Page page;

	public CheckOutPage(Page _page, PlaywrightManager _myPlaywright) {
		this.myPlaywright = _myPlaywright;
		this.page = _page;
		myPlaywright.waitUntilElementVisible("#email");
		log.info("Checkout Page loading is successfully.");
	}

	public void createAccount(String email, String password) {
		myPlaywright
				.clickElement(page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Create Account")));
		myPlaywright.enterText(page.locator("#email"), email);
		myPlaywright.enterText(page.locator("#password"), password);

		// click on accept terms hidden element
		myPlaywright.clickHiddenElement(page.locator("#accept-terms"));
		myPlaywright.clickElement(page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Continue")));
	}

	public void enterBillingAddressInfo() {
		Faker faker = new Faker();		
		String uniqueFirstName = faker.name().firstName();		
		log.info("test firstname: " + uniqueFirstName);		
		String uniqueLastName = faker.name().lastName();		
		log.info("test lastname: " + uniqueLastName);		
		String uniqueStreet1 = faker.address().streetAddress();		
		log.info("test street1: " + uniqueStreet1);		
		String uniqueStreet2 = faker.address().secondaryAddress();		
		log.info("test street2: " + uniqueStreet2);		
		String uniqueCity = faker.address().city();		
		log.info("test city: " + uniqueCity);		
		String uniqueState = faker.address().state();		
		log.info("test state: " + uniqueState);		
		String uniqueZipcode = faker.address().zipCode();		
		log.info("test zipcode: " + uniqueZipcode);		
		String uniqueCellPhone = faker.phoneNumber().cellPhone();		
		log.info("test cellphone: " + uniqueCellPhone);		
		
		myPlaywright.enterText(page.locator("#firstname").first(), uniqueFirstName);
		myPlaywright.enterText(page.locator("#lastname").first(), uniqueLastName);
		myPlaywright.enterText(page.locator("#street").first(), uniqueStreet1);
		myPlaywright.enterText(page.locator("#street2").first(), uniqueStreet2);
		myPlaywright.enterText(page.locator("#city").first(), uniqueCity);		
		myPlaywright.selectDropdown(page.locator("#state").first(), uniqueState);		
		myPlaywright.enterText(page.locator("#postcode").first(), uniqueZipcode);
		myPlaywright.enterText(page.locator("#telephone").first(), uniqueCellPhone);
		
		myPlaywright.clickElement(page.getByRole(
				AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Add the new address")));
	}
	
	public void verifyBillingInfo() {
		myPlaywright.waitUntilElementVisible("div.BillingStep > button.link.mt-3 > small");
		myPlaywright.clickHiddenElement(page.locator("#ship-to-billing"));
		myPlaywright.clickElement(page.getByRole(
				AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Continue")));
		
		
		
	}
	
}











