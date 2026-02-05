package com.playwright.cbaps.library;

import org.testng.ITestResult;
import org.testng.annotations.*;
import com.aventstack.extentreports.*;
import com.microsoft.playwright.Page;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Enhanced Base class for TestNG with ExtentReports integration
 */
public class Base {
    private static final Logger log = LoggerFactory.getLogger(Base.class);
    
    protected static ExtentReports extent;
    protected ExtentTest test;
    protected EnhancedPlaywrightManager pwm;
    protected Page page;
    
    private String browser = System.getProperty("browser", "chromium");
    private boolean headless = Boolean.parseBoolean(System.getProperty("headless", "false"));
    
    @BeforeSuite
    public void setupSuite() {
        extent = ExtentManager.getInstance();
        log.info("✅ Test Suite Started");
    }
    
    @AfterSuite
    public void tearDownSuite() {
        if (extent != null) extent.flush();
        log.info("✅ Test Suite Completed");
        log.info("📊 Report: target/extent-reports/extent-report.html");
    }
    
    @BeforeClass
    public void setupClass() {
        pwm = new EnhancedPlaywrightManager();
        pwm.initPlaywright(browser, headless);
        log.info("✅ Browser initialized: {}", browser);
    }
    
    @AfterClass
    public void tearDownClass() {
        if (pwm != null) pwm.closePlaywright();
        log.info("✅ Browser closed");
    }
    
    @BeforeMethod
    public void setupTest(java.lang.reflect.Method method) {
        page = pwm.openNewBrowserPage();
        test = extent.createTest(method.getName());
        test.assignCategory("Automation Test");
        log.info("🚀 Test Started: {}", method.getName());
    }
    
    @AfterMethod
    public void tearDownTest(ITestResult result) {
        try {
            if (result.getStatus() == ITestResult.FAILURE) {
                log.error("❌ Test Failed: {}", result.getMethod().getMethodName());
                String screenshot = pwm.captureScreenshotBase64();
                test.fail("Test Failed: " + result.getThrowable(),
                    MediaEntityBuilder.createScreenCaptureFromBase64String(screenshot).build());
            } else if (result.getStatus() == ITestResult.SUCCESS) {
                log.info("✅ Test Passed");
                test.pass("Test Passed");
            }
        } finally {
            if (pwm != null) pwm.closePage();
        }
    }
    
    protected void addStepToReport(String step) {
        test.log(Status.INFO, step);
        log.info("📋 {}", step);
    }
    
    protected void addPassToReport(String msg) {
        test.log(Status.PASS, "✅ " + msg);
        log.info("✅ {}", msg);
    }
}
