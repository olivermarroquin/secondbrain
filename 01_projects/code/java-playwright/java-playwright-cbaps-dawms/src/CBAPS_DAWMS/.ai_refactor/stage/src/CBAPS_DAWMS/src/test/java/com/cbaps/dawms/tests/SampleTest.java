package com.cbaps.dawms.tests;

import com.cbaps.dawms.library.Base;
import com.cbaps.dawms.library.ExtentReportManager;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

/**
 * Sample test class demonstrating the framework structure.
 */
public class SampleTest extends Base {

    @BeforeClass
    public void setupReports() {
        ExtentReportManager.initReports();
    }

    @Test
    public void testGoogleTitle() {
        ExtentReportManager.createTest("Google Title Test");
        navigateTo("https://www.google.com");
        String title = page.title();
        Assert.assertTrue(title.contains("Google"), "Title should contain 'Google'");
        ExtentReportManager.logPass("Google page title verified: " + title);
    }

    @AfterClass
    public void teardownReports() {
        ExtentReportManager.flushReports();
    }
}
