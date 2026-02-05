package com.automation.cbaps.models;

public class RequisitionData {
    private String title;
    private String description;
    private String fundType;
    private String priority;
    
    public RequisitionData() {}
    
    public RequisitionData(String title, String fundType) {
        this.title = title;
        this.fundType = fundType;
    }
    
    public RequisitionData(String title, String description, String fundType, String priority) {
        this.title = title;
        this.description = description;
        this.fundType = fundType;
        this.priority = priority;
    }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getFundType() { return fundType; }
    public void setFundType(String fundType) { this.fundType = fundType; }
    public String getPriority() { return priority; }
    public void setPriority(String priority) { this.priority = priority; }
    
    @Override
    public String toString() {
        return "RequisitionData{title='" + title + "', fundType='" + fundType + "', priority='" + priority + "'}";
    }
}
