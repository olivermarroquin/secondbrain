import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import static org.junit.jupiter.api.Assertions.*;

public class SmokeTest {

  @Test
  void homepageLoads() {
    ChromeOptions opts = new ChromeOptions();
    opts.addArguments("--headless=new"); // flip off if you want UI
    WebDriver driver = new ChromeDriver(opts); // Selenium Manager handles driver
    try {
      driver.get("https://example.com");
      assertTrue(driver.getTitle().contains("Example Domain"));
    } finally {
      driver.quit();
    }
  }
}
