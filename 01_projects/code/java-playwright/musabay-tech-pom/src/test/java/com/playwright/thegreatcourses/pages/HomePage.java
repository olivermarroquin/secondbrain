package com.playwright.thegreatcourses.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.AriaRole;
import com.playwright.week5.library.Base;
import com.playwright.week5.library.PlaywrightManager;

public class HomePage {
	private static final Logger log = LoggerFactory.getLogger(HomePage.class);

	private PlaywrightManager myPlaywright;
	private Page page;

	public HomePage(Page _page, PlaywrightManager _myPlaywright) {
		this.myPlaywright = _myPlaywright;
		this.page = _page;
	}

	public HomePage navigateToHomePage() {
		String theGreatCourses = "https://www.thegreatcourses.com/";
		page.navigate(theGreatCourses);
		myPlaywright.waitUntilElementVisible("#search-field");
				
		//page.waitForLoadState(); // Ensure page is fully loaded
		return this;
	}

	public String getTitle() {
		return page.title();
	}

	public SearchCourseResultPage searchACourse(String courseName) {
		myPlaywright.enterText(page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions()
				.setName("Search for Courses")), courseName);
				
		myPlaywright.pressEnterKey(page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions()
				.setName("Search for Courses")));	
		
		SearchCourseResultPage scrPage = new SearchCourseResultPage(page, myPlaywright);		
		return scrPage;
	}
}














