package com.playwright.week3;

import java.util.List;

import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.BrowserType.LaunchOptions;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;

public class WebsiteLinksTest extends OldBase {

	@Test(enabled = false)
	public void findAllLinks() throws Exception {
	
		page.navigate("https://www.amazon.com/");
		// Java hard coded delay for 5 seconds
		// Thread.sleep(5 * 1000);
		
		List<Locator> allLinkElements = page.locator("a").all();
		int totalLinks = allLinkElements.size();
		System.out.println("total links: " + totalLinks);
		
		int counter = 1;
		
		for(Locator link : allLinkElements) {
			String linkText = link.textContent();
			System.out.println(counter + ">>> link text [ " + linkText + "]");
			counter ++;
		}		
		
		// Q1: Display/print total number of links that contains text
		// Q2: Display/print total number of links that do Not have any text
		
		
	}	

	@Test
	public void findAllLinks_HomeDepot() throws Exception {
	
		page.navigate("https://www.homedepot.com/");
		// Java hard coded delay for 5 seconds
		// Thread.sleep(5 * 1000);
		
		List<Locator> allLinkElements = page.locator("a").all();
		int totalLinks = allLinkElements.size();
		System.out.println("total links: " + totalLinks);
		
		int counter = 1;
		
		for(Locator link : allLinkElements) {
			String linkText = link.textContent();
			System.out.println(counter + ">>> link text [ " + linkText + "]");
			counter ++;
		}	
		
	}	

}

























