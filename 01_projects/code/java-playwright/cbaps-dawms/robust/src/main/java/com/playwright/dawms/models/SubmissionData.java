package com.playwright.dawms.models;
public class SubmissionData {
    private String submissionType, applicationNumber, sponsorName, drugName;
    public SubmissionData(String type, String appNum) { this.submissionType = type; this.applicationNumber = appNum; }
    public SubmissionData(String type, String appNum, String sponsor, String drug) {
        this(type, appNum); this.sponsorName = sponsor; this.drugName = drug;
    }
    public String getSubmissionType() { return submissionType; }
    public String getApplicationNumber() { return applicationNumber; }
    public String getSponsorName() { return sponsorName; }
    public String getDrugName() { return drugName; }
}
