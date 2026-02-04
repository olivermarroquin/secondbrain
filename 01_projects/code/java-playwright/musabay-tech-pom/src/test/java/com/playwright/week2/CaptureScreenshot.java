package com.playwright.week2;

import java.nio.file.Paths;

import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import org.xml.sax.ext.Locator2Impl;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.BrowserType.LaunchOptions;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;

public class CaptureScreenshot {
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
		//page.setViewportSize(1280, 720);
		System.out.println("Open chrome browser.");
	}

	@AfterMethod
	public void tearDown() {
		page.close();
		System.out.println("closing chrome browser.");
	}
	
	@Test(enabled = false)
	public void screenshot_FullPage() {
		page.navigate("https://www.mortgagecalculator.org/");
		System.out.println("navigating to website");
		
		// capture full page screenshot
		page.screenshot(new Page.ScreenshotOptions()
				.setPath(Paths.get("C:/playwright/screenshots/fullpage.png"))				
				.setFullPage(true));
	}
	
	@Test(enabled = false)
	public void screenshot_pageView() {
		page.navigate("https://www.mortgagecalculator.org/");
		System.out.println("navigating to website");
		
		// capture displayed view of web-site screenshot
		page.screenshot(new Page.ScreenshotOptions()
				.setPath(Paths.get("C:/playwright/screenshots/view-page.png")));
				
	}
	
	@Test
	public void screenshot_webelement() {
		page.navigate("https://www.mortgagecalculator.org/");
		System.out.println("navigating to website");
		
		String buttonCSS = "div.cal-content > div.cal-left-box > div.calcu-block > div:nth-child(5) > a > input";
		Locator button = page.locator(buttonCSS);
		button.screenshot(new Locator.ScreenshotOptions()
				.setPath(Paths.get("C:/playwright/screenshots/button.png")));			
				
	}
	
	
	// There is another option to capture screenshot 
	// only when a test is failed
	// we will cover this later
	
	
	
	
	
	
	
	
}
