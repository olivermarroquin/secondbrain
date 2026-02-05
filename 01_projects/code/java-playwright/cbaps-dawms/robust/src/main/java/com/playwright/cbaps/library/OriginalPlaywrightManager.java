package com.playwright.week5.library;

import static org.assertj.core.api.Assertions.assertThat;

import java.awt.Dimension;
import java.awt.Toolkit;
import java.io.File;
import java.nio.file.Paths;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.BrowserType.LaunchOptions;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.microsoft.playwright.options.WaitForSelectorState;

import net.datafaker.Faker;

public class PlaywrightManager {
	private static final Logger log = LoggerFactory.getLogger(PlaywrightManager.class);
	private Dimension screenSize;

	private Playwright playwright;
	private Browser browser;
	private BrowserContext browserContext;
	public Page page;

	private String browserType = "chrome"; // Options: "chrome", "firefox", "webkit", "msedge"
	private boolean isMaximized = true;//
	private boolean isHeadless = false;
	private boolean isIgnoreCertificateErros = true;
	private boolean isVideoRecording = true;
	private boolean isDemoMode = false;

	// constructor
	public PlaywrightManager() {

	}

	// Start playwright object
	public void initPlaywright() {
		try {
			playwright = Playwright.create();

			// Choose browser dynamically
			BrowserType browserChoice = null;
			switch (browserType.toLowerCase()) {
			case "firefox":
				browserChoice = playwright.firefox();
				break;
			case "webkit":
				browserChoice = playwright.webkit();
				break;
			case "msedge":
				browserChoice = playwright.chromium();
			case "chrome":
			default:
				browserChoice = playwright.chromium();
				break;
			}

			// Set launch options
			LaunchOptions launchOption = new BrowserType.LaunchOptions().setChannel(browserType) // dynamically select
																									// browser
					// Java ternary conditional operator
					.setArgs(isMaximized ? Arrays.asList("--start-maximized") : Arrays.asList())
					.setHeadless(isHeadless); // if false, run in headed mode

			browser = browserChoice.launch(launchOption);

			// Set browser context options
			Browser.NewContextOptions contextOptions = new Browser.NewContextOptions()
					.setIgnoreHTTPSErrors(isIgnoreCertificateErros); // Ignore certificate error

			if (isMaximized) {
				// Call maximize only for non-Chromium browsers
				if (browserType.equalsIgnoreCase("firefox") || browserType.equalsIgnoreCase("webkit")) {
					screenSize = Toolkit.getDefaultToolkit().getScreenSize();
				} else {
					contextOptions.setViewportSize(null); // Maximize if true for Chromium browsers
				}
			} else {
				contextOptions.setViewportSize(1280, 720); // Default size when not maximized
			}

			if (isVideoRecording == true) {
				contextOptions.setViewportSize(null) // Maximize browser
						.setRecordVideoDir(Paths.get(getAbsoluteFilePath("target/videos/"))) // Save video in 'videos'
																								// folder
						.setRecordVideoSize(1280, 720); // Set resolution
			}

			browserContext = browser.newContext(contextOptions);

			log.info("Playwright & browser initialized sucessfully.");

		} catch (Exception e) {
			log.error("Failed to initialize Playwright: {}", e.getMessage(), e);
			assertThat(false).as("initPlaywright method failed.").isTrue();
		}
	}

	// close or clean-up playwright objects
	public void closePlaywright() {
		try {
			sleep(1);
			if (browserContext != null) {
				browserContext.close();
			}
			if (browser != null) {
				browser.close();
			}
			if (playwright != null) {
				playwright.close();
			}
			log.info("Playwright session closed.");
		} catch (Exception e) {
			log.error("Failed to close Playwright: {}", e.getMessage(), e);
			assertThat(false).as("closePlaywright method failed.").isTrue();
		}
	}

	// open new page browser
	public Page openNewBrowserPage() {
		try {
			page = browserContext.newPage();
			sleep(5);
			if (isMaximized) {
				if (browserType.equalsIgnoreCase("firefox") || browserType.equalsIgnoreCase("webkit")) {
					page.setViewportSize(screenSize.width, screenSize.height);
				}
			}
			// System.out.println("Open '" + browserType + "' browser.");
			log.info("Opened '{}' browser page.", browserType);
		} catch (Exception e) {
			log.error("Failed to open browser page: {}", e.getMessage(), e);
			assertThat(false).as("openNewBrowserPage method failed.").isTrue();
		}
		return page;
	}

	// close page object
	public void closePage() {
		try {
			sleep(1);
			if (page != null) {
				page.close();
			}
			log.info("Closed '{}' browser page.", browserType);
		} catch (Exception e) {
			log.error("Error closing page: {}", e.getMessage(), e);
			assertThat(false).as("closePage method failed.").isTrue();
		}
	}

	public void blinkHighlight(Page page, Locator element) {
		try {
			if (isDemoMode) {
				scrollToElementView(element);
				for (int i = 0; i < 3; i++) { // Repeat 3 times
					// Apply highlight
					element.evaluate(
							"el => { el.style.border = '3px solid red'; el.style.backgroundColor = 'yellow'; }");
					page.waitForTimeout(500); // Wait 0.5 seconds

					// Remove highlight
					element.evaluate("el => { el.style.border = ''; el.style.backgroundColor = ''; }");
					page.waitForTimeout(500); // Wait 0.5 seconds
				}
			}
		} catch (Exception e) {
			log.error("Error in blinkHighlight: {}", e.getMessage(), e);
			assertThat(false).as("blinkHighlight method failed.").isTrue();
		}
	}

	public void blinkHighlight(Locator element) {
		blinkHighlight(page, element);
	}

	public void captureScreenshotFullPage(String screenshotPathName) {
		try {
			// Capture full page screenshot
			log.info("capturing full page screenshot --->    ");
			String newScreenshotPathName = null;
			if (screenshotPathName.trim() != null || !screenshotPathName.trim().isEmpty()) {
				newScreenshotPathName = "target/screenshot/" + screenshotPathName + ".png";
			} else {
				newScreenshotPathName = "target/screenshot/screenshot.png";
			}
			log.info("location: " + getAbsoluteFilePath(newScreenshotPathName));
			page.screenshot(new Page.ScreenshotOptions().setPath(Paths.get(newScreenshotPathName)).setFullPage(true));
		} catch (Exception e) {
			log.error("Failed to capture full-page screenshot: {}", e.getMessage(), e);
			assertThat(false).as("captureScreenshotFullPage method failed.").isTrue();
		}
	}

	public void captureScreenshotDisplayViewPage(String screenshotPathName) {
		try {
			// Capture only display page view screenshot
			log.info("capturing display view screenshot ---> ");

			String newScreenshotPathName = null;
			if (screenshotPathName.trim() != null || !screenshotPathName.trim().isEmpty()) {
				newScreenshotPathName = "target/screenshot/" + screenshotPathName + ".png";
			} else {
				newScreenshotPathName = "target/screenshot/screenshot.png";
			}
			log.info("location: " + getAbsoluteFilePath(newScreenshotPathName));
			page.screenshot(new Page.ScreenshotOptions().setPath(Paths.get(newScreenshotPathName)));
		} catch (Exception e) {
			log.error("Failed to capture display view screenshot: {}", e.getMessage(), e);
			assertThat(false).as("captureScreenshotDisplayViewPage method failed.").isTrue();
		}
	}

	public String captureScreenshotBase64() {
		String base64Screenshot = null;
		try {
			// Capture screenshot in Base64 format for embed into html report files
			byte[] screenshotBytes = page.screenshot();
			base64Screenshot = Base64.getEncoder().encodeToString(screenshotBytes);
			log.debug("Base64 screenshot captured: {}", base64Screenshot);
		} catch (Exception e) {
			log.error("Error capturing Base64 screenshot: {}", e.getMessage(), e);
			assertThat(false).as("captureScreenshotBase64 method failed.").isTrue();
		}
		return base64Screenshot;
	}

	public void enterText(Locator elementLocator, String inputText) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.fill(inputText);
			log.info("Entered text: '{}'", inputText);
		} catch (Exception e) {
			log.error("Error entering text: {}", e.getMessage(), e);
			assertThat(false).as("enterText method failed.").isTrue();
		}
	}

	public void selectCheckBoxOrRadioButton(Locator elementLocator) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.check();
			log.info("Checkbox or radio button selected.");
		} catch (Exception e) {
			log.error("Error selecting checkbox/radio: {}", e.getMessage(), e);
			assertThat(false).as("selectCheckBoxOrRadioButton method failed.").isTrue();
		}
	}

	public void selectDropdown(Locator elementLocator, String inputSelectOption) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.selectOption(inputSelectOption);
			log.info("Selected dropdown option: '{}'", inputSelectOption);
		} catch (Exception e) {
			log.error("Error selecting dropdown: {}", e.getMessage(), e);
			assertThat(false).as("selectDropdown method failed.").isTrue();
		}
	}

	public void clickElement(Locator elementLocator) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.click();
			log.info("Element clicked.");
		} catch (Exception e) {
			log.error("Error clicking element: {}", e.getMessage(), e);
			assertThat(false).as("clickElement method failed.").isTrue();
		}
	}

	public void scrollToElementView(Locator elementLocator) {
		try {
			elementLocator.scrollIntoViewIfNeeded();
			log.debug("Scrolled to element.");
		} catch (Exception e) {
			log.error("Error scrolling to element: {}", e.getMessage(), e);
			assertThat(false).as("clickElement method failed.").isTrue();
		}
	}

	public void fileUpload(Locator elementLocator, String filePath) {
		// file upload
		try {
			blinkHighlight(elementLocator);
			elementLocator.setInputFiles(Paths.get(filePath));
			log.info("File uploaded: '{}'", getAbsoluteFilePath(filePath));
		} catch (Exception e) {
			log.error("Error uploading file: {}", e.getMessage(), e);
			assertThat(false).as("fileUpload method failed.").isTrue();
		}
	}

	public void waitUntilElementVisible(String locatorCssORxpath) {
		try {
			// wait until element is visible on the web-page
			page.locator(locatorCssORxpath)
					.waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.VISIBLE));
			log.info("Element is now visible: '{}'", locatorCssORxpath);
			
			blinkHighlight(page.locator(locatorCssORxpath));			
		} catch (Exception e) {
			log.error("Error waiting until element visibility: {}", e.getMessage(), e);
			assertThat(false).as("waitUntilElementVisible method failed.").isTrue();
		}
	}

	public void maximizeWindow() {
		log.debug("maximizing browser window ....");
		page.evaluate("window.moveTo(0,0); window.resizeTo(screen.width, screen.height);");
	}

	public void maximizeFirefoxWebkitBrowser() {
		// JavaScript Trick: Maximize WebKit & Firefox using JS
		if (browserType.equalsIgnoreCase("firefox") || browserType.equalsIgnoreCase("webkit")) {

			log.info("maximizing browser window ....");
			page.evaluate("window.resizeTo(screen.availWidth, screen.availHeight);");
		}
	}

	public void pressEnterKey(Locator elementLocator) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.press("Enter");
			log.info("press enter key");
		} catch (Exception e) {
			log.error("Error Press Entry Key: {}", e.getMessage(), e);
			assertThat(false).as("pressEnterKey method failed.").isTrue();
		}
	}
	
	public void clickHiddenElement(Locator elementLocator) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.dispatchEvent("click");
			log.info("dispachEvent click");
		} catch (Exception e) {
			log.error("Error dispatchEvent click: {}", e.getMessage(), e);
			assertThat(false).as("clickHiddenElement method failed.").isTrue();
		}
	}
	
	
	
	

	////////// Java Methods ////////// Please write java only method in below
	////////// ////////

	public String getAbsoluteFilePath(String relativeFilePath) {
		String finalAbsolutePath = null;

		File file = new File(relativeFilePath);
		finalAbsolutePath = file.getAbsolutePath();

		return finalAbsolutePath;
	}

	public void sleep(double inSeconds) {
		try {
			long inMilliSec = (long) inSeconds * 1000;
			Thread.sleep(inMilliSec);
		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("sleep method failed.").isTrue();
		}
	}
	
	public String getRandomEmail() {
		Faker faker = new Faker();
		String randomEmail = faker.internet().emailAddress();
		log.info("fake email created: " + randomEmail);
		return randomEmail;
	}
	
	public String getRandomPassword(int charactor) {
		
		Faker faker = new Faker();
		String randomPassword = faker.regexify("[A-Za-z0-9]{"+ charactor +"}");
		log.info("fake password created: " + randomPassword);
		return randomPassword;
	}
	
	public String getRandomPassword(String spcecialCharachters , int length ) {

	    Faker faker = new Faker();
	    // Include A-Z, a-z, 0-9, and special characters !@#$%^&*
	    String regexPattern = "[A-Za-z0-9"+spcecialCharachters+"]{" + length + "}";
	    String randomPassword = faker.regexify(regexPattern);
	    log.info("Fake password created: " + randomPassword);

	    return randomPassword;
	}
		
	public String getRandomPassword(int length, String specialChars) {
	    if (length < 6) {
	        throw new IllegalArgumentException("Password length must be at least 6 to include special characters.");
	    }

	    String upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	    String lower = "abcdefghijklmnopqrstuvwxyz";
	    String digits = "0123456789";

	    String allChars = upper + lower + digits + specialChars;
	    SecureRandom random = new SecureRandom();
	    List<Character> passwordChars = new ArrayList<>();

	    // Add at least one special character
	    passwordChars.add(specialChars.charAt(random.nextInt(specialChars.length())));

	    // Fill the rest with random characters from full pool
	    for (int i = 1; i < length; i++) {
	        passwordChars.add(allChars.charAt(random.nextInt(allChars.length())));
	    }

	    // Shuffle to randomize special char position
	    Collections.shuffle(passwordChars, random);

	    // Build the final password
	    StringBuilder password = new StringBuilder();
	    for (char c : passwordChars) {
	        password.append(c);
	    }

	    log.info("Generated password: " + password);
	    return password.toString();
	}

//	public static void main(String[] args) {
//		PlaywrightManager testManager = new PlaywrightManager();
//		testManager.getRandomEmail();
//		testManager.getRandomPassword(8);
//		testManager.getRandomPassword(8, "@$*");
//		
//		testManager.getRandomPassword("$%^&*", 10);
//	}
	
}




















