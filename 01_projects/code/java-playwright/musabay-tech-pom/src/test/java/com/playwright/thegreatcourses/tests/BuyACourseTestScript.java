package com.playwright.thegreatcourses.tests;

import static org.assertj.core.api.Assertions.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.Test;

import com.aventstack.extentreports.Status;
import com.playwright.thegreatcourses.pages.CheckOutPage;
import com.playwright.thegreatcourses.pages.HomePage;
import com.playwright.thegreatcourses.pages.ProceedToCheckoutPage;
import com.playwright.thegreatcourses.pages.ProductTypePage;
import com.playwright.thegreatcourses.pages.ProductTypes;
import com.playwright.thegreatcourses.pages.SearchCourseResultPage;
import com.playwright.week5.library.Base;

public class BuyACourseTestScript extends Base{

	private static final Logger log = LoggerFactory.getLogger(BuyACourseTestScript.class);
	
	@Test(enabled = false)
	public void ourNightSkyTest() {
		//extent report test object is created.
		test = extent.createTest("Buy a course test - single workflow.");
		
		HomePage homePage = new HomePage(page, myPlaywright);
		homePage.navigateToHomePage();
		addStepToReport("Step1: go to The Great Courses Website.");
		
		String websiteTitle = homePage.getTitle();
		addStepToReport("Step2: verify home page title: " + websiteTitle);
		//assertThat(websiteTitle).contains("The Great Course 2025");
		
		//homePage.searchACourse("Our Night Sky").selectSearchResultCourse();		
		SearchCourseResultPage scrPage = homePage.searchACourse("Our Night Sky");
		addStepToReport("Step3: search course -  'Our Night Sky'");
		
		ProductTypePage productTypePage = scrPage.selectSearchResultCourse();
		addStepToReport("Step4: Select the first course from result page.");
				
		productTypePage.selectProductType(ProductTypes.DVD);
		addStepToReport("Step5: selecting DVD option.");
		
		ProceedToCheckoutPage ptcoPage = productTypePage.clickAddToCartButton();
		addStepToReport("Step6: click on AddToCart button.");
		
		CheckOutPage checkOutPage = ptcoPage.clickProceedToCheckoutBtn();
		addStepToReport("Step7: click on ProceedToCheckout button.");
		
		String uniqueEmail = myPlaywright.getRandomEmail();
		String uniquePassword = myPlaywright.getRandomPassword("@$*", 8);		
		checkOutPage.createAccount(uniqueEmail, uniquePassword);
		addStepToReport("Step8: create new account: email > "+uniqueEmail + ", password > " + uniquePassword);
		
		checkOutPage.enterBillingAddressInfo();
		addStepToReport("Step9: enter billing address information using test data.");
		
		checkOutPage.verifyBillingInfo();
		addStepToReport("Step10: verify billing address information.");
		
		
	}
	
	
	@Test
	public void OriginsOfGreatAncientCivilizations() {
		//extent report test object is created.
		test = extent.createTest("Buy 'Origins of Great Ancient Civilizations' course test - single workflow.");
		
		HomePage homePage = new HomePage(page, myPlaywright);
		homePage.navigateToHomePage();
		addStepToReport("Step1: go to The Great Courses Website.");
		
		String websiteTitle = homePage.getTitle();
		addStepToReport("Step2: verify home page title: " + websiteTitle);
		//assertThat(websiteTitle).contains("The Great Course 2025");
		
		//homePage.searchACourse("Our Night Sky").selectSearchResultCourse();		
		SearchCourseResultPage scrPage = homePage.searchACourse("Origins of Great Ancient Civilizations");
		addStepToReport("Step3: search course -  'Origins of Great Ancient Civilizations'");
		
		ProductTypePage productTypePage = scrPage.selectSearchResultCourse();
		addStepToReport("Step4: Select the first course from result page.");
				
		productTypePage.selectProductType(ProductTypes.Instant_Audio);
		addStepToReport("Step5: selecting InstantAudio option.");
		
		ProceedToCheckoutPage ptcoPage = productTypePage.clickAddToCartButton();
		addStepToReport("Step6: click on AddToCart button.");
		
		CheckOutPage checkOutPage = ptcoPage.clickProceedToCheckoutBtn();
		addStepToReport("Step7: click on ProceedToCheckout button.");
		
		String uniqueEmail = myPlaywright.getRandomEmail();
		String uniquePassword = myPlaywright.getRandomPassword("@$*", 8);		
		checkOutPage.createAccount(uniqueEmail, uniquePassword);
		addStepToReport("Step8: create new account: email > "+uniqueEmail + ", password > " + uniquePassword);
		
		checkOutPage.enterBillingAddressInfo();
		addStepToReport("Step9: enter billing address information using test data.");
		
		checkOutPage.verifyBillingInfo();
		addStepToReport("Step10: verify billing address information.");
		
		
	}
	
	
	
	private void addStepToReport(String testStep) {
		test.log(Status.PASS, testStep);	
		log.info(testStep);
	}
	
	
	
	
}
