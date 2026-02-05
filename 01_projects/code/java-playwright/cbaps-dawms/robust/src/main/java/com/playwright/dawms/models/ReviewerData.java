package com.playwright.dawms.models;
public class ReviewerData {
    private String name, role, specialty;
    public ReviewerData(String name, String role) { this.name = name; this.role = role; }
    public ReviewerData(String name, String role, String specialty) { this(name, role); this.specialty = specialty; }
    public String getName() { return name; }
    public String getRole() { return role; }
    public String getSpecialty() { return specialty; }
}
