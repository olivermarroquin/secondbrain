package com.playwright.cbaps.models;

public class FundingLineData {
    private String amount, fiscalYear;
    
    public FundingLineData(String amount, String year) {
        this.amount = amount; this.fiscalYear = year;
    }
    
    public String getAmount() { return amount; }
    public String getFiscalYear() { return fiscalYear; }
}
