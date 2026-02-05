package com.playwright.cbaps.pages;
import com.microsoft.playwright.*;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import org.slf4j.*;

public class CBAPSDashboardPage {
    private static final Logger log = LoggerFactory.getLogger(CBAPSDashboardPage.class);
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator createRequisitionBtn;
    
    public CBAPSDashboardPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page; this.pwm = pwm;
        this.createRequisitionBtn = page.locator("button:has-text('Create Requisition')");
        pwm.waitUntilElementVisible("button:has-text('Create Requisition')");
    }
    
    public RequisitionPage goToCreateRequisition() {
        pwm.clickElement(createRequisitionBtn);
        return new RequisitionPage(page, pwm);
    }
}
