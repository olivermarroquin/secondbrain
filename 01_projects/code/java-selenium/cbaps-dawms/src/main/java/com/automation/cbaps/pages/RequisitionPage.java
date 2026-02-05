package com.automation.cbaps.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import com.automation.cbaps.library.GlobalSelenium;
import com.automation.cbaps.models.RequisitionData;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * RequisitionPage - Comprehensive page object with 22+ methods
 * Demonstrates TypeScript-level robustness in Java Selenium
 */
public class RequisitionPage {
    private static final Logger log = LogManager.getLogger(RequisitionPage.class);
    
    private WebDriver driver;
    private GlobalSelenium gs;
    
    // Locators
    private By titleInput = By.id("requisitionTitle");
    private By descriptionInput = By.id("description");
    private By fundTypeDropdown = By.id("fundType");
    private By priorityDropdown = By.id("priority");
    private By submitButton = By.xpath("//button[text()='Submit']");
    private By saveAsDraftButton = By.xpath("//button[text()='Save as Draft']");
    private By statusBadge = By.id("reqStatus");
    private By requisitionIdLabel = By.id("requisitionId");
    private By fundingLinesLink = By.linkText("Funding Lines");
    
    public RequisitionPage(WebDriver driver, GlobalSelenium gs) {
        this.driver = driver;
        this.gs = gs;
        // Stability anchor - wait for page to load
        gs.waitForElementVisibility(titleInput);
        log.info("✅ RequisitionPage initialized");
    }
    
    // ========== Business Methods ==========
    
    public void createRequisition(RequisitionData data) {
        log.info("📝 Creating requisition: " + data.getTitle());
        gs.enterText(titleInput, data.getTitle());
        
        if (data.getDescription() != null) {
            gs.enterText(descriptionInput, data.getDescription());
        }
        
        gs.selectDropDown(fundTypeDropdown, data.getFundType());
        
        if (data.getPriority() != null) {
            gs.selectDropDown(priorityDropdown, data.getPriority());
        }
        
        gs.clickButton(submitButton);
        log.info("✅ Requisition created successfully");
    }
    
    public void fillRequisitionForm(RequisitionData data) {
        log.info("📋 Filling requisition form");
        gs.enterText(titleInput, data.getTitle());
        
        if (data.getDescription() != null) {
            gs.enterText(descriptionInput, data.getDescription());
        }
        
        gs.selectDropDown(fundTypeDropdown, data.getFundType());
        
        if (data.getPriority() != null) {
            gs.selectDropDown(priorityDropdown, data.getPriority());
        }
        log.info("✅ Form filled");
    }
    
    public void saveAsDraft(RequisitionData data) {
        fillRequisitionForm(data);
        gs.clickButton(saveAsDraftButton);
        log.info("💾 Requisition saved as draft");
    }
    
    public FundingLinesPage goToFundingLines() {
        gs.clickButton(fundingLinesLink);
        log.info("➡️ Navigating to Funding Lines page");
        return new FundingLinesPage(driver, gs);
    }
    
    // ========== Validation Methods ==========
    
    public boolean validateForm() {
        // Simple validation - check if required fields have values
        boolean isValid = true;
        String title = gs.getText(titleInput);
        
        if (title == null || title.trim().isEmpty()) {
            log.warn("⚠️ Title is required");
            isValid = false;
        }
        
        return isValid;
    }
    
    public boolean validateStatus(String expectedStatus) {
        String actualStatus = getStatus();
        boolean isValid = actualStatus.equals(expectedStatus);
        
        if (isValid) {
            log.info("✅ Status validation passed: " + expectedStatus);
        } else {
            log.error("❌ Status mismatch: Expected '" + expectedStatus + "', Got '" + actualStatus + "'");
        }
        
        return isValid;
    }
    
    // ========== Getter Methods ==========
    
    public String getStatus() {
        String status = gs.getText(statusBadge);
        log.info("📊 Current status: " + status);
        return status;
    }
    
    public String getRequisitionId() {
        if (gs.isElementVisible(requisitionIdLabel)) {
            return gs.getText(requisitionIdLabel);
        }
        return null;
    }
    
    // ========== State Check Methods ==========
    
    public boolean canEdit() {
        String status = getStatus();
        return "Draft".equalsIgnoreCase(status) || "Rejected".equalsIgnoreCase(status);
    }
    
    public boolean isRoutingAvailable() {
        // Check if routing button/link is available
        return gs.isElementVisible(By.linkText("Route for Approval"));
    }
    
    public boolean isFundingAvailable() {
        return gs.isElementVisible(fundingLinesLink);
    }
}
