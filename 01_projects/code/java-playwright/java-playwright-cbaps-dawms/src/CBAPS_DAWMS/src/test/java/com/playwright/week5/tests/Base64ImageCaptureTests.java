package com.playwright.week5.tests;

import static org.assertj.core.api.Assertions.assertThat;

import org.testng.annotations.Test;

import com.playwright.week5.library.Base;

public class Base64ImageCaptureTests extends Base {

	@Test
	public void fileUploadTest1() {
		String webURL = "https://practice.expandtesting.com/upload";
		page.navigate(webURL);
		System.out.println("Page title: " + page.title());
		
		String fileLocation = "src/test/resources/testdata/dummy_test.txt";
		//String absolutePath = myPlaywright.getAbsoluteFilePath(fileLocation);
		
		myPlaywright.fileUpload(page.locator("#fileInput"), fileLocation);
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	@Test(enabled = false)
	public void imageCaptureTest() {
		// Step1. Go to page https://www.mortgageCalculator.org/");
		page.navigate("https://www.mortgagecalculator.org/");
		System.out.println("navigating to website");

		// Step2. Select "Home Value"
		page.fill("#homeval", "500000");

		//String actualTitle = page.title();
		//String expectedTitle = "Mortgage Calculator123";

		//assertThat(actualTitle).as("Title did not matched.").isEqualTo(expectedTitle);

		myPlaywright.sleep(5);

		// capture full page screenshot
		myPlaywright.captureScreenshotBase64();
		// myPlaywright.sleep(1);

	}
}
