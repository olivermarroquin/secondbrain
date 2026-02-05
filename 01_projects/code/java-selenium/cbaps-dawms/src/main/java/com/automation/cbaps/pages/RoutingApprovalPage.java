package com.automation.cbaps.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import com.automation.cbaps.library.GlobalSelenium;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class RoutingApprovalPage {
    private static final Logger log = LogManager.getLogger(RoutingApprovalPage.class);
    
    private WebDriver driver;
    private GlobalSelenium gs;
    
    private By approverDropdown = By.id("approver");
    private By submitButton = By.xpath("//button[text()='Submit for Approval']");
    
    public RoutingApprovalPage(WebDriver driver, GlobalSelenium gs) {
        this.driver = driver;
        this.gs = gs;
        gs.waitForElementVisibility(approverDropdown);
        log.info("✅ RoutingApprovalPage initialized");
    }
    
    public StatusTrackerPage submitForApproval(String approver) {
        log.info("✍️ Submitting for approval to: " + approver);
        gs.selectDropDown(approverDropdown, approver);
        gs.clickButton(submitButton);
        log.info("✅ Submitted for approval");
        return new StatusTrackerPage(driver, gs);
    }
}
