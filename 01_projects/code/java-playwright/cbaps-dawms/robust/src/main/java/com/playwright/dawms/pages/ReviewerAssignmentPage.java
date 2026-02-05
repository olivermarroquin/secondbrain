package com.playwright.dawms.pages;
import com.microsoft.playwright.*;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import com.playwright.dawms.models.ReviewerData;
import org.slf4j.*;
import java.util.List;

public class ReviewerAssignmentPage {
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator reviewerRoleDropdown, reviewerNameInput, assignReviewerButton, continueButton;
    
    public ReviewerAssignmentPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page; this.pwm = pwm;
        this.reviewerRoleDropdown = page.locator("#reviewerRole");
        this.reviewerNameInput = page.locator("#reviewerName");
        this.assignReviewerButton = page.locator("button:has-text('Assign')");
        this.continueButton = page.locator("button:has-text('Route to Signature')");
        pwm.waitUntilElementVisible("#reviewerRole");
    }
    
    public ReviewerAssignmentPage assignReviewer(ReviewerData data) {
        pwm.selectDropdown(reviewerRoleDropdown, data.getRole());
        pwm.enterText(reviewerNameInput, data.getName());
        pwm.clickElement(assignReviewerButton);
        return this;
    }
    
    public void assignMultipleReviewers(List<ReviewerData> reviewers) {
        for (ReviewerData r : reviewers) assignReviewer(r);
    }
    
    public SignatureRoutingPage routeToSignatureStep() {
        pwm.clickElement(continueButton);
        return new SignatureRoutingPage(page, pwm);
    }
}
