package com.cbaps.library;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import com.aventstack.extentreports.reporter.configuration.Theme;
import com.aventstack.extentreports.reporter.configuration.ViewName;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * ExtentReportManager: Singleton class for managing ExtentReports
 * Generates HTML reports for CBAPS automation tests
 */
public class ExtentReportManager {
		
	private static ExtentReports extent;
	
	public static ExtentReports getInstance() {
		
		if (extent == null) {
			String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
			String reportPath = "target/report/cbaps-extent-report-" + timeStamp + ".html";
			ExtentSparkReporter sparkReporter = new ExtentSparkReporter(reportPath)
					.viewConfigurer()
					.viewOrder()
					.as(new ViewName[] {
							ViewName.TEST,
							ViewName.DASHBOARD,							
							ViewName.AUTHOR,
							ViewName.DEVICE,
							ViewName.EXCEPTION,
							ViewName.LOG,
							ViewName.CATEGORY
							
					}).apply();
			
			sparkReporter.config().setTheme(Theme.DARK);
			sparkReporter.config().setReportName("CBAPS Automation Test Results");
			sparkReporter.config().setDocumentTitle("CBAPS Test Report");
			
			extent = new ExtentReports();
			extent.attachReporter(sparkReporter);
			extent.setSystemInfo("Automation Developer", "QA Team");
			extent.setSystemInfo("Environment", "QA/Test");
			extent.setSystemInfo("Application", "CBAPS");
		}		
		return extent;
	}
}
