import com.microsoft.playwright.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class SmokeTest {
  static Playwright playwright;
  static Browser browser;

  @BeforeAll
  static void launchBrowser() {
    playwright = Playwright.create();
    browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setHeadless(false));
  }

  @AfterAll
  static void closeBrowser() {
    if (browser != null) browser.close();
    if (playwright != null) playwright.close();
  }

  @Test
  void homepageLoads() {
    Page page = browser.newPage();
    page.navigate("https://example.com");
    assertTrue(page.title().contains("Example Domain"));
    page.close();
  }
}
