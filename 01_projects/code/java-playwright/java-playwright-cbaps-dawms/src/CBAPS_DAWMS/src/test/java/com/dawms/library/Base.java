package com.dawms.library;

import com.microsoft.playwright.*;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.AfterSuite;

import java.nio.file.Paths;

/**
 * Base class for all test classes providing Playwright setup and teardown.
 */
public class Base {

    protected static Playwright playwright;
    protected static Browser browser;
    protected BrowserContext context;
    protected Page page;

    @BeforeSuite
    public void launchBrowser() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(new BrowserType.LaunchOptions()
                .setHeadless(false)
                .setSlowMo(100));
    }

    @AfterSuite
    public void closeBrowser() {
        if (browser != null) {
            browser.close();
        }
        if (playwright != null) {
            playwright.close();
        }
    }

    @BeforeMethod
    public void createContextAndPage() {
        context = browser.newContext(new Browser.NewContextOptions()
                .setRecordVideoDir(Paths.get("target/videos/")));
        page = context.newPage();
    }

    @AfterMethod
    public void closeContext() {
        if (context != null) {
            context.close();
        }
    }

    /**
     * Navigate to a URL.
     */
    protected void navigateTo(String url) {
        page.navigate(url);
    }

    /**
     * Capture a screenshot with a given name.
     */
    protected void captureScreenshot(String name) {
        page.screenshot(new Page.ScreenshotOptions()
                .setPath(Paths.get("target/screenshots/" + name + ".png"))
                .setFullPage(true));
    }
}
