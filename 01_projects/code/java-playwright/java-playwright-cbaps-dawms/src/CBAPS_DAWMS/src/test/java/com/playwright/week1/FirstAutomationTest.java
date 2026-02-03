package com.playwright.week1;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.BrowserType.LaunchOptions;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;

public class FirstAutomationTest {

	public static void main(String[] args) {
		try {
			// Initialize Playwright object
			Playwright playwright = Playwright.create();

			// select the channel to start a browser
			// chrome, msedge, 			
			LaunchOptions launchOption = new BrowserType.LaunchOptions().setChannel("chrome");

			// headless mode is true by default
			launchOption.setHeadless(false);

			// Lunch browser and default options: chromium, firefox, webkit is like Safari
			Browser browser = playwright.chromium().launch(launchOption);
			
			// create a new browser page
			Page page = browser.newPage();
			
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
						
			//9. Select "Payment Period"
			page.selectOption("#paymentMode", "Monthly");
			
			//10. Click "Calculate Now" button
			page.click("#button");			
			
			// add 15 seconds pause 
			Thread.sleep(10 * 1000);
			
			// close the browser
			browser.close();
			playwright.close();
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
