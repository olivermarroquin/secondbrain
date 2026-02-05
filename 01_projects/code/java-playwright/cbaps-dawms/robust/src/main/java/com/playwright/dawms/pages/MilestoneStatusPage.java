package com.playwright.dawms.pages;
import com.microsoft.playwright.*;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;

public class MilestoneStatusPage {
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator milestoneLabel, statusLabel;
    
    public MilestoneStatusPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page; this.pwm = pwm;
        this.milestoneLabel = page.locator("#milestone");
        this.statusLabel = page.locator("#status");
        pwm.waitUntilElementVisible("#status");
    }
    
    public String getMilestone() { return pwm.getText(milestoneLabel); }
    public String getStatus() { return pwm.getText(statusLabel); }
    public boolean validateStatus(String expected) { return getStatus().equals(expected); }
    public boolean validateMilestone(String expected) { return getMilestone().equals(expected); }
}
