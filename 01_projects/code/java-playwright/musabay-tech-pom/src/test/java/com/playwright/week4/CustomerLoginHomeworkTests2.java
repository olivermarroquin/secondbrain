package com.playwright.week4;

import org.assertj.core.api.Assertions;
import org.testng.annotations.Test;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.LoadState;
import com.microsoft.playwright.options.WaitForSelectorState;
import com.playwright.week3.OldBase;

public class CustomerLoginHomeworkTests2 extends OldBase{

	@Test(priority = 1)

	public void CustomerLogin() {
		try {
		String XYZBankURL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login";
		page.navigate(XYZBankURL);
		
		System.out.println("Customer is logging in....");
		
		}catch (Exception e) {
			e.printStackTrace();
		}
		
	}

	
	@Test(priority = 2)

	public void CustomerDeposit() {
		try {	
		
		System.out.println("Customer deposit....");
		
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
	
	
}
