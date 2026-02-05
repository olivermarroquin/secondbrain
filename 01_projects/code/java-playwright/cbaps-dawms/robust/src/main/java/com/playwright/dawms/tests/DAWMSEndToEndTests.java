package com.playwright.dawms.tests;
import org.testng.Assert;
import org.testng.annotations.Test;
import com.playwright.cbaps.library.Base;
import com.playwright.dawms.models.*;
import com.playwright.dawms.pages.*;
import com.playwright.cbaps.pages.PortalHomePage;
import java.util.Arrays;

public class DAWMSEndToEndTests extends Base {
    private static final String PORTAL_URL = "https://dawms-portal.example.com";
    
    @Test
    public void completeSubmissionWorkflowTest() {
        pwm.navigateTo(PORTAL_URL);
        PortalHomePage portal = new PortalHomePage(page, pwm);
        DAWMSDashboardPage dashboard = portal.openDAWMS();
        
        SubmissionData subData = new SubmissionData("NDA", "APP-" + System.currentTimeMillis(), "PharmaCorp", "DrugX");
        SubmissionIntakePage intakePage = dashboard.goToSubmissionIntake();
        ReviewerAssignmentPage reviewerPage = intakePage.createSubmission(subData);
        
        reviewerPage.assignMultipleReviewers(Arrays.asList(
            new ReviewerData("Dr. Smith", "Clinical Reviewer"),
            new ReviewerData("Dr. Johnson", "Statistical Reviewer")
        ));
        
        SignatureRoutingPage signaturePage = reviewerPage.routeToSignatureStep();
        MilestoneStatusPage statusPage = signaturePage.submitForSignature("Division Director");
        
        Assert.assertTrue(statusPage.validateStatus("Pending Signature"));
    }
}
