package com.playwright.week3;

import java.util.List;

import org.testng.annotations.Test;

import com.microsoft.playwright.FrameLocator;
import com.microsoft.playwright.Keyboard;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.KeyboardModifier;
import com.microsoft.playwright.options.MouseButton;

public class PlaywrightActionMethods extends OldBase{
	
	@Test(enabled = false)
	public void websiteNavigationTests() throws Exception {
		String amazonURL = "https://www.amazon.com/";
		page.navigate(amazonURL);
		System.out.println("website: " + page.title());
		
		Thread.sleep(3 * 1000); // 3 seconds delay		
		String homedepotURL = "https://www.homedepot.com/";
		page.navigate(homedepotURL);
		System.out.println("website: " + page.title());
		
		Thread.sleep(3 * 1000); // 3 seconds delay
		// go back to previous web-site or url
		page.goBack();
		System.out.println("Go back...");
		System.out.println("website: " + page.title());
		
		Thread.sleep(3 * 1000); // 3 seconds delay
		page.goForward();
		System.out.println("Forward ...");
		System.out.println("website: " + page.title());
		
		Thread.sleep(3 * 1000); // 3 seconds delay
		page.reload();
		System.out.println("Reload webpage ...");
	}

	
	@Test (enabled = false)
	public void handleCheckBox() throws Exception {		
		// goto check sample web-site
		String url = "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_input_type_checkbox";
		page.navigate(url);
		
		// locate iframe section of the website where the target element is.
		FrameLocator frame =  page.frameLocator("#iframeResult");
		
		
		// 1) locate the bike check box web-element
		Locator bikeCheckBox = frame.locator("#vehicle1");
		boolean boxStatus = bikeCheckBox.isChecked();
		System.out.println("bike check status: " + boxStatus);		
		
		// checking the check-box
		bikeCheckBox.check();
		
		// delay 2 seconds
		Thread.sleep(2 * 1000);
		
		// 2) locate the car check box web-element
		Locator carCheckBox = frame.locator("#vehicle2");
		boolean carBoxStatus = carCheckBox.isChecked();
		System.out.println("car check status: " + carBoxStatus);		
		
		// un-checking the check-box
		carCheckBox.uncheck();
	}

	@Test(enabled = false)
	public void ClickActionTests() {
		// click actions
		page.navigate("https://www.mortgagecalculator.net/");
		
		//1) Regular click
		//page.locator("#Button").click();
		
		//2) Double click
		//page.locator("#Button").dblclick();
		
		//3) Right - click
		Locator amountElement = page.locator("#amount");
		amountElement.click(new Locator.ClickOptions().setButton(MouseButton.RIGHT));
		
		//4) SHIFT + ALT + Click
		Locator amountElement2 = page.locator("#amount");
		amountElement2.click(new Locator.ClickOptions()
				.setModifiers(List.of(KeyboardModifier.SHIFT, KeyboardModifier.ALT)));		
		
		//5) Click and Hold
		Locator myButton = page.locator("#Button");
		//  Hold the click for 3 seconds
		myButton.click(new Locator.ClickOptions().setDelay(3 * 1000));
		
		
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	@Test (enabled = false)
	public void HoverElementTests() {
		page.navigate("https://www.usps.com/");
		
		// locate "Quick Tools" menu
		String cssSelector = "#g-navigation > div > nav > ul > li.qt-nav.menuheader > a.nav-first-element.menuitem";
		page.locator(cssSelector).hover();
	}
	
	
}












































