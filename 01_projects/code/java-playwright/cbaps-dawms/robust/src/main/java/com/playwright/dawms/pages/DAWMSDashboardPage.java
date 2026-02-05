package com.playwright.dawms.pages;
import com.microsoft.playwright.*;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import org.slf4j.*;

public class DAWMSDashboardPage {
    private static final Logger log = LoggerFactory.getLogger(DAWMSDashboardPage.class);
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator submissionIntakeBtn;
    
    public DAWMSDashboardPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page; this.pwm = pwm;
        this.submissionIntakeBtn = page.locator("button:has-text('Submission Intake')");
        pwm.waitUntilElementVisible("button:has-text('Submission Intake')");
    }
    
    public SubmissionIntakePage goToSubmissionIntake() {
        pwm.clickElement(submissionIntakeBtn);
        return new SubmissionIntakePage(page, pwm);
    }
}
