import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import static org.junit.jupiter.api.Assertions.*;

public class C016_SeleniumStubTestTest {

  @Test
  void todo() {
    ChromeOptions opts = new ChromeOptions();
    opts.addArguments("--headless=new"); // set false for UI
    WebDriver driver = new ChromeDriver(opts);
    try {
      // TODO
      driver.get("https://example.com");
      assertTrue(driver.getTitle().contains("Example Domain"));
    } finally {
      driver.quit();
    }
  }
}
