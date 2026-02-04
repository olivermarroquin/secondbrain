package com.playwright.week5.library;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import com.aventstack.extentreports.reporter.configuration.Theme;
import com.aventstack.extentreports.reporter.configuration.ViewName;
import java.text.SimpleDateFormat;
import java.util.Date;

// this is Singleton class
public class ExtentReportManager {
		
	private static ExtentReports extent;
	
	public static ExtentReports getInstance() {
		
		if (extent == null) {
			String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
			String reportPath = "target/report/extent-report-" + timeStamp + ".html";
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
			sparkReporter.config().setReportName("BOA Automation Test Results");
			sparkReporter.config().setDocumentTitle("Test Report");
			
			extent = new ExtentReports();
			extent.attachReporter(sparkReporter);
			extent.setSystemInfo("Automation Developer", "Frank Musabay");
			extent.setSystemInfo("Environment", "QA/Test");
		}		
		return extent;
	}
		
	
	
}






