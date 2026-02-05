# CBAPS & DAWMS Java Selenium Automation Framework

## 🎯 Enterprise-Grade Automation Framework

**Comprehensive Java Selenium framework matching TypeScript version's robustness with:**

- ✅ **Selenium WebDriver** with enhanced GlobalSelenium (50+ methods)
- ✅ **REST Assured** for API testing
- ✅ **TestNG** for test execution and parallel testing
- ✅ **ExtentReports** for beautiful HTML reports
- ✅ **Data-Driven Testing** with Apache POI (Excel)
- ✅ **Page Object Model** with 15-22 methods per page
- ✅ **6-7 Test Scenarios** per application
- ✅ **Parallel Execution** support
- ✅ **Log4j2** for comprehensive logging

---

## 📁 Complete Project Structure

```
java-selenium-automation/
├── pom.xml                                    # Maven dependencies
├── testng.xml                                  # TestNG suite configuration
├── testng-parallel.xml                         # Parallel execution config
├── README.md                                   # This file
├── SUMMARY.md                                  # Framework summary
│
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── automation/
│   │               ├── cbaps/                 # CBAPS Framework
│   │               │   ├── library/
│   │               │   │   ├── GlobalSelenium.java          # 50+ Selenium methods
│   │               │   │   ├── Base.java                    # TestNG base class
│   │               │   │   ├── ExtentManager.java           # Report manager
│   │               │   │   ├── ExcelManager.java            # Excel data reader
│   │               │   │   └── APIHelper.java               # REST Assured helper
│   │               │   ├── models/
│   │               │   │   ├── RequisitionData.java         # Requisition POJO
│   │               │   │   ├── FundingLineData.java         # Funding line POJO
│   │               │   │   ├── ApproverData.java            # Approver POJO
│   │               │   │   └── ValidationResult.java        # Validation result
│   │               │   ├── pages/
│   │               │   │   ├── PortalHomePage.java          # 8 methods
│   │               │   │   ├── CBAPSDashboardPage.java      # 12 methods
│   │               │   │   ├── RequisitionPage.java         # 22 methods ⭐
│   │               │   │   ├── FundingLinesPage.java        # 18 methods ⭐
│   │               │   │   ├── RoutingApprovalPage.java     # 10 methods
│   │               │   │   └── StatusTrackerPage.java       # 12 methods
│   │               │   ├── api/
│   │               │   │   └── CBAPS_APITests.java          # REST Assured tests
│   │               │   └── tests/
│   │               │       ├── CBAPSEndToEndTests.java      # 6 scenarios ⭐
│   │               │       └── CBAPSDataDrivenTests.java    # Excel-driven tests
│   │               │
│   │               └── dawms/                 # DAWMS Framework
│   │                   ├── library/
│   │                   │   ├── GlobalSelenium.java          # Shared wrapper
│   │                   │   ├── Base.java
│   │                   │   ├── ExtentManager.java
│   │                   │   ├── ExcelManager.java
│   │                   │   └── APIHelper.java
│   │                   ├── models/
│   │                   │   ├── SubmissionData.java
│   │                   │   ├── ReviewerData.java
│   │                   │   ├── SignerData.java
│   │                   │   └── ValidationResult.java
│   │                   ├── pages/
│   │                   │   ├── PortalHomePage.java
│   │                   │   ├── DAWMSDashboardPage.java
│   │                   │   ├── SubmissionIntakePage.java
│   │                   │   ├── ReviewerAssignmentPage.java
│   │                   │   ├── SignatureRoutingPage.java
│   │                   │   └── MilestoneStatusPage.java
│   │                   ├── api/
│   │                   │   └── DAWMS_APITests.java
│   │                   └── tests/
│   │                       ├── DAWMSEndToEndTests.java      # 7 scenarios ⭐
│   │                       └── DAWMSDataDrivenTests.java
│   │
│   └── test/
│       └── resources/
│           ├── testdata/
│           │   ├── cbaps-test-data.xlsx        # CBAPS test data
│           │   └── dawms-test-data.xlsx        # DAWMS test data
│           └── config/
│               └── log4j2.xml                   # Logging configuration
```

---

## 🚀 Quick Start

### Prerequisites
- JDK 11 or higher
- Maven 3.6+
- Chrome/Firefox/Edge browser

### Setup

```bash
# Clone/Extract the project
cd java-selenium-automation

# Install dependencies
mvn clean install -DskipTests

# Verify setup
mvn test -Dtest=CBAPSEndToEndTests#completeWorkflowTest
```

### Running Tests

```bash
# Run all tests
mvn test

# Run CBAPS tests only
mvn test -Dtest=CBAPSEndToEndTests

# Run DAWMS tests only
mvn test -Dtest=DAWMSEndToEndTests

# Run with specific browser
mvn test -Dbrowser=chrome
mvn test -Dbrowser=firefox
mvn test -Dbrowser=edge

# Run in headless mode
mvn test -Dheadless=true

# Run with parallel execution
mvn test -DsuiteXmlFile=testng-parallel.xml

# Run data-driven tests
mvn test -Dtest=CBAPSDataDrivenTests

# Run API tests
mvn test -Dtest=CBAPS_APITests
```

### View Reports

```bash
# Open ExtentReports
open target/extent-reports/extent-report.html

# View TestNG reports
open target/surefire-reports/index.html

# View logs
cat target/logs/automation.log
```

---

## 📚 Enhanced GlobalSelenium (50+ Methods)

### Original Methods (from your file) ✅
- `startAChromeBrowser()`, `startAFirefoxBrowser()`, `startAEdgeBrowser()`, `startASafariBrowser()`
- `startARemoteChromeBrowser()` - Selenium Grid support
- `cleanUpAfterEachTest()`
- `gotoWebsite(String url)`
- `getWebsiteTitle()`
- `enterText(By/WebElement, String)`
- `selectDropDown(By, String)`
- `clickButton(By/WebElement)`
- `delay(double)`
- `scrollToElement(WebElement)`, `scrollIntoView(WebElement)`
- `fileUpload(By, String)`
- `handleCheckBox(By, boolean)`
- `waitForElementVisibility(By)`
- `highlightElement(By/WebElement)` - Demo mode
- `clickHiddenElement(By/WebElement)`
- `swtichToBrowserWindowByIndex(int)`
- `moveToElement(By)`, `moveToElement(WebElement, WebElement)`
- `capureScreenshot(String, String)`
- `getAbsuluteFilePath(String)`
- `getCurrentTime()`
- `checkDirectory(String)`

### New Enhanced Methods ⭐
- `getCurrentURL()` - Get current page URL
- `isElementVisible(By)`, `isElementEnabled(By)`, `isElementSelected(By)` - State checks
- `getText(By/WebElement)` - Get element text
- `getAttributeValue(WebElement, String)` - Get attribute value
- `waitForElementClickable(By)` - Wait for clickable
- `waitForElementInvisibility(By)` - Wait for hidden
- `scrollToTop()`, `scrollToBottom()` - Page scrolling
- `captureScreenshotBase64()` - Base64 screenshot for reports
- `doubleClick(WebElement)`, `rightClick(WebElement)` - Mouse actions
- `refreshPage()`, `navigateBack()`, `navigateForward()` - Navigation
- `generateRandomEmail()`, `generateRandomName()`, `generateRandomPhone()` - Test data
- `generateRandomAddress()`, `generateRandomText(int)` - More test data

**Total: 50+ comprehensive methods!**

---

## 🎯 Page Object Pattern

### Example: RequisitionPage (22 Methods)

```java
public class RequisitionPage {
    private WebDriver driver;
    private GlobalSelenium gs;
    
    // Locators
    private By titleInput = By.id("requisitionTitle");
    private By fundTypeDropdown = By.id("fundType");
    private By submitButton = By.xpath("//button[text()='Submit']");
    private By statusBadge = By.id("reqStatus");
    
    public RequisitionPage(WebDriver driver, GlobalSelenium gs) {
        this.driver = driver;
        this.gs = gs;
        gs.waitForElementVisibility(titleInput); // Stability anchor
    }
    
    // Business methods
    public void createRequisition(RequisitionData data) {
        gs.enterText(titleInput, data.getTitle());
        gs.selectDropDown(fundTypeDropdown, data.getFundType());
        gs.clickButton(submitButton);
    }
    
    public FundingLinesPage goToFundingLines() {
        gs.clickButton(By.linkText("Funding Lines"));
        return new FundingLinesPage(driver, gs);
    }
    
    public String getStatus() {
        return gs.getText(statusBadge);
    }
    
    public boolean validateStatus(String expectedStatus) {
        String actualStatus = getStatus();
        return actualStatus.equals(expectedStatus);
    }
    
    // ... 15+ more methods
}
```

### Complete Page Object Methods

#### CBAPS Pages (82 total methods)
- **PortalHomePage** (8 methods): navigate, openCBAPS, openDAWMS, validateLoaded, getTitle, search, isLoggedIn, getNotificationCount
- **CBAPSDashboardPage** (12 methods): goToCreateRequisition, getDashboardMetrics, searchRequisition, getRecentCount, validateLoaded, hasNotifications, waitForReady, etc.
- **RequisitionPage** (22 methods): createRequisition, fillForm, saveAsDraft, validateForm, getStatus, getRequisitionId, validateStatus, goToFundingLines, routeForApproval, canEdit, canDelete, getMetadata, clearForm, cancel, etc.
- **FundingLinesPage** (18 methods): addFundingLine, addMultiple, getTotalAmount, getLineCount, validateTotal, validateCount, deleteLine, getAllAmounts, calculateTotal, verifyCalculation, canContinue, continueToRouting, etc.
- **RoutingApprovalPage** (10 methods): submitForApproval, getEstimatedTime, validateApprover, addComments, selectLevel, etc.
- **StatusTrackerPage** (12 methods): getStatus, getRequisitionId, validateStatus, getWorkflowResult, hasApprovalHistory, getHistoryCount, printRequisition, etc.

#### DAWMS Pages (75 total methods)
- **PortalHomePage**, **DAWMSDashboardPage** (similar pattern)
- **SubmissionIntakePage** (18 methods)
- **ReviewerAssignmentPage** (20 methods): assignReviewer, assignMultiple, getReviewerCount, validateCount, deleteReviewer, getAllReviewers, canContinue, routeToSignature, etc.
- **SignatureRoutingPage** (12 methods)
- **MilestoneStatusPage** (15 methods): getMilestone, getStatus, validateMilestone, validateStatus, validateWorkflow, getWorkflowResult, hasReviewHistory, etc.

---

## 🧪 Comprehensive Test Scenarios

### CBAPS Tests (6 Scenarios)

```java
@Test
public void completeWorkflowTest() {
    // Portal → Dashboard → Create Requisition → Add Funding → Route → Validate
    PortalHomePage portal = new PortalHomePage(driver, gs);
    portal.navigateToPortal("https://cbaps.example.com");
    
    CBAPSDashboardPage dashboard = portal.openCBAPS();
    Assert.assertTrue(dashboard.validateDashboardLoaded());
    
    RequisitionPage reqPage = dashboard.goToCreateRequisition();
    RequisitionData data = new RequisitionData("FY26 Project", "Operations");
    reqPage.createRequisition(data);
    
    FundingLinesPage fundingPage = reqPage.goToFundingLines();
    fundingPage.addFundingLine(new FundingLineData("25000", "2026"));
    Assert.assertEquals(fundingPage.getTotalAmount(), 25000.0);
    
    RoutingApprovalPage routingPage = fundingPage.continueToRouting();
    StatusTrackerPage statusPage = routingPage.submitForApproval("Branch Chief");
    
    Assert.assertTrue(statusPage.validateStatus("Submitted"));
}

@Test
public void multipleFundingLinesTest() {
    // Test with multiple funding lines and calculations
}

@Test
public void draftSaveResumeTest() {
    // Save as draft and verify metadata
}

@Test
public void formValidationTest() {
    // Test empty and partial form validation
}

@Test
public void dashboardMetricsTest() {
    // Validate dashboard metrics and search
}

@Test(dataProvider = "excelData")
public void dataClassDrivenTest(String title, String fundType, String amount) {
    // Excel-driven parameterized test
}
```

### DAWMS Tests (7 Scenarios)

```java
@Test
public void completeSubmissionWorkflowTest() {
    // Full workflow with multiple reviewers
}

@Test
public void singleReviewerTest() {
    // Simplified single reviewer flow
}

@Test
public void multipleReviewersValidationTest() {
    // Complex reviewer assignment with 5 reviewers
}

@Test
public void draftSubmissionTest() {
    // Save submission as draft
}

@Test
public void formValidationTest() {
    // Form validation scenarios
}

@Test
public void dashboardSearchTest() {
    // Search and metrics functionality
}

@Test
public void stepByStepValidationTest() {
    // Validation at each workflow step
}
```

---

## 🔌 REST Assured API Testing

### APIHelper Class

```java
public class APIHelper {
    private static final String BASE_URL = "https://api.cbaps.example.com";
    
    public static Response getRequest(String endpoint) {
        return given()
            .baseUri(BASE_URL)
            .contentType(ContentType.JSON)
            .when()
            .get(endpoint)
            .then()
            .extract().response();
    }
    
    public static Response postRequest(String endpoint, Object body) {
        return given()
            .baseUri(BASE_URL)
            .contentType(ContentType.JSON)
            .body(body)
            .when()
            .post(endpoint)
            .then()
            .extract().response();
    }
    
    // PUT, DELETE, PATCH methods
    // Authentication methods
    // Response validation methods
}
```

### API Test Examples

```java
@Test
public void testGetRequisitions() {
    Response response = APIHelper.getRequest("/requisitions");
    
    Assert.assertEquals(response.getStatusCode(), 200);
    Assert.assertTrue(response.jsonPath().getList("data").size() > 0);
}

@Test
public void testCreateRequisitionAPI() {
    RequisitionData data = new RequisitionData("API Test", "Operations");
    
    Response response = APIHelper.postRequest("/requisitions", data);
    
    Assert.assertEquals(response.getStatusCode(), 201);
    String requisitionId = response.jsonPath().getString("id");
    Assert.assertNotNull(requisitionId);
}

@Test
public void testValidateRequisitionStatus() {
    String reqId = "REQ-12345";
    
    Response response = APIHelper.getRequest("/requisitions/" + reqId);
    
    Assert.assertEquals(response.jsonPath().getString("status"), "Submitted");
}
```

---

## 📊 Data-Driven Testing

### Excel Structure

**cbaps-test-data.xlsx:**
| Title | Description | FundType | Priority | Amount | FiscalYear |
|-------|-------------|----------|----------|--------|------------|
| FY26 Cloud | Cloud services | Operations | High | 25000 | 2026 |
| FY26 Training | Staff training | Training | Medium | 15000 | 2026 |

### ExcelManager Usage

```java
ExcelManager excel = new ExcelManager("testdata/cbaps-test-data.xlsx", "Sheet1");
Object[][] data = excel.getAllData();

@DataProvider(name = "excelData")
public Object[][] getTestData() {
    return excel.getAllData();
}

@Test(dataProvider = "excelData")
public void dataClassDrivenTest(String title, String fundType, String amount) {
    // Use Excel data in test
}
```

---

## ⚡ Parallel Execution

### TestNG Configuration

```xml
<!-- testng-parallel.xml -->
<suite name="Parallel Suite" parallel="tests" thread-count="4">
    <test name="CBAPS Thread 1">
        <classes>
            <class name="com.automation.cbaps.tests.CBAPSEndToEndTests"/>
        </classes>
    </test>
    
    <test name="DAWMS Thread 2">
        <classes>
            <class name="com.automation.dawms.tests.DAWMSEndToEndTests"/>
        </classes>
    </test>
</suite>
```

```bash
# Run with 4 parallel threads
mvn test -DsuiteXmlFile=testng-parallel.xml
```

---

## 📈 ExtentReports

### Report Features
- Beautiful HTML reports
- Screenshots on failure
- Test step logging
- Execution timeline
- Environment info
- System metrics

### Usage in Tests

```java
@BeforeClass
public void setup() {
    extent = ExtentManager.getInstance();
    test = extent.createTest("Complete Workflow Test");
}

@Test
public void testWorkflow() {
    test.log(Status.INFO, "Step 1: Navigate to portal");
    // ... test code ...
    
    test.log(Status.PASS, "Step 2: Created requisition");
    // ... more steps ...
}

@AfterMethod
public void tearDown(ITestResult result) {
    if (result.getStatus() == ITestResult.FAILURE) {
        String screenshot = gs.captureScreenshotBase64();
        test.fail("Test failed", MediaEntityBuilder
            .createScreenCaptureFromBase64String(screenshot).build());
    }
}
```

---

## 🎓 Best Practices Implemented

1. **Page Object Model** - All UI interactions in Page Objects
2. **Method Chaining** - Fluent APIs for readability
3. **Stability Anchors** - Wait for page load in constructors
4. **Comprehensive Logging** - Log4j2 throughout
5. **Error Handling** - Try-catch with assertions
6. **Screenshot on Failure** - Automatic capture
7. **Data-Driven** - Excel integration
8. **Parallel Execution** - TestNG support
9. **API Integration** - REST Assured tests
10. **Maintainability** - Clear separation of concerns

---

## 🛠️ Configuration

### System Properties
- `-Dbrowser=chrome|firefox|edge` - Browser selection
- `-Dheadless=true|false` - Headless mode
- `-DsuiteXmlFile=testng.xml` - TestNG suite

### Environment Variables
```properties
# config.properties
base.url=https://cbaps.example.com
api.url=https://api.cbaps.example.com
browser=chrome
headless=false
timeout=30
```

---

## 📦 Dependencies (pom.xml)

- **Selenium WebDriver** 4.15.0
- **TestNG** 7.8.0
- **REST Assured** 5.3.2
- **ExtentReports** 5.1.1
- **Apache POI** 5.2.4 (Excel)
- **Log4j2** 2.20.0
- **Datafaker** 2.0.2
- **AssertJ** 3.24.2
- **Jackson** 2.15.3 (JSON)

---

## 🚀 CI/CD Integration

### GitHub Actions Example

```yaml
name: Selenium Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '11'
      - run: mvn clean test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: extent-reports
          path: target/extent-reports/
```

---

## 📚 Additional Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [TestNG Documentation](https://testng.org/doc/)
- [REST Assured](https://rest-assured.io/)
- [ExtentReports](https://www.extentreports.com/)

---

## 🎉 Summary

This **enterprise-grade framework** provides:

✅ **50+ enhanced Selenium methods** (original + 20 new)  
✅ **6-7 comprehensive test scenarios** per application  
✅ **15-22 methods per Page Object** with validations  
✅ **REST Assured** API testing integration  
✅ **Data-driven testing** with Excel  
✅ **Parallel execution** with TestNG  
✅ **Beautiful ExtentReports** with screenshots  
✅ **Production-ready** with proper error handling  

**Framework Version**: 1.0.0  
**Created**: February 2026  
**Technologies**: Java 11, Selenium 4, TestNG, REST Assured, Maven  
**Pattern**: Enhanced Page Object Model  
**Applications**: CBAPS, DAWMS
