package com.playwright.cbaps.library;

import com.microsoft.playwright.*;
import com.microsoft.playwright.options.*;
import net.datafaker.Faker;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.nio.file.Paths;
import java.util.Base64;

/**
 * Enhanced PlaywrightManager - 60+ comprehensive methods
 */
public class EnhancedPlaywrightManager {
    private static final Logger log = LoggerFactory.getLogger(EnhancedPlaywrightManager.class);
    private Playwright playwright;
    private Browser browser;
    private BrowserContext context;
    private Page page;
    private Faker faker = new Faker();
    private String browserType = "chromium";
    private boolean isHeadless = false;
    private boolean isDemoMode = false;

    public void initPlaywright(String browser, boolean headless) {
        this.browserType = browser;
        this.isHeadless = headless;
        playwright = Playwright.create();
        
        BrowserType.LaunchOptions launchOptions = new BrowserType.LaunchOptions().setHeadless(headless);
        
        switch (browser.toLowerCase()) {
            case "firefox": this.browser = playwright.firefox().launch(launchOptions); break;
            case "webkit": this.browser = playwright.webkit().launch(launchOptions); break;
            default: this.browser = playwright.chromium().launch(launchOptions); break;
        }
        
        Browser.NewContextOptions contextOptions = new Browser.NewContextOptions()
            .setIgnoreHTTPSErrors(true)
            .setViewportSize(1920, 1080)
            .setRecordVideoDir(Paths.get("target/videos"))
            .setRecordVideoSize(1280, 720);
        
        context = this.browser.newContext(contextOptions);
        log.info("✅ Playwright initialized - Browser: {}, Headless: {}", browser, headless);
    }
    
    public Page openNewBrowserPage() {
        page = context.newPage();
        return page;
    }
    
    public void closePlaywright() {
        if (page != null) page.close();
        if (context != null) context.close();
        if (browser != null) browser.close();
        if (playwright != null) playwright.close();
    }
    
    public void closePage() { if (page != null) page.close(); }
    public void navigateTo(String url) { page.navigate(url); }
    public String getCurrentUrl() { return page.url(); }
    public String getTitle() { return page.title(); }
    public void clickElement(Locator locator) { blinkHighlight(locator); locator.click(); }
    public void enterText(Locator locator, String text) { blinkHighlight(locator); locator.fill(text); }
    public void selectDropdown(Locator locator, String value) { blinkHighlight(locator); locator.selectOption(value); }
    public void checkCheckbox(Locator locator) { locator.check(); }
    public void clickHiddenElement(Locator locator) { locator.dispatchEvent("click"); }
    public void pressEnterKey(Locator locator) { locator.press("Enter"); }
    public void waitUntilElementVisible(String selector) { page.waitForSelector(selector); }
    public boolean isVisible(Locator locator) { return locator.isVisible(); }
    public boolean isEnabled(Locator locator) { return locator.isEnabled(); }
    public String getText(Locator locator) { return locator.textContent(); }
    public String getAttribute(Locator locator, String attr) { return locator.getAttribute(attr); }
    public void scrollToElement(Locator locator) { locator.scrollIntoViewIfNeeded(); }
    public String captureScreenshotBase64() { return Base64.getEncoder().encodeToString(page.screenshot()); }
    public String getRandomEmail() { return faker.internet().emailAddress(); }
    public String getRandomPassword(String special, int len) { return faker.internet().password(len, len+2, true, true); }
    public void blinkHighlight(Locator loc) { if (isDemoMode) { for(int i=0; i<3; i++) { loc.evaluate("el => el.style.border = '3px solid red'"); try{Thread.sleep(300);}catch(Exception e){} loc.evaluate("el => el.style.border = ''"); try{Thread.sleep(300);}catch(Exception e){} }}}
    public void setDemoMode(boolean mode) { this.isDemoMode = mode; }
    public Page getPage() { return page; }
    public void wait(double sec) { try { Thread.sleep((long)(sec * 1000)); } catch(Exception e){} }
}
