package com.playwright.week5.tests;

import static org.assertj.core.api.Assertions.assertThat;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.Test;

import com.aventstack.extentreports.Status;
import com.playwright.week5.library.Base;

public class MortgageCalculatorOrgTest extends Base {
	private static final Logger log = LoggerFactory.getLogger(MortgageCalculatorOrgTest.class);
	
	@Test
	public void buyAnotherSingleHouseTest_3() {
		
		test = extent.createTest("Mortage Calculator - Buy a single house");
		
		// Step1. 
		page.navigate("https://www.mortgagecalculator.org/");
		test.log(Status.PASS, "Step 1: Website navigation - successful");	
		log.info("Step 1: Website navigation - sucessful");
				
		// Step2. 
		myPlaywright.enterText(page.locator("#homeval"), "500000");
		test.log(Status.PASS, "Step 2: Enter home value 500,000 - successful");
		log.info("Step 2: Enter home value 500,000 - successful");
				
		// Step3. 		
		myPlaywright.selectCheckBoxOrRadioButton(page.getByLabel("%"));
		test.log(Status.PASS, "Step 3: Select Downpayment % - successful");
		log.info("Step 3: Select Downpayment % - successful");
		
		// Step4.			
		myPlaywright.enterText(page.locator("#downpayment"), "3.5");
		test.log(Status.PASS, "Step 4: Enter down payment percent 3.5 - successful");
		log.info("Step 4: Enter down payment percent 3.5 - successful");
		
		// Step5.
		myPlaywright.enterText(page.locator("#loanamt"), "75000");
		test.log(Status.PASS, "Step 5: Enter loan amount 75000 - successful");
		log.info("Step 5: Enter loan amount 75000 - successful");
		
		// Step6.
		myPlaywright.enterText(page.locator("#intrstsrate"), "6.5"); 
		test.log(Status.PASS, "Step 6: Enter interest rate 6.5 - successful");
		log.info("Step 6: Enter interest rate 6.5 - successful");
		
		// Step7.
		myPlaywright.enterText(page.locator("#loanterm"), "29");
		test.log(Status.PASS, "Step 7: Enter loan term 29 years - successful");
		log.info("Step 7: Enter loan term 29 years - successful");
		
		// Step8.
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(8) > select"), "Mar");
		test.log(Status.PASS, "Step 8: Select start month: Mar - successful");
		log.info("Step 8: Select start month: Mar - successful");
		
		// Step9.
		myPlaywright.enterText(page.locator("#start_year"), "2025");
		test.log(Status.PASS, "Step 9: Select start year: 2025 - successful");
		log.info("Step 9: Select start year: 2025 - successful");
		
		
		// Step10.
		myPlaywright.enterText(page.locator("#pptytax"), "2500");
		test.log(Status.PASS, "Step 10: Enter property tax $2,510 - successful");
		log.info("Step 10: Enter property tax $2,510 - successful");
		
		
		// Step11. 				
		myPlaywright.enterText(page.locator("#pmi"), "0.05");
		test.log(Status.PASS, "Step 11: Enter PMI 0.05 - successful");
		log.info("Step 11: Enter PMI 0.05 - successful");
				
		// Step12. 		
		myPlaywright.enterText(page.locator("#hoi"), "1200");
		test.log(Status.PASS, "Step 12: Enter home insurance $1,200 - successful");
		log.info("Step 12: Enter home insurance $1,200 - successful");
				
	
		// Step13.
		myPlaywright.enterText(page.locator("#hoa"), "100");
		test.log(Status.PASS, "Step 13: Enter monthly HOA $100 - successful");
		log.info("Step 13: Enter monthly HOA $100 - successful");
		
		
		// Step14.		
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(13) > select"), "FHA");
		test.log(Status.PASS, "Step 14: Select Loan Type FHA - successful");
		log.info("Step 14: Select Loan Type FHA - successful");
		myPlaywright.sleep(0.5);
		
		// Step15.		
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(16) > select"), "Buy");
		test.log(Status.PASS, "Step 15: Select Buy - successful");
		log.info("Step 15: Select Buy - successful");
		myPlaywright.sleep(0.5);
			
		// Step16.
		myPlaywright.clickElement(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div.rw-box.button > input"));
		test.log(Status.PASS, "Step 16: Click button Calculate - successful");
		log.info("Step 16: Click button Calculate - successful");
		
	}
	
	@Test
	public void buyAnotherSingleHouseTest_1() {
		
		test = extent.createTest("Mortage Calculator - Buy a single house");
		
		// Step1. 
		page.navigate("https://www.mortgagecalculator.org/");
		test.log(Status.PASS, "Step 1: Website navigation - successful");	
		log.info("Step 1: Website navigation - sucessful");
				
		// Step2. 
		myPlaywright.enterText(page.locator("#homeval"), "500000");
		test.log(Status.PASS, "Step 2: Enter home value 500,000 - successful");
		log.info("Step 2: Enter home value 500,000 - successful");
				
		// Step3. 		
		myPlaywright.selectCheckBoxOrRadioButton(page.getByLabel("%"));
		test.log(Status.PASS, "Step 3: Select Downpayment % - successful");
		log.info("Step 3: Select Downpayment % - successful");
		
		// Step4.			
		myPlaywright.enterText(page.locator("#downpayment"), "3.5");
		test.log(Status.PASS, "Step 4: Enter down payment percent 3.5 - successful");
		log.info("Step 4: Enter down payment percent 3.5 - successful");
		
		// Step5.
		myPlaywright.enterText(page.locator("#loanamt"), "75000");
		test.log(Status.PASS, "Step 5: Enter loan amount 75000 - successful");
		log.info("Step 5: Enter loan amount 75000 - successful");
		
		// Step6.
		myPlaywright.enterText(page.locator("#intrstsrate"), "6.5"); 
		test.log(Status.PASS, "Step 6: Enter interest rate 6.5 - successful");
		log.info("Step 6: Enter interest rate 6.5 - successful");
		
		// Step7.
		myPlaywright.enterText(page.locator("#loanterm"), "29");
		test.log(Status.PASS, "Step 7: Enter loan term 29 years - successful");
		log.info("Step 7: Enter loan term 29 years - successful");
		
		// Step8.
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(8) > select"), "Mar");
		test.log(Status.PASS, "Step 8: Select start month: Mar - successful");
		log.info("Step 8: Select start month: Mar - successful");
		
		// Step9.
		myPlaywright.enterText(page.locator("#start_year"), "2025");
		test.log(Status.PASS, "Step 9: Select start year: 2025 - successful");
		log.info("Step 9: Select start year: 2025 - successful");
		
		
		// Step10.
		myPlaywright.enterText(page.locator("#pptytax"), "2500");
		test.log(Status.PASS, "Step 10: Enter property tax $2,510 - successful");
		log.info("Step 10: Enter property tax $2,510 - successful");
		
		
		// Step11. 				
		myPlaywright.enterText(page.locator("#pmi"), "0.05");
		test.log(Status.PASS, "Step 11: Enter PMI 0.05 - successful");
		log.info("Step 11: Enter PMI 0.05 - successful");
				
		// Step12. 		
		myPlaywright.enterText(page.locator("#hoi"), "1200");
		test.log(Status.PASS, "Step 12: Enter home insurance $1,200 - successful");
		log.info("Step 12: Enter home insurance $1,200 - successful");
				
	
		// Step13.
		myPlaywright.enterText(page.locator("#hoa"), "100");
		test.log(Status.PASS, "Step 13: Enter monthly HOA $100 - successful");
		log.info("Step 13: Enter monthly HOA $100 - successful");
		
		
		// Step14.		
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(13) > select"), "FHA");
		test.log(Status.PASS, "Step 14: Select Loan Type FHA - successful");
		log.info("Step 14: Select Loan Type FHA - successful");
		myPlaywright.sleep(0.5);
		
		// Step15.		
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(16) > select"), "Buy");
		test.log(Status.PASS, "Step 15: Select Buy - successful");
		log.info("Step 15: Select Buy - successful");
		myPlaywright.sleep(0.5);
			
		// Step16.
		myPlaywright.clickElement(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div.rw-box.button > input"));
		test.log(Status.PASS, "Step 16: Click button Calculate - successful");
		log.info("Step 16: Click button Calculate - successful");
		
	}

	
	@Test
	public void buyAnotherSingleHouseTest_2() {
		
		test = extent.createTest("Mortage Calculator - Buy a single house");
		
		// Step1. 
		page.navigate("https://www.mortgagecalculator.org/");
		test.log(Status.PASS, "Step 1: Website navigation - successful");	
		log.info("Step 1: Website navigation - sucessful");
				
		// Step2. 
		myPlaywright.enterText(page.locator("#homeval"), "500000");
		test.log(Status.PASS, "Step 2: Enter home value 500,000 - successful");
		log.info("Step 2: Enter home value 500,000 - successful");
				
		// Step3. 		
		myPlaywright.selectCheckBoxOrRadioButton(page.getByLabel("%"));
		test.log(Status.PASS, "Step 3: Select Downpayment % - successful");
		log.info("Step 3: Select Downpayment % - successful");
		
		// Step4.			
		myPlaywright.enterText(page.locator("#downpayment"), "3.5");
		test.log(Status.PASS, "Step 4: Enter down payment percent 3.5 - successful");
		log.info("Step 4: Enter down payment percent 3.5 - successful");
		
		// Step5.
		myPlaywright.enterText(page.locator("#loanamt"), "75000");
		test.log(Status.PASS, "Step 5: Enter loan amount 75000 - successful");
		log.info("Step 5: Enter loan amount 75000 - successful");
		
		// Step6.
		myPlaywright.enterText(page.locator("#intrstsrate123"), "6.5"); // make this test fail by changing locator
		test.log(Status.PASS, "Step 6: Enter interest rate 6.5 - successful");
		log.info("Step 6: Enter interest rate 6.5 - successful");
		
		// Step7.
		myPlaywright.enterText(page.locator("#loanterm"), "29");
		test.log(Status.PASS, "Step 7: Enter loan term 29 years - successful");
		log.info("Step 7: Enter loan term 29 years - successful");
		
		// Step8.
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(8) > select"), "Mar");
		test.log(Status.PASS, "Step 8: Select start month: Mar - successful");
		log.info("Step 8: Select start month: Mar - successful");
		
		// Step9.
		myPlaywright.enterText(page.locator("#start_year"), "2025");
		test.log(Status.PASS, "Step 9: Select start year: 2025 - successful");
		log.info("Step 9: Select start year: 2025 - successful");
		
		
		// Step10.
		myPlaywright.enterText(page.locator("#pptytax"), "2500");
		test.log(Status.PASS, "Step 10: Enter property tax $2,510 - successful");
		log.info("Step 10: Enter property tax $2,510 - successful");
		
		
		// Step11. 				
		myPlaywright.enterText(page.locator("#pmi"), "0.05");
		test.log(Status.PASS, "Step 11: Enter PMI 0.05 - successful");
		log.info("Step 11: Enter PMI 0.05 - successful");
				
		// Step12. 		
		myPlaywright.enterText(page.locator("#hoi"), "1200");
		test.log(Status.PASS, "Step 12: Enter home insurance $1,200 - successful");
		log.info("Step 12: Enter home insurance $1,200 - successful");
				
	
		// Step13.
		myPlaywright.enterText(page.locator("#hoa"), "100");
		test.log(Status.PASS, "Step 13: Enter monthly HOA $100 - successful");
		log.info("Step 13: Enter monthly HOA $100 - successful");
		
		
		// Step14.		
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(13) > select"), "FHA");
		test.log(Status.PASS, "Step 14: Select Loan Type FHA - successful");
		log.info("Step 14: Select Loan Type FHA - successful");
		myPlaywright.sleep(0.5);
		
		// Step15.		
		myPlaywright.selectDropdown(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(16) > select"), "Buy");
		test.log(Status.PASS, "Step 15: Select Buy - successful");
		log.info("Step 15: Select Buy - successful");
		myPlaywright.sleep(0.5);
			
		// Step16.
		myPlaywright.clickElement(page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div.rw-box.button > input"));
		test.log(Status.PASS, "Step 16: Click button Calculate - successful");
		log.info("Step 16: Click button Calculate - successful");
		
	}

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	@Test(enabled = false)
	public void buyASingleHouseTest1() {
		// Step1. Go to page https://www.mortgageCalculator.org/");
		page.navigate("https://www.mortgagecalculator.org/");
		System.out.println("navigating to website");

		// Step2. Select "Home Value"
		page.fill("#homeval", "500000");

		String actualTitle = page.title();
		String expectedTitle = "Mortgage Calculator123";

		assertThat(actualTitle).as("Title did not matched.").isEqualTo(expectedTitle);

		myPlaywright.sleep(5);

		// capture full page screenshot
		myPlaywright.captureScreenshotFullPage("fullPage1");
		// myPlaywright.sleep(1);

		// myPlaywright.captureScreenshotDisplayViewPage("DisplayPage");
	}
}
