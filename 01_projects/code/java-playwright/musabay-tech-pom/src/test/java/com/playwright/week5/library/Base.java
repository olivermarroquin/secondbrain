package com.playwright.week5.library;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.ITestResult;
import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.AfterSuite;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeSuite;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.MediaEntityBuilder;
import com.aventstack.extentreports.Status;
import com.aventstack.extentreports.model.Media;
import com.microsoft.playwright.Page;

public class Base {
	private static final Logger log = LoggerFactory.getLogger(Base.class);

	public static ExtentReports extent;
	public static ExtentTest test;
	public PlaywrightManager myPlaywright;
	public Page page;

	@BeforeSuite
	public void setupReport() {
		extent = ExtentReportManager.getInstance();
	}
	
	@AfterSuite
	public void tearDownReport() {
		extent.flush();
		log.info("Log file location: " + "target/logs/automation.log");
		log.info("Screenshot location: " + "target/screenshot/");
		log.info("Video location: " + "target/videos/");
		log.info("Extent html report location: " + "target/report/");
	}
	
	@BeforeClass
	public void beforeTestClass() {
		log.info("Initializing Playwright object before test class.");

		myPlaywright = new PlaywrightManager();
		myPlaywright.initPlaywright();
	}

	@AfterClass
	public void afterTestClass() {
		myPlaywright.closePlaywright();
		log.info("Closing Playwright object after test class.");
	}

	@BeforeMethod
	public void setUp() {
		page = myPlaywright.openNewBrowserPage();
	}

	@AfterMethod
	public void tearDown(ITestResult result) {
		String testName = null;
		try {
			// capture screenshot only when test is failed
			testName = result.getMethod().getMethodName();
			if (result.getStatus() == ITestResult.FAILURE) {
				log.info("Test failed...");
				myPlaywright.captureScreenshotFullPage(testName);
				
				// add screenshot to the extent report
				String base64Image = myPlaywright.captureScreenshotBase64();
				Media reportBase64 = MediaEntityBuilder
						.createScreenCaptureFromBase64String(base64Image)
						.build();
				test.log(Status.FAIL, "Test failed with exception: " + result.getThrowable(), reportBase64);				
				
			}else if  (result.getStatus() == ITestResult.SUCCESS) {
				test.log(Status.PASS, "Test passed: " + testName);				
			}
			
			// attach video file link
			
			try {
				String videoPath = page.video().path().toString(); // .webm file path
				test.info("<a href='" + videoPath + "' target='_blank'>Click here to see video recording</a>");
			} catch (Exception e) {
				test.warning("Video not available: " + e.getMessage());
				log.error("Video not available: " + e.getMessage());
			}
			
			
			
			
			myPlaywright.closePage();

		} catch (Exception e) {
			log.error("Exception during test '{}' tearDown: {}", testName, e.getMessage(), e);
		} finally {
			if(page != null) {
				myPlaywright.closePage();
			}
		}
	}

}
