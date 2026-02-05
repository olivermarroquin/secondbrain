package com.playwright.cbaps.pages;
import com.microsoft.playwright.*;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import org.slf4j.*;

public class PortalHomePage {
    private static final Logger log = LoggerFactory.getLogger(PortalHomePage.class);
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator cbapsLink, dawmsLink;
    
    public PortalHomePage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page; this.pwm = pwm;
        this.cbapsLink = page.locator("a:has-text('CBAPS')");
        this.dawmsLink = page.locator("a:has-text('DAWMS')");
    }
    
    public CBAPSDashboardPage openCBAPS() {
        pwm.clickElement(cbapsLink);
        return new CBAPSDashboardPage(page, pwm);
    }
    
    public com.playwright.dawms.pages.DAWMSDashboardPage openDAWMS() {
        pwm.clickElement(dawmsLink);
        return new com.playwright.dawms.pages.DAWMSDashboardPage(page, pwm);
    }
}
