package com.playwright.week3;

import java.util.Arrays;

import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.microsoft.playwright.BrowserType.LaunchOptions;

public class OldBase {
	private Playwright playwright;
	private Browser browser;
	private BrowserContext context;
	public Page page;

	@BeforeClass
	public void beforeTestClass() {
		playwright = Playwright.create();
		LaunchOptions launchOption = new BrowserType.LaunchOptions().setChannel("chrome");
		launchOption.setArgs(Arrays.asList("--start-maximized")).setHeadless(false);
			
		browser = playwright.chromium().launch(launchOption);
		context = browser.newContext(new Browser.NewContextOptions().setViewportSize(null));
		System.out.println("Create playwright & browser objects.");
	}

	@AfterClass
	public void afterTestClass() {
		//context.close();
		browser.close();
		playwright.close();
		System.out.println("Cleaning up playwright & browser objects.");
	}

	@BeforeMethod
	public void setUp() throws Exception {		
		page = context.newPage();		
		Thread.sleep(5 * 1000);
		//page.setViewportSize(1280, 720);
		System.out.println("Open chrome browser.");
	}

	@AfterMethod
	public void tearDown() throws Exception {
		Thread.sleep(8 * 1000);
		page.close();
		System.out.println("closing chrome browser.");
	}
}
