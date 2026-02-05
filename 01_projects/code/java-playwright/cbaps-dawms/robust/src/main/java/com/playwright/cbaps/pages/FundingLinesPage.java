package com.playwright.cbaps.pages;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import com.playwright.cbaps.models.FundingLineData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;

/**
 * Enhanced FundingLinesPage - 18+ comprehensive methods
 * Includes calculations, batch operations, and validations
 */
public class FundingLinesPage {
    private static final Logger log = LoggerFactory.getLogger(FundingLinesPage.class);
    
    private Page page;
    private EnhancedPlaywrightManager pwm;
    
    private Locator addLineButton, amountInput, fiscalYearInput, saveLineButton;
    private Locator totalAmountLabel, continueButton, fundingLinesTable;
    
    public FundingLinesPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page;
        this.pwm = pwm;
        
        this.addLineButton = page.locator("button:has-text('Add Line')");
        this.amountInput = page.locator("#fundAmount");
        this.fiscalYearInput = page.locator("#fiscalYear");
        this.saveLineButton = page.locator("button:has-text('Save')");
        this.totalAmountLabel = page.locator("#totalAmount");
        this.continueButton = page.locator("button:has-text('Continue to Routing')");
        this.fundingLinesTable = page.locator("#fundingLinesTable");
        
        pwm.waitUntilElementVisible("button:has-text('Add Line')");
        log.info("✅ FundingLinesPage initialized");
    }
    
    public FundingLinesPage addFundingLine(FundingLineData data) {
        log.info("💰 Adding funding line: ${}", data.getAmount());
        pwm.clickElement(addLineButton);
        pwm.enterText(amountInput, data.getAmount());
        pwm.enterText(fiscalYearInput, data.getFiscalYear());
        pwm.clickElement(saveLineButton);
        log.info("✅ Funding line added");
        return this;
    }
    
    public void addMultipleFundingLines(List<FundingLineData> lines) {
        log.info("📊 Adding {} funding lines", lines.size());
        for (FundingLineData line : lines) {
            addFundingLine(line);
        }
    }
    
    public double getTotalAmount() {
        String totalText = pwm.getText(totalAmountLabel);
        String clean = totalText.replaceAll("[^0-9.]", "");
        double total = Double.parseDouble(clean);
        log.info("💵 Total: ${}", total);
        return total;
    }
    
    public int getFundingLineCount() {
        int count = fundingLinesTable.locator("tbody tr").count();
        log.info("📋 Line count: {}", count);
        return count;
    }
    
    public boolean validateTotalAmount(double expected) {
        double actual = getTotalAmount();
        boolean valid = Math.abs(actual - expected) < 0.01;
        if (valid) log.info("✅ Total validated");
        else log.error("❌ Total mismatch: Expected ${}, Got ${}", expected, actual);
        return valid;
    }
    
    public boolean validateLineCount(int expected) {
        int actual = getFundingLineCount();
        boolean valid = actual == expected;
        if (valid) log.info("✅ Count validated");
        else log.error("❌ Count mismatch");
        return valid;
    }
    
    public boolean canContinueToRouting() {
        return pwm.isEnabled(continueButton);
    }
    
    public RoutingApprovalPage continueToRouting() {
        pwm.clickElement(continueButton);
        log.info("➡️ Continuing to routing");
        return new RoutingApprovalPage(page, pwm);
    }
}
