package com.dawms.library;

import java.lang.reflect.Method;

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

/**
 * Base: TestNG base class for CBAPS automation
 * Manages lifecycle: initialization, setup, teardown, reporting
 * Tests extend this class to inherit common setup/teardown behavior
 */
public class Base {
	private static final Logger log = LoggerFactory.getLogger(Base.class);

	// PlaywrightManager wrapper (owns Playwright/Browser/Context/Page)
	public PlaywrightManager myPlaywright;
	
	// Current test's Page
	public Page page;
	
	// ExtentReports: report container for entire run (suite)
	public static ExtentReports extent;
	
	// ExtentTest: single test case entry inside the report
	public static ExtentTest test;

	/**
	 * Suite-level initialization - create ExtentReports instance
	 */
	@BeforeSuite
	public void setupReport() {
		extent = ExtentReportManager.getInstance();
		log.info("ExtentReports initialized for CBAPS automation.");
	}
	
	/**
	 * Suite-level teardown - flush report output
	 */
	@AfterSuite
	public void tearDownReport() {
		extent.flush();
		log.info("Log file location: target/logs/automation.log");
		log.info("Screenshot location: target/screenshot/");
		log.info("Video location: target/videos/");
		log.info("Extent HTML report location: target/report/");
	}
	
	/**
	 * Class-level initialization - create Playwright + Browser + Context ONCE per class
	 */
	@BeforeClass
	public void beforeTestClass() {
		log.info("Initializing Playwright object before test class.");
		myPlaywright = new PlaywrightManager();
		myPlaywright.initPlaywright();
	}

	/**
	 * Class-level teardown - close Playwright resources
	 */
	@AfterClass
	public void afterTestClass() {
		myPlaywright.closePlaywright();
		log.info("Closing Playwright object after test class.");
	}

	/**
	 * Method-level setup - create new Page for each test method (isolation)
	 */
	@BeforeMethod
	public void setUp(Method method) {
		page = myPlaywright.openNewBrowserPage();
		
		// Create test node in report
		test = extent.createTest(method.getName());
		log.info("Starting test: " + method.getName());
	}

	/**
	 * Method-level teardown - capture evidence on failure, close page
	 */
	@AfterMethod
	public void tearDown(ITestResult result) {
		String testName = null;
		try {
			testName = result.getMethod().getMethodName();
			
			if (result.getStatus() == ITestResult.FAILURE) {
				log.info("Test failed: " + testName);
				myPlaywright.captureScreenshotFullPage(testName);
				
				// Add screenshot to ExtentReports
				String base64Image = myPlaywright.captureScreenshotBase64();
				Media reportBase64 = MediaEntityBuilder
						.createScreenCaptureFromBase64String(base64Image)
						.build();
				test.log(Status.FAIL, "Test failed with exception: " + result.getThrowable(), reportBase64);				
				
			} else if (result.getStatus() == ITestResult.SUCCESS) {
				test.log(Status.PASS, "Test passed: " + testName);				
			}
			
			// Attach video file link
			try {
				String videoPath = page.video().path().toString();
				test.info("<a href='" + videoPath + "' target='_blank'>Click here to see video recording</a>");
			} catch (Exception e) {
				test.warning("Video not available: " + e.getMessage());
				log.error("Video not available: " + e.getMessage());
			}
			
			myPlaywright.closePage();

		} catch (Exception e) {
			log.error("Exception during test '{}' tearDown: {}", testName, e.getMessage(), e);
		} finally {
			if (page != null) {
				myPlaywright.closePage();
			}
		}
	}
	
	/**
	 * Helper method to log test steps in ExtentReports and console
	 */
	protected void addStepToReport(String testStep) {
		test.log(Status.PASS, testStep);	
		log.info(testStep);
	}
}
