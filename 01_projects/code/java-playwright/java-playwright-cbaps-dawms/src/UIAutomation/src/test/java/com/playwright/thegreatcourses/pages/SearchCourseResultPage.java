package com.playwright.thegreatcourses.pages;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Page;
import com.playwright.week5.library.PlaywrightManager;

public class SearchCourseResultPage {
	private static final Logger log = LoggerFactory.getLogger(SearchCourseResultPage.class);

	private PlaywrightManager myPlaywright;
	private Page page;	
	
	public SearchCourseResultPage(Page _page, PlaywrightManager _myPlaywright) {
		this.myPlaywright = _myPlaywright;
		this.page = _page;
		
		myPlaywright.waitUntilElementVisible("div.SearchPage-Header");		
		//myPlaywright.blinkHighlight(page.locator("div.SearchPage-Header"));
	}

	public ProductTypePage selectSearchResultCourse() {
		//myPlaywright.clickElement(page.locator("[aria-label='Our Night Sky']"));		
		myPlaywright.clickElement(page.locator("div.grid.row > div:nth-child(1) > div"));
		
		return new ProductTypePage(page, myPlaywright);
		
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
}
