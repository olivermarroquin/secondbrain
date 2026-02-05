package com.playwright.dawms.pages;
import com.microsoft.playwright.*;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;

public class SignatureRoutingPage {
    private Page page;
    private EnhancedPlaywrightManager pwm;
    private Locator signerDropdown, submitButton;
    
    public SignatureRoutingPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page; this.pwm = pwm;
        this.signerDropdown = page.locator("#signer");
        this.submitButton = page.locator("button:has-text('Submit for Signature')");
        pwm.waitUntilElementVisible("#signer");
    }
    
    public MilestoneStatusPage submitForSignature(String signer) {
        pwm.selectDropdown(signerDropdown, signer);
        pwm.clickElement(submitButton);
        return new MilestoneStatusPage(page, pwm);
    }
}
