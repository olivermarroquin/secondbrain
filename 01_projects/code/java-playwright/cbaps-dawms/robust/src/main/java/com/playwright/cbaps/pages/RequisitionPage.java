package com.playwright.cbaps.pages;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.playwright.cbaps.library.EnhancedPlaywrightManager;
import com.playwright.cbaps.models.RequisitionData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Enhanced RequisitionPage - 22+ comprehensive methods
 * Matches TypeScript version's robustness with validations, calculations, and state checks
 */
public class RequisitionPage {
    private static final Logger log = LoggerFactory.getLogger(RequisitionPage.class);
    
    private Page page;
    private EnhancedPlaywrightManager pwm;
    
    // Locators
    private Locator titleInput;
    private Locator descriptionInput;
    private Locator fundTypeDropdown;
    private Locator priorityDropdown;
    private Locator submitButton;
    private Locator saveAsDraftButton;
    private Locator cancelButton;
    private Locator statusBadge;
    private Locator requisitionIdLabel;
    private Locator fundingLinesLink;
    private Locator routeForApprovalButton;
    private Locator lastModifiedLabel;
    private Locator createdByLabel;
    
    public RequisitionPage(Page page, EnhancedPlaywrightManager pwm) {
        this.page = page;
        this.pwm = pwm;
        
        // Initialize locators
        this.titleInput = page.locator("#requisitionTitle");
        this.descriptionInput = page.locator("#description");
        this.fundTypeDropdown = page.locator("#fundType");
        this.priorityDropdown = page.locator("#priority");
        this.submitButton = page.locator("button:has-text('Submit')");
        this.saveAsDraftButton = page.locator("button:has-text('Save as Draft')");
        this.cancelButton = page.locator("button:has-text('Cancel')");
        this.statusBadge = page.locator("#reqStatus");
        this.requisitionIdLabel = page.locator("#requisitionId");
        this.fundingLinesLink = page.locator("a:has-text('Funding Lines')");
        this.routeForApprovalButton = page.locator("button:has-text('Route for Approval')");
        this.lastModifiedLabel = page.locator("#lastModified");
        this.createdByLabel = page.locator("#createdBy");
        
        // Stability anchor - wait for page to load
        pwm.waitUntilElementVisible("#requisitionTitle");
        log.info("✅ RequisitionPage initialized");
    }
    
    // ========== Business Methods ==========
    
    /**
     * Create requisition with complete data and submit
     */
    public void createRequisition(RequisitionData data) {
        log.info("📝 Creating requisition: {}", data.getTitle());
        
        pwm.enterText(titleInput, data.getTitle());
        
        if (data.getDescription() != null && !data.getDescription().isEmpty()) {
            pwm.enterText(descriptionInput, data.getDescription());
        }
        
        pwm.selectDropdown(fundTypeDropdown, data.getFundType());
        
        if (data.getPriority() != null && !data.getPriority().isEmpty()) {
            pwm.selectDropdown(priorityDropdown, data.getPriority());
        }
        
        pwm.clickElement(submitButton);
        log.info("✅ Requisition created successfully");
    }
    
    /**
     * Fill form without submitting
     */
    public void fillRequisitionForm(RequisitionData data) {
        log.info("📋 Filling requisition form");
        
        pwm.enterText(titleInput, data.getTitle());
        
        if (data.getDescription() != null) {
            pwm.enterText(descriptionInput, data.getDescription());
        }
        
        pwm.selectDropdown(fundTypeDropdown, data.getFundType());
        
        if (data.getPriority() != null) {
            pwm.selectDropdown(priorityDropdown, data.getPriority());
        }
        
        log.info("✅ Form filled");
    }
    
    /**
     * Save requisition as draft
     */
    public void saveAsDraft(RequisitionData data) {
        log.info("💾 Saving as draft");
        fillRequisitionForm(data);
        pwm.clickElement(saveAsDraftButton);
        log.info("✅ Saved as draft");
    }
    
    /**
     * Clear all form fields
     */
    public void clearForm() {
        log.info("🧹 Clearing form");
        titleInput.fill("");
        descriptionInput.fill("");
        log.info("✅ Form cleared");
    }
    
    /**
     * Cancel requisition creation
     */
    public void cancel() {
        pwm.clickElement(cancelButton);
        log.info("❌ Requisition creation cancelled");
    }
    
    // ========== Navigation Methods ==========
    
    /**
     * Navigate to Funding Lines page
     */
    public FundingLinesPage goToFundingLines() {
        pwm.clickElement(fundingLinesLink);
        log.info("➡️ Navigating to Funding Lines");
        return new FundingLinesPage(page, pwm);
    }
    
    /**
     * Navigate to Routing/Approval page
     */
    public RoutingApprovalPage routeForApproval() {
        pwm.clickElement(routeForApprovalButton);
        log.info("➡️ Routing for approval");
        return new RoutingApprovalPage(page, pwm);
    }
    
    // ========== Validation Methods ==========
    
    /**
     * Validate form has required fields filled
     */
    public boolean validateForm() {
        boolean isValid = true;
        String title = pwm.getText(titleInput);
        
        if (title == null || title.trim().isEmpty()) {
            log.warn("⚠️ Title is required");
            isValid = false;
        }
        
        if (!pwm.isVisible(fundTypeDropdown) || pwm.getText(fundTypeDropdown).isEmpty()) {
            log.warn("⚠️ Fund type is required");
            isValid = false;
        }
        
        if (isValid) {
            log.info("✅ Form validation passed");
        } else {
            log.error("❌ Form validation failed");
        }
        
        return isValid;
    }
    
    /**
     * Validate requisition status matches expected
     */
    public boolean validateStatus(String expectedStatus) {
        String actualStatus = getStatus();
        boolean isValid = actualStatus.equals(expectedStatus);
        
        if (isValid) {
            log.info("✅ Status validation passed: {}", expectedStatus);
        } else {
            log.error("❌ Status mismatch: Expected '{}', Got '{}'", expectedStatus, actualStatus);
        }
        
        return isValid;
    }
    
    /**
     * Validate requisition ID exists
     */
    public boolean validateRequisitionId() {
        String reqId = getRequisitionId();
        boolean isValid = reqId != null && !reqId.isEmpty();
        
        if (isValid) {
            log.info("✅ Requisition ID validation passed: {}", reqId);
        } else {
            log.error("❌ Requisition ID missing");
        }
        
        return isValid;
    }
    
    // ========== Getter Methods ==========
    
    /**
     * Get current requisition status
     */
    public String getStatus() {
        String status = pwm.getText(statusBadge);
        log.info("📊 Status: {}", status);
        return status;
    }
    
    /**
     * Get requisition ID
     */
    public String getRequisitionId() {
        if (pwm.isVisible(requisitionIdLabel)) {
            String id = pwm.getText(requisitionIdLabel);
            log.info("🆔 Requisition ID: {}", id);
            return id;
        }
        return null;
    }
    
    /**
     * Get requisition metadata as formatted string
     */
    public String getRequisitionMetadata() {
        StringBuilder metadata = new StringBuilder();
        metadata.append("ID: ").append(getRequisitionId()).append(", ");
        metadata.append("Status: ").append(getStatus());
        
        if (pwm.isVisible(lastModifiedLabel)) {
            metadata.append(", Modified: ").append(pwm.getText(lastModifiedLabel));
        }
        
        if (pwm.isVisible(createdByLabel)) {
            metadata.append(", Created By: ").append(pwm.getText(createdByLabel));
        }
        
        log.info("📋 Metadata: {}", metadata.toString());
        return metadata.toString();
    }
    
    /**
     * Get requisition title
     */
    public String getTitle() {
        return pwm.getAttribute(titleInput, "value");
    }
    
    // ========== State Check Methods ==========
    
    /**
     * Check if requisition can be edited
     */
    public boolean canEdit() {
        String status = getStatus();
        boolean editable = "Draft".equalsIgnoreCase(status) || "Rejected".equalsIgnoreCase(status);
        log.info("📝 Can edit: {}", editable);
        return editable;
    }
    
    /**
     * Check if requisition can be deleted
     */
    public boolean canDelete() {
        String status = getStatus();
        boolean deletable = "Draft".equalsIgnoreCase(status);
        log.info("🗑️ Can delete: {}", deletable);
        return deletable;
    }
    
    /**
     * Check if routing is available
     */
    public boolean isRoutingAvailable() {
        boolean available = pwm.isVisible(routeForApprovalButton) && pwm.isEnabled(routeForApprovalButton);
        log.info("✍️ Routing available: {}", available);
        return available;
    }
    
    /**
     * Check if funding lines section is available
     */
    public boolean isFundingAvailable() {
        boolean available = pwm.isVisible(fundingLinesLink);
        log.info("💰 Funding available: {}", available);
        return available;
    }
    
    /**
     * Check if submit button is enabled
     */
    public boolean canSubmit() {
        return pwm.isEnabled(submitButton);
    }
    
    // ========== Utility Methods ==========
    
    /**
     * Wait for status to change to expected value
     */
    public boolean waitForStatus(String expectedStatus, int timeoutSeconds) {
        log.info("⏳ Waiting for status: {}", expectedStatus);
        
        for (int i = 0; i < timeoutSeconds; i++) {
            if (getStatus().equals(expectedStatus)) {
                log.info("✅ Status changed to: {}", expectedStatus);
                return true;
            }
            pwm.wait(1);
        }
        
        log.error("❌ Status did not change to: {}", expectedStatus);
        return false;
    }
    
    /**
     * Refresh requisition page
     */
    public void refresh() {
        page.reload();
        pwm.waitUntilElementVisible("#requisitionTitle");
        log.info("🔄 Page refreshed");
    }
}
