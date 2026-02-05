package com.playwright.cbaps.models;

public class RequisitionData {
    private String title, description, fundType, priority;
    
    public RequisitionData(String title, String fundType) {
        this.title = title; this.fundType = fundType;
    }
    
    public RequisitionData(String title, String desc, String fund, String priority) {
        this.title = title; this.description = desc; this.fundType = fund; this.priority = priority;
    }
    
    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public String getFundType() { return fundType; }
    public String getPriority() { return priority; }
}
