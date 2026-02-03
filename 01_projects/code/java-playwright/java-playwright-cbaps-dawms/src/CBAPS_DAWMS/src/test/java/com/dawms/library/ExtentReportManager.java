package com.dawms.library;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import com.aventstack.extentreports.reporter.configuration.Theme;

/**
 * Manager class for Extent Reports.
 */
public class ExtentReportManager {

    private static ExtentReports extent;
    private static ThreadLocal<ExtentTest> test = new ThreadLocal<>();

    public static void initReports() {
        if (extent == null) {
            ExtentSparkReporter spark = new ExtentSparkReporter("target/extent-reports/report.html");
            spark.config().setTheme(Theme.STANDARD);
            spark.config().setDocumentTitle("CBAPS DAWMS Automation Report");
            spark.config().setReportName("Test Execution Report");

            extent = new ExtentReports();
            extent.attachReporter(spark);
            extent.setSystemInfo("Environment", "QA");
            extent.setSystemInfo("Browser", "Chromium");
        }
    }

    public static void createTest(String testName) {
        ExtentTest extentTest = extent.createTest(testName);
        test.set(extentTest);
    }

    public static ExtentTest getTest() {
        return test.get();
    }

    public static void logPass(String message) {
        getTest().pass(message);
    }

    public static void logFail(String message) {
        getTest().fail(message);
    }

    public static void logInfo(String message) {
        getTest().info(message);
    }

    public static void flushReports() {
        if (extent != null) {
            extent.flush();
        }
    }
}
