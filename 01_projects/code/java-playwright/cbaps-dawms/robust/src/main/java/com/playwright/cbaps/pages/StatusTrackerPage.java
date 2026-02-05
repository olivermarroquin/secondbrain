package com.playwright.cbaps.pages;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StatusTrackerPage {
    private static final Logger log = LoggerFactory.getLogger(StatusTrackerPage.class);
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator statusBadge, requisitionIdLabel;
    
    public StatusTrackerPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page;
        this.pwm = pwm;
        this.statusBadge = page.locator("#reqStatus");
        this.requisitionIdLabel = page.locator("#requisitionId");
        pwm.waitUntilElementVisible("#reqStatus");
        log.info("✅ StatusTrackerPage initialized");
    }
    
    public String getStatus() {
        String status = pwm.getText(statusBadge);
        log.info("📊 Final status: {}", status);
        return status;
    }
    
    public boolean validateStatus(String expected) {
        String actual = getStatus();
        boolean valid = actual.equals(expected);
        if (valid) log.info("✅ Status validated: {}", expected);
        else log.error("❌ Status mismatch: Expected '{}', Got '{}'", expected, actual);
        return valid;
    }
}
