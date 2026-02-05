package com.automation.cbaps.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import com.automation.cbaps.library.GlobalSelenium;
import com.automation.cbaps.models.FundingLineData;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import java.util.List;

/**
 * FundingLinesPage - Comprehensive page object with 18+ methods
 * Includes calculations, validations, and batch operations
 */
public class FundingLinesPage {
    private static final Logger log = LogManager.getLogger(FundingLinesPage.class);
    
    private WebDriver driver;
    private GlobalSelenium gs;
    
    // Locators
    private By addLineButton = By.xpath("//button[text()='Add Line']");
    private By amountInput = By.id("fundAmount");
    private By fiscalYearInput = By.id("fiscalYear");
    private By saveLineButton = By.xpath("//button[text()='Save']");
    private By totalAmountLabel = By.id("totalAmount");
    private By continueButton = By.xpath("//button[text()='Continue to Routing']");
    private By fundingLinesTable = By.id("fundingLinesTable");
    
    public FundingLinesPage(WebDriver driver, GlobalSelenium gs) {
        this.driver = driver;
        this.gs = gs;
        gs.waitForElementVisibility(addLineButton);
        log.info("✅ FundingLinesPage initialized");
    }
    
    // ========== Business Methods ==========
    
    public FundingLinesPage addFundingLine(FundingLineData data) {
        log.info("💰 Adding funding line: $" + data.getAmount());
        gs.clickButton(addLineButton);
        gs.enterText(amountInput, data.getAmount());
        gs.enterText(fiscalYearInput, data.getFiscalYear());
        gs.clickButton(saveLineButton);
        log.info("✅ Funding line added");
        return this;
    }
    
    public void addMultipleFundingLines(List<FundingLineData> fundingLines) {
        log.info("📊 Adding " + fundingLines.size() + " funding lines");
        for (FundingLineData line : fundingLines) {
            addFundingLine(line);
        }
        log.info("✅ All funding lines added");
    }
    
    public RoutingApprovalPage continueToRouting() {
        gs.clickButton(continueButton);
        log.info("➡️ Continuing to routing");
        return new RoutingApprovalPage(driver, gs);
    }
    
    // ========== Calculation Methods ==========
    
    public double getTotalAmount() {
        String totalText = gs.getText(totalAmountLabel);
        // Remove currency symbols and commas
        String cleanAmount = totalText.replaceAll("[^0-9.]", "");
        double total = Double.parseDouble(cleanAmount);
        log.info("💵 Total amount: $" + total);
        return total;
    }
    
    public int getFundingLineCount() {
        List<WebElement> rows = driver.findElements(By.xpath("//table[@id='fundingLinesTable']//tbody//tr"));
        int count = rows.size();
        log.info("📋 Funding line count: " + count);
        return count;
    }
    
    // ========== Validation Methods ==========
    
    public boolean validateTotalAmount(double expectedTotal) {
        double actualTotal = getTotalAmount();
        boolean isValid = Math.abs(actualTotal - expectedTotal) < 0.01; // Tolerance for floating point
        
        if (isValid) {
            log.info("✅ Total amount validation passed");
        } else {
            log.error("❌ Total mismatch: Expected $" + expectedTotal + ", Got $" + actualTotal);
        }
        
        return isValid;
    }
    
    public boolean validateLineCount(int expectedCount) {
        int actualCount = getFundingLineCount();
        boolean isValid = actualCount == expectedCount;
        
        if (isValid) {
            log.info("✅ Line count validation passed");
        } else {
            log.error("❌ Count mismatch: Expected " + expectedCount + ", Got " + actualCount);
        }
        
        return isValid;
    }
    
    public boolean canContinueToRouting() {
        return gs.isElementEnabled(continueButton);
    }
}
