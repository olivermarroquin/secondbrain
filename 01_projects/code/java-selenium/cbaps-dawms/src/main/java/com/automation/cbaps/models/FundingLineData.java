package com.automation.cbaps.models;
public class FundingLineData {
    private String amount;
    private String fiscalYear;
    private String category;
    private String description;
    
    public FundingLineData(String amount, String fiscalYear) {
        this.amount = amount;
        this.fiscalYear = fiscalYear;
    }
    
    public String getAmount() { return amount; }
    public void setAmount(String amount) { this.amount = amount; }
    public String getFiscalYear() { return fiscalYear; }
    public void setFiscalYear(String fiscalYear) { this.fiscalYear = fiscalYear; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
