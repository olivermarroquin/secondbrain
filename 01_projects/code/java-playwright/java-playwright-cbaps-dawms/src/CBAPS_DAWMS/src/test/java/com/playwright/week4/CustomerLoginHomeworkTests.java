package com.playwright.week4;

import org.assertj.core.api.Assertions;
import org.testng.annotations.Test;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.LoadState;
import com.microsoft.playwright.options.WaitForSelectorState;
import com.playwright.week3.OldBase;

public class CustomerLoginHomeworkTests extends OldBase{

	@Test

	public void CustomerLogin() {
		try {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		
		// this will initials / starts playwright inspector tool / another name is CodeGen. 
		page.pause();
		
		// this line waits until webpage is fully loaded. or full web-site load complete.
		page.waitForLoadState(LoadState.LOAD);
		
		String actualPageTitle = page.title();
		String expectedPageTitle = "XYZ Bank";
		
		System.out.println("website: " + actualPageTitle);
		
		// add page title verification
		Assertions.assertThat(actualPageTitle.equals(expectedPageTitle))
		.as("Actual page title did not match with expected page title.")
		.isTrue();
				
	
		
		Locator customerLoginButton = page.locator("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");
		
		blinkHighlight(page, customerLoginButton);
		
		
		System.out.println("Step1: Clicking 'Customer Login' button. ");
		page.click("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");// use
																													// CSS
		// verify login button is there but hidden
		Locator loginButton2 = page.locator("body > div > div > div.ng-scope > div > form > button");
		Assertions.assertThat(loginButton2.isVisible())
		.as("Login button should be Hidden.")
		.isFalse();
		
		System.out.println("--- Login button is visible but it should be hidden.");
		
		// Login
																													// button
		Thread.sleep(2 * 1000);
		System.out.println("Step2: Selecting 'Hermonie' bank customer. ");
		
		// locate dropdown element and call blink highlight method
		Locator customerSelectElement = page.locator("#userSelect");
		blinkHighlight(page, customerSelectElement);
		
		page.selectOption("#userSelect", "1");// use CSS locator select Hermonie
		Thread.sleep(2 * 1000);
		// before clicking login button, add Explicit wait for login button visibility
		System.out.println("Step3: Waiting until 'Login' button is visible.");
		
		
		// default maximum wait time for below method is 30 seconds.
		page.locator("body > div > div > div.ng-scope > div > form > button").
		waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.VISIBLE));
		
		Locator loginButton = page.locator("body > div > div > div.ng-scope > div > form > button");
		Assertions.assertThat(loginButton.isVisible())
		.as("Login button is Not visible.")
		.isTrue();
		
		
		
		Locator loginButton11 = page.locator("body > div > div > div.ng-scope > div > form > button");
		blinkHighlight(page, loginButton11);
		
		
		System.out.println("Step4: Clicking 'Login' button.");
		page.click("body > div > div > div.ng-scope > div > form > button");// use CSS locator to click login button
		
		
		
		Thread.sleep(2 * 1000);
		System.out.println("Step5: Clicking 'Deposit' button.");
		page.locator("[ng-click='deposit()']").click();// use attribute locator to click deposit button
		//Thread.sleep(2 * 1000);
		
		// page.waitForTimeout(1.5 * 1000);
		
		page.locator("[placeholder='amount']").fill("5000");// use attribute locator to fill 5000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// use
																														// CSS
																														// to
																														// click
																														// deposit
																														// button
		Thread.sleep(2 * 1000);
		page.locator("[ng-class='btnClass3']").click();// use attribute to click withdraw button
		Thread.sleep(2 * 1000);
		page.locator("[ng-model='amount']").fill("3000");// use attribute to locate and fill 3000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// click
																														// withdraw
																														// button
		Thread.sleep(2 * 1000);
		page.locator("[ng-model='amount']").fill("15000");// use attribute to fill 15000
		Thread.sleep(2 * 1000);
		page.locator("[class='btn btn-default']").click();// click withdraw button
		Thread.sleep(2 * 1000);
		page.click("body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(1)");// click
																										// transaction
																										// button
		Thread.sleep(2 * 1000);
		page.click("body > div > div > div.ng-scope > div > div.fixedTopBox > button:nth-child(3)");// click reset
																									// button
		Thread.sleep(2 * 1000);
		page.click("body > div > div > div.box.mainhdr > button.btn.logout");// click logout button

		}catch (Exception e) {
			e.printStackTrace();
		}
		
	}

	@Test
	public void VerifyAccountDetailsOnLogin() {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		System.out.println("website: " + page.title());

		page.click("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");// click
																													// Customer
																													// Login
																													// button
		page.selectOption("#userSelect", "2");// Harry Potter
		page.click("body > div > div > div.ng-scope > div > form > button");// click login button

	}

	@Test
	public void DepositMoneyIntoAccount() throws Exception {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		System.out.println("website: " + page.title());
		page.click("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");
		page.selectOption("#userSelect", "3");// select Ron
		page.click("body > div > div > div.ng-scope > div > form > button");// click login button
		page.locator("[ng-click='deposit()']").click();// use attribute locator to click deposit button
		Thread.sleep(2 * 1000);
		page.locator("[placeholder='amount']").fill("5000");// use attribute locator to fill 5000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// click
																														// deposit
																														// button

	}

	@Test
	public void WithdrawMoneyFromAccount() throws Exception {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		System.out.println("website: " + page.title());
		page.click("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");
		page.selectOption("#userSelect", "4");// select Albus
		page.click("body > div > div > div.ng-scope > div > form > button");// click login button

		page.locator("[ng-click='deposit()']").click();// use attribute locator to click deposit button
		Thread.sleep(2 * 1000);
		page.locator("[placeholder='amount']").fill("5000");// use attribute locator to fill 5000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// click
																														// deposit
																														// button
		page.locator("[ng-class='btnClass3']").click();// use attribute to click withdraw button
		Thread.sleep(2 * 1000);
		page.locator("[ng-model='amount']").fill("3000");// use attribute to locate and fill 3000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// click
																														// withdraw
																														// button
	}

	@Test
	public void WithdrawMoneyWithInsufficientBalance() throws Exception {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		System.out.println("website: " + page.title());
		page.click("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");
		page.selectOption("#userSelect", "4");// select Albus
		page.click("body > div > div > div.ng-scope > div > form > button");// click login button

		page.locator("[ng-click='deposit()']").click();// use attribute locator to click deposit button
		Thread.sleep(2 * 1000);
		page.locator("[placeholder='amount']").fill("5000");// use attribute locator to fill 5000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// click
																														// deposit
																														// button
		page.locator("[ng-class='btnClass3']").click();// use attribute to click withdraw button
		Thread.sleep(2 * 1000);
		page.locator("[ng-model='amount']").fill("15000");
		Thread.sleep(2 * 1000);
		page.locator("[class='btn btn-default']").click();
	}

	@Test
	public void ViewTransactionHistory() throws Exception {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		System.out.println("website: " + page.title());
		page.click("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");
		page.selectOption("#userSelect", "5");// select Neville
		page.click("body > div > div > div.ng-scope > div > form > button");// click login button
		Thread.sleep(2 * 1000);
		page.locator("[ng-click='deposit()']").click();// use attribute locator to click deposit button
		Thread.sleep(2 * 1000);
		page.locator("[placeholder='amount']").fill("5000");// use attribute locator to fill 5000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// use
																														// CSS
																														// to
																														// click
																														// deposit
																														// button
		Thread.sleep(2 * 1000);
		page.locator("[ng-class='btnClass3']").click();// use attribute to click withdraw button
		Thread.sleep(2 * 1000);
		page.locator("[ng-model='amount']").fill("3000");// use attribute to locate and fill 3000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// click
																														// withdraw
																														// button
		Thread.sleep(2 * 1000);
		page.locator("[ng-model='amount']").fill("15000");// use attribute to fill 15000
		Thread.sleep(2 * 1000);
		page.locator("[class='btn btn-default']").click();// click withdraw button
		page.click("body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(1)");// click
																										// transaction
																										// button
	}

	@Test
	public void ResetTransactionHistory() throws Exception {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		System.out.println("website: " + page.title());
		page.click("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");
		page.selectOption("#userSelect", "5");// select Neville
		page.click("body > div > div > div.ng-scope > div > form > button");// click login button
		Thread.sleep(2 * 1000);
		page.locator("[ng-click='deposit()']").click();// use attribute locator to click deposit button
		Thread.sleep(2 * 1000);
		page.locator("[placeholder='amount']").fill("5000");// use attribute locator to fill 5000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// use
																														// CSS
																														// to
																														// click
																														// deposit
																														// button
		Thread.sleep(2 * 1000);
		page.locator("[ng-class='btnClass3']").click();// use attribute to click withdraw button
		Thread.sleep(2 * 1000);
		page.locator("[ng-model='amount']").fill("3000");// use attribute to locate and fill 3000
		Thread.sleep(2 * 1000);
		page.click(
				"body > div > div > div.ng-scope > div > div.container-fluid.mainBox.ng-scope > div > form > button");// click
																														// withdraw
																														// button
		Thread.sleep(2 * 1000);
		page.locator("[ng-model='amount']").fill("15000");// use attribute to fill 15000
		Thread.sleep(2 * 1000);
		page.locator("[class='btn btn-default']").click();// click withdraw button
		page.click("body > div > div > div.ng-scope > div > div:nth-child(5) > button:nth-child(1)");// click
																										// transaction
																										// button
		Thread.sleep(2 * 1000);
		page.click("body > div > div > div.ng-scope > div > div.fixedTopBox > button:nth-child(3)");// click reset
																									// button
	}

	@Test
	public void LogoutCustomer() throws InterruptedException {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		System.out.println("website: " + page.title());
		page.click("body > div > div > div.ng-scope > div > div.borderM.box.padT20 > div:nth-child(1) > button");
		page.selectOption("#userSelect", "5");// select Neville
		page.click("body > div > div > div.ng-scope > div > form > button");// click login button
		Thread.sleep(2 * 1000);
		page.click("body > div > div > div.box.mainhdr > button.btn.logout");// click logout button
	}
	
	
	private void blinkHighlight(Page page, Locator element) {
		// Repeat loop body 3 times
		for(int i = 0; i < 3; i++) {
			
			// Apply highlight
			element.evaluate("el => { el.style.border = '3px solid red'; el.style.backgroundColor = 'yellow'; }");
			page.waitForTimeout(500);
			// Remove highlight
			element.evaluate("el => { el.style.border = ''; el.style.backgroundColor = ''; }");
			page.waitForTimeout(500);
		}
		
		
		
	}
	
	
	
	
}


















