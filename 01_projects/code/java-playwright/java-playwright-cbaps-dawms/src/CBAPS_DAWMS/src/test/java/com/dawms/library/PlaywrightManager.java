package com.dawms.library;

import com.microsoft.playwright.*;

import java.nio.file.Paths;

/**
 * Singleton manager for Playwright browser instances.
 */
public class PlaywrightManager {

    private static PlaywrightManager instance;
    private Playwright playwright;
    private Browser browser;
    private BrowserContext context;
    private Page page;

    private PlaywrightManager() {
        playwright = Playwright.create();
    }

    public static synchronized PlaywrightManager getInstance() {
        if (instance == null) {
            instance = new PlaywrightManager();
        }
        return instance;
    }

    public void launchBrowser(boolean headless) {
        browser = playwright.chromium().launch(new BrowserType.LaunchOptions()
                .setHeadless(headless)
                .setSlowMo(50));
    }

    public void createContext() {
        context = browser.newContext(new Browser.NewContextOptions()
                .setRecordVideoDir(Paths.get("target/videos/")));
    }

    public void createPage() {
        page = context.newPage();
    }

    public Page getPage() {
        return page;
    }

    public BrowserContext getContext() {
        return context;
    }

    public Browser getBrowser() {
        return browser;
    }

    public void closePage() {
        if (page != null) {
            page.close();
        }
    }

    public void closeContext() {
        if (context != null) {
            context.close();
        }
    }

    public void closeBrowser() {
        if (browser != null) {
            browser.close();
        }
        if (playwright != null) {
            playwright.close();
        }
        instance = null;
    }
}
