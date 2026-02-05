package com.playwright.cbaps.pages;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class RoutingApprovalPage {
    private static final Logger log = LoggerFactory.getLogger(RoutingApprovalPage.class);
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator approverDropdown, submitButton;
    
    public RoutingApprovalPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page;
        this.pwm = pwm;
        this.approverDropdown = page.locator("#approver");
        this.submitButton = page.locator("button:has-text('Submit for Approval')");
        pwm.waitUntilElementVisible("#approver");
        log.info("✅ RoutingApprovalPage initialized");
    }
    
    public StatusTrackerPage submitForApproval(String approver) {
        log.info("✍️ Submitting for approval: {}", approver);
        pwm.selectDropdown(approverDropdown, approver);
        pwm.clickElement(submitButton);
        return new StatusTrackerPage(page, pwm);
    }
}
