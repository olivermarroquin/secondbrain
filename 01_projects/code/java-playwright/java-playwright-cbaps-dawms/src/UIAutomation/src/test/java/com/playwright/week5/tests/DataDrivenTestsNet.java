package com.playwright.week5.tests;

import static org.assertj.core.api.Assertions.assertThat;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import com.microsoft.playwright.Locator;
import com.playwright.week5.library.Base;
import com.playwright.week5.library.ExcelManager;

public class DataDrivenTestsNet extends Base {

	private static final Logger log = LoggerFactory.getLogger(Base.class);

	@DataProvider(name = "MortgageTestDataSet1")
	private Object[][] getCalculatorData() {
		Object[][] data = null;
		ExcelManager excelManager = new ExcelManager("src/test/resources/testdata/CalculaterTestData2.xlsx",
				"MortgageData1");
		data = excelManager.getExcelData();
		return data;
	}

	@Test(dataProvider = "MortgageTestDataSet1")
	public void buyASingleHouseTest(String mortgageAmount, String mortgagePeriodYear, String mortgagePeriodMonth,
			String intYear, String intMonth, String intType, String intRate, String startMonth, String startYear,
			String paymentPeriod, String expectedResult

	) {
		page.navigate("https://www.mortgagecalculator.net/");
		System.out.println("navigating to website");
		page.locator("#currency").selectOption("$");
		page.fill("#amount", mortgageAmount);
		page.fill("#amortizationYears", mortgagePeriodYear);
		page.fill("#amortizationMonths", mortgagePeriodMonth);

		page.fill("#interestTermYears", intYear);
		page.fill("#interestTermMonths", intMonth);
		page.selectOption("#interestType", intType);
		page.fill("#rate", intRate);
		page.selectOption("#startMonth", startMonth);
		page.selectOption("#startYear", startYear);
		page.selectOption("#paymentMode", paymentPeriod);
		page.click("#button");

		myPlaywright.sleep(5);

		Locator monthlyPayment = page
				.locator("div.mortageTableWrapper > table > tbody > tr:nth-child(1) > td:nth-child(2)");
		String actualResult = monthlyPayment.innerText();
		System.out.println("actual monthly payment: " + actualResult);

		assertThat(actualResult).as("Monthly payment did not matched.").isEqualTo(expectedResult);
		// page.pause();
	}

}
