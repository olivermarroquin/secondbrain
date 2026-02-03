package com.playwright.week5.tests;

import org.testng.annotations.Test;

import com.playwright.week5.library.Base;

public class CertificateErrorTests extends Base{

	public String webURL = "https://uitestingplayground.com/dynamictable/";
	
	@Test
	public void certificateErrorTest1() {
		System.out.println("Navigating to website: " + webURL);
		page.navigate(webURL);
		
		
		String pageTitle = page.title();
		System.out.println("Get page title: " + pageTitle);
		
	}
}










