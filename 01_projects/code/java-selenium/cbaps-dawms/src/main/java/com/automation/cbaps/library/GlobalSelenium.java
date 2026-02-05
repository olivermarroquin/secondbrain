package com.automation.cbaps.library;

import static org.testng.Assert.assertEquals;

import java.io.File;
import java.net.URL;
import java.sql.Timestamp;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Set;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WrapsDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.remote.Augmenter;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.LocalFileDetector;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.safari.SafariDriver;
import org.openqa.selenium.safari.SafariOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import com.google.common.io.Files;

public class GlobalSelenium {
	public static final Logger log = LogManager.getLogger(GlobalSelenium.class);

	private WebDriver driver;
	private boolean isHeadless = false;
	private boolean isRemote = false;
	
	private boolean isDemoMode = false;
	private String hubURL = null;

	public void setHubURL(String hubURL) {
		this.hubURL = hubURL;
	}

	public WebDriver getDriver() {
		return driver;
	}

	public void setDemoMode(boolean isDemoMode) {
		this.isDemoMode = isDemoMode;
	}
	
	public void setHeadless(boolean isHeadless) {
		this.isHeadless = isHeadless;
	}

	public boolean getRemote() {
		return isRemote;
	}

	public void setRemote(boolean isRemote) {
		this.isRemote = isRemote;
	}
	
	public WebDriver startARemoteChromeBrowser() {
		try {
			DesiredCapabilities cap = new DesiredCapabilities();
			ChromeOptions chromeOps = new ChromeOptions();
			if (isHeadless) {
				chromeOps.addArguments("--headless=new");
			}
			chromeOps.merge(cap);
			driver = new RemoteWebDriver(new URL(hubURL), chromeOps);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return driver;
	}

	public WebDriver startAChromeBrowser() {
		try {
			ChromeOptions options = new ChromeOptions();
			if(isHeadless)
			{
				options.addArguments("--headless=new");
			}	
			
			driver = new ChromeDriver(options);
			delay(5);
			driver.manage().window().maximize();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return driver;
	}

	public WebDriver startAFirefoxBrowser() {
		try {
			FirefoxOptions options = new FirefoxOptions();
			if(isHeadless) {
				options.addArguments("--headless=new");
			}			
			driver = new FirefoxDriver(options);
			delay(5);
			driver.manage().window().maximize();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return driver;
	}
	
	public WebDriver startAEdgeBrowser() {
		try {
			EdgeOptions options = new EdgeOptions();
			if(isHeadless) {
				options.addArguments("--headless=new");
			}			
			driver = new EdgeDriver(options);
			delay(5);
			driver.manage().window().maximize();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return driver;
	}

	public WebDriver startASafariBrowser() {
		try {
			// as of today (08/31/2024), Safari browser dosn't support HeadLess Mode.			
			driver = new SafariDriver();
			delay(5);
			driver.manage().window().maximize();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return driver;
	}

	public void cleanUpAfterEachTest() {
		try {
			delay(2);
			// close the browser
			driver.close();
			// kill the driver object or process only if driver is not instance of
			// Firefox driver. It looks like, Firefox browser has some bug
			// when driver.quit() method is executed.
			if (!(driver instanceof FirefoxDriver)) {
				driver.quit();
				log.info("driver.quit() method is executed....");
			}

		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void gotoWebsite(String url) {
		try {
			driver.get(url);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public String getWebsiteTitle() {
		String title = null;
		try {
			title = driver.getTitle();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return title;
	}

	public void enterText(By by, String textValue) {
		try {
			WebElement element = driver.findElement(by);
			highlightElement(element);
			element.clear();
			element.sendKeys(textValue);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void enterText(WebElement element, String textValue) {
		try {
			highlightElement(element);
			element.clear();
			element.sendKeys(textValue);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void selectDropDown(By by, String visibleTextOption) {
		try {
			WebElement element = driver.findElement(by);
			highlightElement(element);
			Select select = new Select(element);
			select.selectByVisibleText(visibleTextOption);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void clickButton(By by) {
		try {
			WebElement element = driver.findElement(by);
			highlightElement(element);
			element.click();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void clickButton(WebElement element) {
		try {
			highlightElement(element);
			element.click();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void delay(double inSeconds) {
		try {
			long millisec = (long) (inSeconds * 1000);
			Thread.sleep(millisec);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void scrollToElement(WebElement element) {
		try {
			highlightElement(element);
			JavascriptExecutor js = (JavascriptExecutor) driver;
			js.executeScript("arguments[0].scrollIntoView();", element);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void scrollIntoView(WebElement element) {
		try {
			highlightElement(element);
			Actions actions = new Actions(driver);
			actions.scrollToElement(element);
			actions.build().perform();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void fileUpload(By by, String uploadFilePath) {
		try {
			WebElement uploadElem = driver.findElement(by);
			highlightElement(uploadElem);
			scrollIntoView(uploadElem);
			// delay(3);
			String abPath = getAbsuluteFilePath(uploadFilePath);
			if (isRemote) {
				((RemoteWebDriver) driver).setFileDetector(new LocalFileDetector());
			}

			uploadElem.sendKeys(abPath);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void handleCheckBox(By by, boolean isUserCheckBox) {
		try {
			WebElement checkBoxElement;
			highlightElement(by);
			// user wants to check the box
			if (isUserCheckBox == true) {
				checkBoxElement = driver.findElement(by);
				// get checkbox state
				boolean checkboxState = checkBoxElement.isSelected();
				if (checkboxState == true) {
					// do nothing
					log.debug("1) user wants to checkbox, box is already checked, selenium do nothing.");
				} else {
					checkBoxElement.click();
					log.debug("2) user wants to checkbox, box is Not checked, selenium do click.");
				}
			} else {
				checkBoxElement = driver.findElement(by);
				// get checkbox state
				boolean checkboxState = checkBoxElement.isSelected();
				if (checkboxState == true) {
					checkBoxElement.click();
					log.debug("3) user wants to uncheck box, box is already checked, selenium do click.");
				} else {
					// do nothing
					log.debug("4) user wants to uncheck box, box is Not checked, selenium do nothing.");
				}
			}
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	// explicit wait
	public WebElement waitForElementVisibility(By by) {
		WebElement element = null;
		try {
			WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(30));
			element = wait.until(ExpectedConditions.visibilityOfElementLocated(by));
			if (element == null) {
				log.info("Element is not visible within 30 seconds.");
			}
			highlightElement(element);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return element;
	}

	public void highlightElement(WebElement element) {
		try {
			if (isDemoMode) {
				for (int i = 1; i < 4; i++) {
					WrapsDriver wrappedElement = (WrapsDriver) element;
					JavascriptExecutor js = (JavascriptExecutor) wrappedElement.getWrappedDriver();
					js.executeScript("arguments[0].setAttribute('style', arguments[1]);", element,
							"color: red; border: 2px solid yellow");
					delay(0.5);
					js.executeScript("arguments[0].setAttribute('style', arguments[1]);", element, "");
					delay(0.5);
				}
			}
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void highlightElement(By by) {
		try {
			WebElement element = driver.findElement(by);
			highlightElement(element);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void clickHiddenElement(By by) {
		try {
			WebElement element = driver.findElement(by);
			highlightElement(element);
			JavascriptExecutor js = (JavascriptExecutor) driver;
			js.executeScript("arguments[0].click();", element);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void clickHiddenElement(WebElement element) {
		try {
			highlightElement(element);
			JavascriptExecutor js = (JavascriptExecutor) driver;
			js.executeScript("arguments[0].click();", element);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public WebDriver swtichToBrowserWindowByIndex(int index) {
		int totalBrowsers = 0;
		try {
			Set<String> setAllBrowsers = driver.getWindowHandles();
			totalBrowsers = setAllBrowsers.size();
			if (index < totalBrowsers) {
				List<String> listBrowsers = new ArrayList<String>();
				for (String browser : setAllBrowsers) {
					listBrowsers.add(browser);
				}
				String windowName = listBrowsers.get(index);
				driver = driver.switchTo().window(windowName);
			} else {
				int tempBrowser = index + 1;
				System.err.println("There are only [" + totalBrowsers + "] open browser availabe,"
						+ "can't switch to browser number [" + tempBrowser + "], that doesn't exist!");
			}
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return driver;
	}

	public void moveToElement(By by) {
		try {
			WebElement element = driver.findElement(by);
			highlightElement(element);
			Actions action = new Actions(driver);
			action.moveToElement(element).build().perform();
			delay(0.5);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void moveToElement(WebElement fromElem, WebElement toElem) {
		try {
			highlightElement(fromElem);
			Actions action1 = new Actions(driver);
			Actions action2 = action1.moveToElement(fromElem);
			delay(2);
			highlightElement(toElem);
			action2.moveToElement(toElem).build().perform();
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
	}

	public void capureScreenshot(String screenshotFileName, String filePath) {
		String finalScreenshotPath = null;
		try {
			String timeStamp = getCurrentTime();
			// default location for the screenshot file
			if (filePath.isEmpty()) {
				checkDirectory("target/screenshots/");
				finalScreenshotPath = "target/screenshots/" + screenshotFileName + "_" + timeStamp + ".png";
			} else {
				checkDirectory(filePath);
				finalScreenshotPath = filePath + screenshotFileName + "_" + timeStamp + ".png";
			}
			if (isRemote) {
				driver = new Augmenter().augment(driver);
			}
			File scrFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
			Files.copy(scrFile, new File(finalScreenshotPath));
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		String fullPath = getAbsuluteFilePath(finalScreenshotPath);
		log.info("Screenshot location: " + fullPath);
	}

	////////////////////// this is java utility methods///
	//////////// temporarily we will have them here //////

	public String getAbsuluteFilePath(String relativePath) {
		String finalPath = null;
		try {
			File file = new File(relativePath);
			finalPath = file.getAbsolutePath();
			log.info("file full path: " + finalPath);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return finalPath;
	}

	public String getCurrentTime() {
		String finalTimeStamp = null;
		try {
			Date date = new Date();
			String tempTime = new Timestamp(date.getTime()).toString();
			finalTimeStamp = tempTime.replace('-', '_').replace(':', '_').replace('.', '_').replace(' ', '_')
					.replaceAll("_", "");
			// System.out.println("current time: " + tempTime);
			log.info("timestamp: " + finalTimeStamp);
		} catch (Exception e) {
			log.error("Error: ", e);
			assertEquals(true, false);
		}
		return finalTimeStamp;
	}

	public void checkDirectory(String inputPath) {
		try {
			File file1 = new File(inputPath);
			String abPath = file1.getAbsolutePath();
			File file2 = new File(abPath);

			if (!file2.exists()) {
				if (file2.mkdirs()) {
					log.info("Directories are created...");
					// System.out.println("Directories are created...");
				} else {
					log.info("Directories Not created...");
					// System.out.println("Directories are created...");
				}
			}
		} catch (Exception e) {
			log.error("Error: ", e);
			// System.out.println(e);
			assertEquals(true, false);
		}
	}

//	public static void main(String[] args) {
//		checkDirectory("C:/abc/bc123/ca22/frank1/folder2/data.txt");
//	}
}
