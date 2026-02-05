package com.automation.cbaps.library;

import org.testng.ITestResult;
import org.testng.annotations.*;
import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.MediaEntityBuilder;
import com.aventstack.extentreports.Status;
import org.openqa.selenium.WebDriver;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Base Test Class - Foundation for all test classes
 * Manages browser lifecycle, reporting, and common test setup/teardown
 */
public class Base {
    private static final Logger log = LogManager.getLogger(Base.class);
    
    protected static ExtentReports extent;
    protected ExtentTest test;
    protected GlobalSelenium gs;
    protected WebDriver driver;
    
    private String browser = System.getProperty("browser", "chrome");
    private boolean headless = Boolean.parseBoolean(System.getProperty("headless", "false"));
    
    @BeforeSuite
    public void setupSuite() {
        extent = ExtentManager.getInstance();
        log.info("✅ Test Suite Started - ExtentReports initialized");
    }
    
    @AfterSuite
    public void tearDownSuite() {
        if (extent != null) {
            extent.flush();
        }
        log.info("✅ Test Suite Completed - Reports generated");
        log.info("📊 Report Location: target/extent-reports/extent-report.html");
        log.info("📝 Log Location: target/logs/automation.log");
    }
    
    @BeforeClass
    public void setupClass() {
        gs = new GlobalSelenium();
        gs.setHeadless(headless);
        gs.setDemoMode(false); // Set to true for visual highlighting
        log.info("✅ Test Class initialized - Browser: " + browser);
    }
    
    @AfterClass
    public void tearDownClass() {
        log.info("✅ Test Class completed");
    }
    
    @BeforeMethod
    public void setupTest(java.lang.reflect.Method method) {
        // Initialize browser for each test
        driver = initializeBrowser();
        
        // Create test node in ExtentReports
        test = extent.createTest(method.getName());
        test.assignCategory("Automation Test");
        test.assignAuthor("QA Team");
        
        log.info("🚀 Test Started: " + method.getName());
    }
    
    @AfterMethod
    public void tearDownTest(ITestResult result) {
        String testName = result.getMethod().getMethodName();
        
        try {
            if (result.getStatus() == ITestResult.FAILURE) {
                log.error("❌ Test Failed: " + testName);
                
                // Capture screenshot
                gs.capureScreenshot(testName, "target/screenshots/");
                String base64Screenshot = gs.captureScreenshotBase64();
                
                // Add to report
                test.fail("Test Failed: " + result.getThrowable(),
                    MediaEntityBuilder.createScreenCaptureFromBase64String(base64Screenshot).build());
                
            } else if (result.getStatus() == ITestResult.SUCCESS) {
                log.info("✅ Test Passed: " + testName);
                test.pass("Test Passed Successfully");
                
            } else if (result.getStatus() == ITestResult.SKIP) {
                log.warn("⚠️ Test Skipped: " + testName);
                test.skip("Test Skipped: " + result.getThrowable());
            }
            
        } catch (Exception e) {
            log.error("Error in teardown: " + e.getMessage());
        } finally {
            // Close browser
            if (gs != null) {
                gs.cleanUpAfterEachTest();
            }
        }
    }
    
    /**
     * Initialize browser based on system property
     */
    private WebDriver initializeBrowser() {
        switch (browser.toLowerCase()) {
            case "firefox":
                return gs.startAFirefoxBrowser();
            case "edge":
                return gs.startAEdgeBrowser();
            case "safari":
                return gs.startASafariBrowser();
            case "chrome":
            default:
                return gs.startAChromeBrowser();
        }
    }
    
    /**
     * Helper method to add test steps to report
     */
    protected void addStepToReport(String stepDescription) {
        test.log(Status.INFO, stepDescription);
        log.info("📋 " + stepDescription);
    }
    
    protected void addPassToReport(String message) {
        test.log(Status.PASS, "✅ " + message);
        log.info("✅ " + message);
    }
    
    protected void addWarningToReport(String message) {
        test.log(Status.WARNING, "⚠️ " + message);
        log.warn("⚠️ " + message);
    }
}
