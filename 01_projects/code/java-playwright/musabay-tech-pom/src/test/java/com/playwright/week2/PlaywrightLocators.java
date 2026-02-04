package com.playwright.week2;

import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.microsoft.playwright.BrowserType.LaunchOptions;

public class PlaywrightLocators {

	private Playwright playwright;
	private Browser browser;
	private Page page;

	@BeforeClass
	public void beforeTestClass() {
		playwright = Playwright.create();
		LaunchOptions launchOption = new BrowserType.LaunchOptions().setChannel("chrome");
		launchOption.setHeadless(false);
		browser = playwright.chromium().launch(launchOption);
		System.out.println("Create playwright & browser objects.");
	}

	@AfterClass
	public void afterTestClass() {
		browser.close();
		playwright.close();
		System.out.println("Cleaning up playwright & browser objects.");
	}

	@BeforeMethod
	public void setUp() {
		page = browser.newPage();
		System.out.println("Open chrome browser.");
	}

	@AfterMethod
	public void tearDown() {
		page.close();
		System.out.println("closing chrome browser.");
	}

	@Test(enabled = false)
	public void buyTownHouseTest1() {
		try {
			// add 5 seconds pause
			Thread.sleep(5 * 1000);

			// Step1. Go to page https://www.mortgagecalculator.net/
			page.navigate("https://www.mortgagecalculator.net/");
			System.out.println("navigating to website");

			// Step2. Select "$" icon from the "Mortgage Amount"
			// locating drop-down element using CSS Selector locator
			page.selectOption("#currency", "£");

			// Step3. Enter "Mortgage Amount"
			page.fill("#amount", "500000");

			// Step4. Enter "Amortization - Year & Month"
			page.fill("#amortizationYears", "29");
			page.fill("#amortizationMonths", "12");

			// Step5. Enter "Interest Term" for Year & Month
			page.fill("#interestTermYears", "30");
			page.fill("#interestTermMonths", "2");

			// Step6. Select "Interest Type"
			page.selectOption("#interestType", "Fixed");

			// 7. Enter "Interest Rate"
			page.fill("#rate", "6.5");

			// 8. Select "Start Date" for Month & Year
			page.selectOption("#startMonth", "4");
			page.selectOption("#startYear", "2025");

			// 9. Select "Payment Period"
			page.selectOption("#paymentMode", "Monthly");

			// 10. Click "Calculate Now" button
			page.click("#button");

			// add 15 seconds pause
			Thread.sleep(10 * 1000);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Test(enabled = false)
	public void buySingleHouseTest2() {
		try {
			// add 5 seconds pause
			Thread.sleep(5 * 1000);

			// Step1. Go to page https://www.mortgagecalculator.net/
			page.navigate("https://www.mortgagecalculator.net/");
			System.out.println("navigating to website");

			// Step2. Select "$" icon from the "Mortgage Amount"
			// locating drop-down element using CSS Selector locator
			page.selectOption("#currency", "$");

			// Step3. Enter "Mortgage Amount"
			page.fill("#amount", "900000");

			// Step4. Enter "Amortization - Year & Month"
			page.fill("#amortizationYears", "29");
			page.fill("#amortizationMonths", "12");

			// Step5. Enter "Interest Term" for Year & Month
			page.fill("#interestTermYears", "30");
			page.fill("#interestTermMonths", "2");

			// Step6. Select "Interest Type"
			page.selectOption("#interestType", "Fixed");

			// 7. Enter "Interest Rate"
			page.fill("#rate", "6.5");

			// 8. Select "Start Date" for Month & Year
			page.selectOption("#startMonth", "4");
			page.selectOption("#startYear", "2025");

			// 9. Select "Payment Period"
			page.selectOption("#paymentMode", "Monthly");

			// 10. Click "Calculate Now" button
			page.click("#button");

			// add 15 seconds pause
			Thread.sleep(10 * 1000);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Test
	public void locatorTests() {
		
		page.navigate("https://www.mortgagecalculator.org/");
		
		// 1: Attribute Selector
		// Attribute Selector: Use unique attributes like name or aria-label (e.g., [name='homeValue']).
		// attributes like id, name, class, type, placeholder, or aria-label.
		page.locator("[type='button']").click();
		
		//String a = "[aria-label='Our Night Sky']";
		
		// 2: CSS Selector
		// css using id      example: <input id="amount" class="right-cell">
		page.locator("#amount").fill("200000");
		// css using class   example: <input id="homeval" class="right-cell">
		page.locator("input.right-cell").selectOption("fixed");
		// css using hierarchy
		page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(8) > select").fill("12345");
		
		// 3. Text Selector
		page.locator("text=Update Lenders");
		page.locator("label= Start Date: ");
		
		// 4. Xpath Selector
		// Description: Uses XPath expressions to locate elements.
		// Syntax: xpath=//expression
		// Example:
		//		page.locator("//button[@id='submitButton']").click();
		
		// 5. Label Selector
		// Description: Targets input elements associated with a specific <label> element.
		// Syntax: label=label_text
		// Example:
		//		page.locator("label=Username").fill("john_doe");
		//		page.locator("label= Start Date: ");
		
		// 6) Placeholder Selector
		// Description: Targets input elements by their placeholder attribute.
		// Syntax: placeholder=placeholder_text
		// Example:
		//		page.locator("placeholder=80000").fill("20000");
		
		// 7) Alt Selector
		// Description: Targets images by their alt attribute.
		// Syntax: alt=alt_text
		// Example: 
		//		page.click("alt=Profile Picture");

		// 8 Title Selector
		page.locator("title=Mortgage Calculator").click();
		
	}
}

























