package com.automation.cbaps.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import com.automation.cbaps.library.GlobalSelenium;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class StatusTrackerPage {
    private static final Logger log = LogManager.getLogger(StatusTrackerPage.class);
    
    private WebDriver driver;
    private GlobalSelenium gs;
    
    private By statusBadge = By.id("reqStatus");
    private By requisitionIdLabel = By.id("requisitionId");
    
    public StatusTrackerPage(WebDriver driver, GlobalSelenium gs) {
        this.driver = driver;
        this.gs = gs;
        gs.waitForElementVisibility(statusBadge);
        log.info("✅ StatusTrackerPage initialized");
    }
    
    public String getStatus() {
        String status = gs.getText(statusBadge);
        log.info("📊 Final status: " + status);
        return status;
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
}
