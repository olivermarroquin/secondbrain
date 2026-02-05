package com.playwright.dawms.pages;
import com.microsoft.playwright.*;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import com.playwright.dawms.models.SubmissionData;
import org.slf4j.*;

public class SubmissionIntakePage {
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator submissionTypeDropdown, applicationNumberInput, createSubmissionButton;
    
    public SubmissionIntakePage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page; this.pwm = pwm;
        this.submissionTypeDropdown = page.locator("#submissionType");
        this.applicationNumberInput = page.locator("#applicationNumber");
        this.createSubmissionButton = page.locator("button:has-text('Create Submission')");
        pwm.waitUntilElementVisible("#submissionType");
    }
    
    public ReviewerAssignmentPage createSubmission(SubmissionData data) {
        pwm.selectDropdown(submissionTypeDropdown, data.getSubmissionType());
        pwm.enterText(applicationNumberInput, data.getApplicationNumber());
        pwm.clickElement(createSubmissionButton);
        return new ReviewerAssignmentPage(page, pwm);
    }
}
