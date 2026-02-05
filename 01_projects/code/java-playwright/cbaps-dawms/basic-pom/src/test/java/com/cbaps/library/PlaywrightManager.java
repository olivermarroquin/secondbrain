package com.cbaps.library;

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

/**
 * PlaywrightManager: Wrapper around Playwright primitives
 * Manages Playwright, Browser, BrowserContext, and Page objects
 * Provides common actions for CBAPS automation
 */
public class PlaywrightManager {
	private static final Logger log = LoggerFactory.getLogger(PlaywrightManager.class);
	private Dimension screenSize;

	private Playwright playwright;
	private Browser browser;
	private BrowserContext browserContext;
	public Page page;

	private String browserType = "chrome"; // Options: "chrome", "firefox", "webkit", "msedge"
	private boolean isMaximized = true;
	private boolean isHeadless = false;
	private boolean isIgnoreCertificateErrors = true;
	private boolean isVideoRecording = true;
	private boolean isDemoMode = false;

	public PlaywrightManager() {
	}

	/**
	 * Initialize Playwright with browser and context options
	 */
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
			LaunchOptions launchOption = new BrowserType.LaunchOptions().setChannel(browserType)
					.setArgs(isMaximized ? Arrays.asList("--start-maximized") : Arrays.asList())
					.setHeadless(isHeadless);

			browser = browserChoice.launch(launchOption);

			// Set browser context options
			Browser.NewContextOptions contextOptions = new Browser.NewContextOptions()
					.setIgnoreHTTPSErrors(isIgnoreCertificateErrors);

			if (isMaximized) {
				if (browserType.equalsIgnoreCase("firefox") || browserType.equalsIgnoreCase("webkit")) {
					screenSize = Toolkit.getDefaultToolkit().getScreenSize();
				} else {
					contextOptions.setViewportSize(null);
				}
			} else {
				contextOptions.setViewportSize(1280, 720);
			}

			if (isVideoRecording == true) {
				contextOptions.setViewportSize(null)
						.setRecordVideoDir(Paths.get(getAbsoluteFilePath("target/videos/")))
						.setRecordVideoSize(1280, 720);
			}

			browserContext = browser.newContext(contextOptions);

			log.info("Playwright & browser initialized successfully.");

		} catch (Exception e) {
			log.error("Failed to initialize Playwright: {}", e.getMessage(), e);
			assertThat(false).as("initPlaywright method failed.").isTrue();
		}
	}

	/**
	 * Close Playwright objects
	 */
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

	/**
	 * Open new browser page
	 */
	public Page openNewBrowserPage() {
		try {
			page = browserContext.newPage();
			sleep(5);
			if (isMaximized) {
				if (browserType.equalsIgnoreCase("firefox") || browserType.equalsIgnoreCase("webkit")) {
					page.setViewportSize(screenSize.width, screenSize.height);
				}
			}
			log.info("Opened '{}' browser page.", browserType);
		} catch (Exception e) {
			log.error("Failed to open browser page: {}", e.getMessage(), e);
			assertThat(false).as("openNewBrowserPage method failed.").isTrue();
		}
		return page;
	}

	/**
	 * Close page object
	 */
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

	/**
	 * Highlight element by blinking (for demo mode)
	 */
	public void blinkHighlight(Page page, Locator element) {
		try {
			if (isDemoMode) {
				scrollToElementView(element);
				for (int i = 0; i < 3; i++) {
					element.evaluate(
							"el => { el.style.border = '3px solid red'; el.style.backgroundColor = 'yellow'; }");
					page.waitForTimeout(500);
					element.evaluate("el => { el.style.border = ''; el.style.backgroundColor = ''; }");
					page.waitForTimeout(500);
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

	/**
	 * Capture full page screenshot
	 */
	public void captureScreenshotFullPage(String screenshotPathName) {
		try {
			log.info("Capturing full page screenshot...");
			String newScreenshotPathName = null;
			if (screenshotPathName.trim() != null || !screenshotPathName.trim().isEmpty()) {
				newScreenshotPathName = "target/screenshot/" + screenshotPathName + ".png";
			} else {
				newScreenshotPathName = "target/screenshot/screenshot.png";
			}
			log.info("Location: " + getAbsoluteFilePath(newScreenshotPathName));
			page.screenshot(new Page.ScreenshotOptions().setPath(Paths.get(newScreenshotPathName)).setFullPage(true));
		} catch (Exception e) {
			log.error("Failed to capture full-page screenshot: {}", e.getMessage(), e);
			assertThat(false).as("captureScreenshotFullPage method failed.").isTrue();
		}
	}

	/**
	 * Capture Base64 screenshot for embedding in reports
	 */
	public String captureScreenshotBase64() {
		String base64Screenshot = null;
		try {
			byte[] screenshotBytes = page.screenshot();
			base64Screenshot = Base64.getEncoder().encodeToString(screenshotBytes);
			log.debug("Base64 screenshot captured.");
		} catch (Exception e) {
			log.error("Error capturing Base64 screenshot: {}", e.getMessage(), e);
			assertThat(false).as("captureScreenshotBase64 method failed.").isTrue();
		}
		return base64Screenshot;
	}

	// --- Wrapped helpers used by Page Objects ---

	/**
	 * Click element (wrapper)
	 */
	public void click(Locator elementLocator) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.click();
			log.info("Element clicked.");
		} catch (Exception e) {
			log.error("Error clicking element: {}", e.getMessage(), e);
			assertThat(false).as("clickElement method failed.").isTrue();
		}
	}

	/**
	 * Enter text (wrapper)
	 */
	public void type(Locator elementLocator, String inputText) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.fill(inputText);
			log.info("Entered text: '{}'", inputText);
		} catch (Exception e) {
			log.error("Error entering text: {}", e.getMessage(), e);
			assertThat(false).as("enterText method failed.").isTrue();
		}
	}

	/**
	 * Wait for element visibility
	 */
	public void waitVisible(String locatorCssOrXpath) {
		try {
			page.locator(locatorCssOrXpath)
					.waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.VISIBLE));
			log.info("Element is now visible: '{}'", locatorCssOrXpath);
			blinkHighlight(page.locator(locatorCssOrXpath));
		} catch (Exception e) {
			log.error("Error waiting until element visibility: {}", e.getMessage(), e);
			assertThat(false).as("waitUntilElementVisible method failed.").isTrue();
		}
	}

	/**
	 * Scroll to element view
	 */
	public void scrollToElementView(Locator elementLocator) {
		try {
			elementLocator.scrollIntoViewIfNeeded();
			log.debug("Scrolled to element.");
		} catch (Exception e) {
			log.error("Error scrolling to element: {}", e.getMessage(), e);
			assertThat(false).as("scrollToElementView method failed.").isTrue();
		}
	}

	/**
	 * Select dropdown option
	 */
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

	/**
	 * File upload
	 */
	public void fileUpload(Locator elementLocator, String filePath) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.setInputFiles(Paths.get(filePath));
			log.info("File uploaded: '{}'", getAbsoluteFilePath(filePath));
		} catch (Exception e) {
			log.error("Error uploading file: {}", e.getMessage(), e);
			assertThat(false).as("fileUpload method failed.").isTrue();
		}
	}

	/**
	 * Press Enter key
	 */
	public void pressEnterKey(Locator elementLocator) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.press("Enter");
			log.info("Pressed enter key");
		} catch (Exception e) {
			log.error("Error pressing Enter key: {}", e.getMessage(), e);
			assertThat(false).as("pressEnterKey method failed.").isTrue();
		}
	}

	/**
	 * Click hidden element using dispatch event
	 */
	public void clickHiddenElement(Locator elementLocator) {
		try {
			blinkHighlight(elementLocator);
			elementLocator.dispatchEvent("click");
			log.info("DispatchEvent click performed");
		} catch (Exception e) {
			log.error("Error performing dispatchEvent click: {}", e.getMessage(), e);
			assertThat(false).as("clickHiddenElement method failed.").isTrue();
		}
	}

	// --- Java utility methods ---

	/**
	 * Get absolute file path
	 */
	public String getAbsoluteFilePath(String relativeFilePath) {
		String finalAbsolutePath = null;
		File file = new File(relativeFilePath);
		finalAbsolutePath = file.getAbsolutePath();
		return finalAbsolutePath;
	}

	/**
	 * Sleep for specified seconds
	 */
	public void sleep(double inSeconds) {
		try {
			long inMilliSec = (long) inSeconds * 1000;
			Thread.sleep(inMilliSec);
		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("sleep method failed.").isTrue();
		}
	}

	/**
	 * Generate random email
	 */
	public String getRandomEmail() {
		Faker faker = new Faker();
		String randomEmail = faker.internet().emailAddress();
		log.info("Fake email created: " + randomEmail);
		return randomEmail;
	}

	/**
	 * Generate random password with special characters
	 */
	public String getRandomPassword(String specialCharacters, int length) {
		Faker faker = new Faker();
		String regexPattern = "[A-Za-z0-9" + specialCharacters + "]{" + length + "}";
		String randomPassword = faker.regexify(regexPattern);
		log.info("Fake password created: " + randomPassword);
		return randomPassword;
	}

	/**
	 * Generate secure random password
	 */
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

		passwordChars.add(specialChars.charAt(random.nextInt(specialChars.length())));

		for (int i = 1; i < length; i++) {
			passwordChars.add(allChars.charAt(random.nextInt(allChars.length())));
		}

		Collections.shuffle(passwordChars, random);

		StringBuilder password = new StringBuilder();
		for (char c : passwordChars) {
			password.append(c);
		}

		log.info("Generated password: " + password);
		return password.toString();
	}
}
