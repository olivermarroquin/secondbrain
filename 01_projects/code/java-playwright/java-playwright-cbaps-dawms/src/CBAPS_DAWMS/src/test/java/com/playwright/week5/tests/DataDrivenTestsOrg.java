package com.playwright.week5.tests;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import com.playwright.week5.library.Base;
import com.playwright.week5.library.ExcelManager;

public class DataDrivenTestsOrg extends Base{

	private static final Logger log = LoggerFactory.getLogger(Base.class);
	
	@DataProvider (name = "MortgageTestDataSet1")
	private Object[][] getCalculatorData(){
		Object[][] data = null;
		ExcelManager excelManager = new ExcelManager(
				"src/test/resources/testdata/CalculaterTestData2.xlsx", "MortgageData1");
		data = excelManager.getExcelData();
		return data;
	}
	
	
		
	
	@Test
	public void buyASingleHouseTest(
			String mortgageAmount,
			String downPayment,
			String mortgagePeriodYear,
			String mortgagePeriodMonth,
			String intYear,
			String intMonth,
			String intType,
			String intRate,
			String startMonth,
			String startYear,
			String paymentPeriod,
			String expectedResult			
			
			) {
		// Step1. Go to page https://www.mortgageCalculator.net/");
		page.navigate("https://www.mortgagecalculator.org/");
		System.out.println("navigating to website");

		// Step2. Select "Home Value"
		// page.fill("#homeval","500000");
		myPlaywright.enterText(page.locator("#homeval"), mortgageAmount);

		// Step3. Enter "Down Payment "
		// page.getByLabel("%").check();
		myPlaywright.selectCheckBoxOrRadioButton(page.locator(
				"div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(2) > span > label:nth-child(2) > input[type=radio]"));

		// page.fill("#downpayment", "3.5");
		myPlaywright.enterText(page.locator("#downpayment"), downPayment);

		// Step4. Enter "Loan Amount"
		// page.fill("#loanamt", "750000");
		myPlaywright.enterText(page.locator("#loanamt"), "75000");

		// Step5. Enter "Interest Rate"
		// page.fill("#intrstsrate", "3.75");
		myPlaywright.enterText(page.locator("#intrstsrate"), "6.5");

		// Step6. Enter "Loan Term"
		// page.fill("#loanterm", "31");
		myPlaywright.enterText(page.locator("#loanterm"), "29");

		// Step7. Enter "Start Date:" Month and Year
		// page.selectOption("div.calculation-container > div > div > div.cal-content >
		// div.cal-left-box > div.calcu-block > div:nth-child(8) > select", "Mar");
		myPlaywright.selectDropdown(
				page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(8) > select"),
				"Mar");

		// page.fill("#start_year", "2025");
		myPlaywright.enterText(page.locator("#start_year"), "2025");

		// Step8. Enter "Property Tax"
		// page.fill("#pptytax", "2500");
		myPlaywright.enterText(page.locator("#pptytax"), "2500");

		// Step9. Enter "PMI"
		// page.fill("#pmi", ".05");
		myPlaywright.enterText(page.locator("#pmi"), "0.05");

		// Step10. Enter "Home Ins"
		// page.fill("#hoi", "1200");
		myPlaywright.enterText(page.locator("#hoi"), "1200");

		// Step11. Enter "Monthly HOA"
		// page.fill("#hoa", "100");
		myPlaywright.enterText(page.locator("#hoa"), "100");

		// Step12. Enter "Loan Type"
		// page.selectOption("#calc > form > section > section.content-area > div > div
		// > div.calculation-container > div > div > div.cal-content > div.cal-left-box
		// > div.calcu-block > div:nth-child(13) > select", "FHA");
		myPlaywright.selectDropdown(
				page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(13) > select"),
				"FHA");

		// Step13. Enter "Buy or Refi"
		// page.selectOption("#calc > form > section > section.content-area > div > div
		// > div.calculation-container > div > div > div.cal-content > div.cal-left-box
		// > div.calcu-block > div:nth-child(16) > select", "Buy");
		myPlaywright.selectDropdown(
				page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(16) > select"),
				"Buy");
		myPlaywright.sleep(3);

		// Step14. Enter "Calculate" button
		// page.click("#calc > form > section > section.content-area > div > div >
		// div.calculation-container > div > div > div.cal-content > div.cal-left-box >
		// div.calcu-block > div.rw-box.button > input");
		myPlaywright.clickElement(
				page.locator("div.cal-content > div.cal-left-box > div.calcu-block > div.rw-box.button > input"));
		myPlaywright.sleep(5);
		
		
		
	}
	
}
